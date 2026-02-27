import os
import psycopg2
import csv
from dotenv import load_dotenv
from difflib import SequenceMatcher

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

def get_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def generate_common_report():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        print("Fetching data...")
        
        # Get all text from each shop
        cur.execute("SELECT text FROM rag.data_supermarket_docs WHERE metadata_->>'shop_name' = 'Coles'")
        coles_text = " ".join([r[0] for r in cur.fetchall()])
        
        cur.execute("SELECT text FROM rag.data_supermarket_docs WHERE metadata_->>'shop_name' = 'Woolworths'")
        woolies_text = " ".join([r[0] for r in cur.fetchall()])
        
        # Extract meaningful terms (2-3 word phrases that look like product names)
        def extract_product_terms(text):
            import re
            # Clean text
            text = text.replace('\n', ' ').lower()
            # Look for capitalized phrases or common product patterns
            words = text.split()
            
            terms = set()
            # Add individual meaningful words (longer than 4 chars, likely product names)
            for word in words:
                clean = re.sub(r'[^a-z]', '', word)
                if len(clean) > 4 and clean.isalpha():
                    terms.add(clean)
            
            # Add 2-word phrases
            for i in range(len(words)-1):
                phrase = f"{words[i]} {words[i+1]}"
                clean = re.sub(r'[^a-z ]', '', phrase)
                if len(clean) > 6:
                    terms.add(clean.strip())
                    
            return terms
        
        print("Extracting product terms...")
        coles_terms = extract_product_terms(coles_text)
        woolies_terms = extract_product_terms(woolies_text)
        
        print(f"Coles unique terms: {len(coles_terms)}")
        print(f"Woolworths unique terms: {len(woolies_terms)}")
        
        # Find common terms
        common_terms = coles_terms.intersection(woolies_terms)
        
        print(f"Found {len(common_terms)} common terms")
        
        # Filter out very generic terms
        stopwords = {'price', 'special', 'sale', 'offer', 'save', 'save up', 'catalogue', 'page'}
        common_terms = [t for t in common_terms if t not in stopwords and len(t) > 3]
        
        filename = "common_products.csv"
        
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Common Product Term"])
            
            for term in sorted(common_terms)[:100]:  # Top 100 common terms
                writer.writerow([term])
                
        print(f"Generated {filename} with {len(common_terms)} common product terms")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    generate_common_report()
