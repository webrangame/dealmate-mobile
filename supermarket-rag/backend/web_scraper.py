import requests
from bs4 import BeautifulSoup
import random
import time
import re

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
]

def get_random_header():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/"
    }

def extract_price_from_text(text):
    """
    Attempts to find a price pattern (e.g., $12.50, 2 for $5, $1.50/ea) in text.
    """
    # $12.50 or $12
    p1 = re.search(r'\$\d+(?:\.\d{2})?', text)
    if p1:
        # Check for context around it like /ea or /kg
        context_match = re.search(r'\$\d+(?:\.\d{2})?/(?:ea|kg|unit)', text.lower())
        if context_match:
            return context_match.group(0)
        return p1.group(0)
    
    # "2 for $5"
    p2 = re.search(r'\d+\s+for\s+\$\d+(?:\.\d{2})?', text.lower())
    if p2:
        return p2.group(0)
        
    return None

def search_ddg(query, num_results=5):
    """
    Searches DuckDuckGo HTML version for the query and extracts potential price information.
    Attempts a site-specific search first, then a broader search.
    """
    # Clean query: Remove common "at Coles", "from Woolworths" noise
    clean_q = re.sub(r'\s+(at|from|in|for)\s+(coles|woolworths|woolies)', '', query, flags=re.IGNORECASE)
    
    # Try a few variations of search terms
    search_variations = [
        f"{clean_q} site:coles.com.au OR site:woolworths.com.au price",
        f"{clean_q} Australia price Coles Woolworths",
        f"{clean_q} price"
    ]
    
    all_results = []
    seen_links = set()
    
    url = "https://html.duckduckgo.com/html/"
    
    for search_term in search_variations:
        if len(all_results) >= num_results:
            break
            
        data = {'q': search_term}
        try:
            headers = get_random_header()
            response = requests.post(url, data=data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for result in soup.find_all('div', class_='result'):
                    title_tag = result.find('a', class_='result__a')
                    if not title_tag:
                        continue
                        
                    title = title_tag.get_text(strip=True)
                    link = title_tag['href']
                    
                    if link in seen_links:
                        continue
                        
                    snippet_tag = result.find('a', class_='result__snippet')
                    snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""
                    
                    # Determine source
                    source = "Coles" if 'coles.com.au' in link or 'Coles' in title else "Woolworths" if 'woolworths.com.au' in link or 'Woolworths' in title else "Web"
                    
                    # If it's a "Web" result without Coles/Woolworths in title/link, skip for now to maintain relevance
                    if source == "Web" and not any(kw in title.lower() or kw in snippet.lower() for kw in ["coles", "woolworths", "woolies", "supermarket"]):
                        continue
                        
                    # Try to extract price from snippet or title
                    price = extract_price_from_text(title) or extract_price_from_text(snippet)
                    
                    if price:
                        all_results.append({
                            "title": title,
                            "link": link,
                            "snippet": snippet,
                            "source": source,
                            "price": price
                        })
                        seen_links.add(link)
                    
                    if len(all_results) >= num_results:
                        break
                
                # If we found at least 2 results, don't try broader variations to avoid noise
                if len(all_results) >= 2:
                    break
                    
                time.sleep(1) # Polite delay between variations
                
            elif response.status_code == 429:
                time.sleep(2)
                continue
                
        except Exception as e:
            print(f"Error scraping DDG variation: {e}")
            time.sleep(1)
            
    return all_results

if __name__ == "__main__":
    # Test
    print(search_ddg("Red Bull Lilac Edition"))
