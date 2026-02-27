import os
import psycopg2
from sqlalchemy.engine.url import make_url
import re
import sys

DB_URL = "postgresql://postgres:it371Ananda@agent-marketplace-db.cmt466aga8u0.us-east-1.rds.amazonaws.com:5432/postgres?sslmode=require"

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
    generic_question_words = {
        "what", "how", "where", "much", "many", "show", "tell", "list", "find", 
        "the", "for", "with", "is", "of", "in", "at", "on", "a", "an", "and", 
        "do", "you", "have", "are", "any", "me", "show", "list", "give", "can", "could"
    }
    clean_text = re.sub(r'[^\w\s]', '', query_text)
    words = clean_text.split()
    keywords = [w.lower() for w in words if len(w) > 2 and w.lower() not in generic_question_words]
    brand_keywords = [w.lower() for i, w in enumerate(words) if (w[0].isupper() or len(w) > 5) and w.lower() not in generic_question_words]
    
    print(f"\nQUERY: {query_text}")
    print(f"Keywords: {keywords}")
    print(f"Brand Keywords: {brand_keywords}")

    noise_keywords = [
        "deli promotions", "noranda square", "western australian regular", 
        "reserves the right to limit", "savings are shown off", "prices may vary in regional",
        "terms and conditions apply", "while stocks last", "multi save", "catalogue prices",
        "tobacco products", "gift cards", "excludes clearance", "not available in all stores"
    ]

    scored = []
    for txt, meta in nodes:
        txt_low = txt.lower()
        score = 0
        for bkw in brand_keywords:
            if bkw in txt_low: score += 60
        for kw in keywords:
            if kw in txt_low: score += 35
        clean_query = " ".join(keywords).lower()
        if clean_query and clean_query in txt_low:
            score += 100
        for noise in noise_keywords:
            if noise in txt_low: score -= 40
        
        if score > 50: # Threshold in rag_engine is actually not explicitly shown in view_file but usually it takes top K.
            scored.append((score, txt[:200].replace('\n', ' '), meta))
    
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:5]

nodes = get_nodes()
print("\n--- CANADIAN CLUB ---")
for s in score_nodes("Canadian Club in Coles", nodes): print(s)

print("\n--- CAT FOOD ---")
for s in score_nodes("cat food", nodes): print(s)
