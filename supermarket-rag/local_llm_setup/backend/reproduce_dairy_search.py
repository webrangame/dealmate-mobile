import os
import psycopg2
from sqlalchemy.engine.url import make_url
import re
import sys
from dotenv import load_dotenv
import math

# Load env from current directory
load_dotenv()

DB_URL = os.getenv("DATABASE_URL")
if not DB_URL:
    print("Error: DATABASE_URL not set in environment or .env file")
    sys.exit(1)

def get_nodes():
    print("Connecting to DB...")
    url = make_url(DB_URL)
    try:
        conn = psycopg2.connect(
            host=url.host, port=url.port, database=url.database,
            user=url.username, password=url.password, sslmode='require',
            connect_timeout=10
        )
        print("Connected.")
        cur = conn.cursor()
        
        #rag_engine uses data_supermarket_docs
        cur.execute("SELECT text, metadata_ FROM rag.data_supermarket_docs")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        print(f"Retrieved {len(rows)} nodes.")
        return rows
    except Exception as e:
        print(f"DB Error: {e}")
        sys.exit(1)

def score_nodes(query_text, nodes):
    # Copying logic from NEW rag_engine.py query method (keyword matching part)
    generic_question_words = {
        "what", "how", "where", "much", "many", "show", "tell", "list", "find", 
        "the", "for", "with", "is", "of", "in", "at", "on", "a", "an", "and", 
        "do", "you", "have", "are", "any", "me", "show", "list", "give", "can", "could"
    }
    
    clean_text = re.sub(r'[^\w\s]', '', query_text)
    words = clean_text.split()
    
    # All words > 2 that aren't generic question words
    keywords = [w.lower() for w in words if len(w) > 2 and w.lower() not in generic_question_words]
    
    # Significant words (capitalized or long)
    # FIX: Exclude common non-brand words from being treated as brands just because they are long
    common_non_brands = {
        "powder", "packet", "bottle", "carton", "flavour", "flavour", "sachet", "medium", "large", "small", 
        "family", "value", "pack", "piece", "pieces", "gram", "grams", "liter", "litre", "slices", "slice",
        "frozen", "fresh", "market", "pantry", "bakery", "served", "serve", "serving", "people", "adult"
    }
    brand_keywords = [
        w.lower() for i, w in enumerate(words) 
        if (w[0].isupper() or len(w) > 5) 
        and w.lower() not in generic_question_words 
        and w.lower() not in common_non_brands
    ]
    
    print(f"\nQUERY: {query_text}")
    print(f"Keywords: {keywords}")
    print(f"Brand Keywords: {brand_keywords}")
    
    noise_keywords = [
        "deli promotions", "noranda square", "western australian regular", 
        "reserves the right to limit", "savings are shown off", "prices may vary in regional",
        "terms and conditions apply", "while stocks last", "multi save", "catalogue prices",
        "tobacco products", "gift cards", "excludes clearance", "not available in all stores"
    ]
    
    # Negative Keywords
    chocolate_terms = {"chocolate", "candy", "confectionery", "cadbury", "cocoa", "easter", "bunny", "egg"}
    query_has_chocolate = any(t in clean_text for t in chocolate_terms)
    
    query_has_powder = "powder" in clean_text
    query_has_milk = "milk" in clean_text

    scored_results = []
    
    for txt, meta in nodes:
        txt_low = txt.lower()
        # Handle meta which might be a dict (from rag_engine) or tuple/list if fetched raw
        # In this script, meta is from SQL metadata_ (string/json?) -> wait, get_nodes fetches metadata_
        # metadata_ in SQL is JSONB, psycopg2 returns dict.
        product_name = meta.get('product_name', '').lower() if isinstance(meta, dict) else ""
        
        score = 0
        
        # 1. Boost based on brand/significant keywords (high priority)
        for bkw in brand_keywords:
            if re.search(r'\b' + re.escape(bkw) + r'\b', txt_low):
                score += 80 
        
        # 2. General Keyword Overlap
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', txt_low):
                score += 40 
                
        # 3. Exact Sequence Match
        clean_query = " ".join(keywords).lower()
        if clean_query and clean_query in txt_low:
             score += 120 
             
        # 4. Penalize Noise
        for noise in noise_keywords:
            if noise in txt_low:
                score -= 40
        
        # 6. Multi-word match bonus
        if len(keywords) >= 2 and all(re.search(r'\b' + re.escape(kw) + r'\b', txt_low) for kw in keywords):
            score += 200 

        # 7. Price Evidence Bonus
        if "$" in txt or "price" in txt_low or "save" in txt_low:
            score += 50

        # 8. Title/Header Bonus
        if txt.strip().startswith("#") or (len(txt) < 100 and any(kw in txt_low for kw in keywords)):
            score += 40

        # 9. Product Name field bonus (Stronger than just text match)
        if product_name:
             for kw in keywords:
                 if kw in product_name:
                     score += 50
        
        # 10. Negative Boosting (Context Awareness)
        if not query_has_chocolate:
            # If product mentions chocolate/candy but user didn't ask for it -> Penalize
            if any(bad in txt_low for bad in chocolate_terms):
                score -= 100
            
            # Special case: "Milk Powder" vs "Dairy Milk" (Chocolate)
            if query_has_milk and "cadbury" in txt_low:
                score -= 1000 # Heavy penalty for Cadbury
        
        # 11. Category Boost
        if query_has_powder and "powder" in product_name:
            score += 100
            
        # 12. Milk Powder Specific Logic
        if query_has_powder and query_has_milk:
            # Boost purely for the phrase "milk powder" or "powdered milk"
            if "milk powder" in txt_low or "powdered milk" in txt_low or "instant milk" in txt_low:
                score += 200
            
            # Penalize irrelevant powders if user didn't ask for them
            irrelevant_powders = {"protein", "muscle", "water", "laundry", "washing", "detergent", "whey", "workout", "supplement"}
            # Check what user asked for vs what is in result
            user_wants_irrelevant = any(bad in clean_text for bad in irrelevant_powders)
            
            if not user_wants_irrelevant:
                if any(bad in txt_low for bad in irrelevant_powders):
                    score -= 1000 # Increased from -500 to -1000. ABSOLUTELY NUKE IT.
            
        if score >= 35:
            scored_results.append({
                "score": score,
                "text": txt[:300].replace('\n', ' '),
                "product": meta.get('product_name', 'Unknown') if isinstance(meta, dict) else "Unknown",
                "shop": meta.get('shop_name', 'Unknown') if isinstance(meta, dict) else "Unknown",
                "metadata": meta
            })
            
    scored_results.sort(key=lambda x: x["score"], reverse=True)
    return scored_results[:20]

def main():
    nodes = get_nodes()
    
    # Simulating what user typed: "dairy milk powder for adult"
    # User said: "I wanted to search dairy milk powder for adult but it does show.rather it shows Cadbury products etc"
    # So likely query is "dairy milk powder" or "dairy milk powder for adult"
    
    queries = [
        "dairy milk powder for adult",
        "dairy milk powder"
    ]
    
    for q in queries:
        print(f"\n{'='*50}")
        print(f"SEARCHING FOR: {q}")
        print(f"{'='*50}")
        results = score_nodes(q, nodes)
        print(f"Found {len(results)} results above threshold.")
        for i, res in enumerate(results):
            print(f"{i+1}. [Score: {res['score']}] {res['product']} ({res['shop']})")
            # print(f"   Context: {res['text']}...")
            print("-" * 20)

if __name__ == "__main__":
    main()
