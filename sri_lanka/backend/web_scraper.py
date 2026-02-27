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
    Attempts to find a price pattern (e.g., $12.50) in text.
    Returns the first match or None.
    """
    match = re.search(r'\$\d+(?:\.\d{2})?', text)
    if match:
        return match.group(0)
    return None

def search_ddg(query, num_results=5):
    """
    Searches DuckDuckGo HTML version for the query and extracts potential price information.
    Retries once on failure.
    """
    # Specific search for Coles and Woolworths results
    search_term = f"{query} site:coles.com.au OR site:woolworths.com.au price"
    url = "https://html.duckduckgo.com/html/"
    data = {'q': search_term}
    
    for attempt in range(2):
        try:
            headers = get_random_header()
            # print(f"Scraping DDG for: {search_term} (Attempt {attempt+1})")
            
            response = requests.post(url, data=data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                results = []
                for result in soup.find_all('div', class_='result'):
                    title_tag = result.find('a', class_='result__a')
                    if not title_tag:
                        continue
                        
                    title = title_tag.get_text(strip=True)
                    link = title_tag['href']
                    snippet_tag = result.find('a', class_='result__snippet')
                    snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""
                    
                    # Determine source
                    source = "Unknown"
                    if 'coles.com.au' in link:
                        source = "Coles"
                    elif 'woolworths.com.au' in link:
                        source = "Woolworths"
                    
                    # Try to extract price from snippet or title
                    price = extract_price_from_text(title) or extract_price_from_text(snippet)
                    
                    if price:
                         results.append({
                            "title": title,
                            "link": link,
                            "snippet": snippet,
                            "source": source,
                            "price": price
                        })
                    
                    if len(results) >= num_results:
                        break
                
                return results
                
            elif response.status_code == 429:
                # Rate limited, wait a bit and retry (or just return empty if it's the last attempt)
                time.sleep(2)
                continue
            else:
                # Other error
                continue

        except Exception as e:
            print(f"Error scraping DDG: {e}")
            time.sleep(1)
            
    return []

if __name__ == "__main__":
    # Test
    print(search_ddg("Red Bull Lilac Edition"))
