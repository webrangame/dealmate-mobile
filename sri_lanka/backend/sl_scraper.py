import os
import asyncio
import logging
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from rag_engine import RAGEngine
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

def scrape_cargills_playwright():
    """Scrapes promotions from Cargills Online using Playwright."""
    url = "https://cargillsonline.com/sc/Promotions"
    logger.info(f"Scraping Cargills (Playwright): {url}")
    products = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            page.goto(url, timeout=60000)
            # Wait for product cards to load
            try:
                page.wait_for_selector(".product-card", timeout=10000)
            except:
                logger.warning("Timeout waiting for .product-card selector")

            # Get full HTML after JS execution
            content = page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Simple selector logic (same as before but on JS-rendered HTML)
            cards = soup.select(".product-card")
            if not cards:
                 cards = soup.find_all("div", class_=lambda x: x and "product" in x.lower())
            
            logger.info(f"Found {len(cards)} potnetial cards.")

            for card in cards:
                try:
                    title_elem = card.select_one(".product-title") or card.find("h3") or card.find("h4")
                    price_elem = card.select_one(".price") or card.select_one(".current-price")
                    old_price_elem = card.select_one(".old-price") or card.select_one(".was-price")
                    img_elem = card.select_one("img")
                    
                    if title_elem and price_elem:
                        name = title_elem.get_text(strip=True)
                        price = price_elem.get_text(strip=True)
                        old_price = old_price_elem.get_text(strip=True) if old_price_elem else ""
                        img_url = img_elem['src'] if img_elem and 'src' in img_elem.attrs else ""
                        
                        # Handle relative image URLs
                        if img_url and not img_url.startswith("http"):
                            img_url = f"https://cargillsonline.com{img_url}"

                        savings = "Deal"
                        if old_price:
                            savings = f"WAS {old_price}"

                        products.append({
                            "brand": "Cargills",
                            "name": name,
                            "price": price,
                            "savings": savings,
                            "size": "", 
                            "image_url": img_url,
                            "shop": "Cargills Food City"
                        })
                except Exception:
                    continue
                    
        except Exception as e:
            logger.error(f"Playwright error: {e}")
        finally:
            browser.close()

    logger.info(f"Found {len(products)} products from Cargills.")
    return products

def scrape_keells_playwright():
    """Scrapes promotions from Keells Super using Playwright."""
    url = "https://www.keellssuper.com/promotions"
    logger.info(f"Scraping Keells (Playwright): {url}")
    products = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            page.goto(url, timeout=60000)
            try:
                page.wait_for_selector(".product-item", timeout=10000)
            except:
                logger.warning("Timeout waiting for .product-item selector")

            content = page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            cards = soup.select(".product-item") 
            
            for card in cards:
                try:
                    title_elem = card.select_one(".product-name")
                    price_elem = card.select_one(".product-price")
                    
                    if title_elem and price_elem:
                        name = title_elem.get_text(strip=True)
                        price = price_elem.get_text(strip=True)
                        
                        products.append({
                            "brand": "Keells",
                            "name": name,
                            "price": price,
                            "savings": "Promotion",
                            "size": "",
                            "image_url": "",
                            "shop": "Keells Super"
                        })
                except Exception:
                    continue

        except Exception as e:
            logger.error(f"Playwright error: {e}")
        finally:
             browser.close()

    logger.info(f"Found {len(products)} products from Keells.")
    return products

async def run_daily_update():
    logger.info("Starting Daily Sri Lanka Promotion Update (Playwright)...")
    
    rag = RAGEngine()
    
    # 1. Scrape Cargills
    cargills_deals = scrape_cargills_playwright() # Sync call
    if cargills_deals:
        logger.info(f"Ingesting {len(cargills_deals)} Cargills deals...")
        await rag.ingest_product_batch(cargills_deals)
        
    # 2. Scrape Keells
    keells_deals = scrape_keells_playwright() # Sync call
    if keells_deals:
        logger.info(f"Ingesting {len(keells_deals)} Keells deals...")
        await rag.ingest_product_batch(keells_deals)
        
    logger.info("Daily Update Completed.")

if __name__ == "__main__":
    asyncio.run(run_daily_update())
