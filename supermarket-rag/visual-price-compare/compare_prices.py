import asyncio
import os
import json
import base64
import sys
import argparse
from playwright.async_api import async_playwright
import litellm
from playwright_stealth import Stealth
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

# Ensure we have the necessary API keys
LITELLM_API_KEY = os.getenv("LITELLM_API_KEY")
LITELLM_API_BASE = os.getenv("LITELLM_API_BASE")

# Fix for Gemini: Drop unsupported params like encoding_format
litellm.drop_params = True

async def extract_intent(prompt: str):
    """Uses LLM to parse user prompt into structured search queries."""
    sys.stderr.write(f"Extracting intent from prompt: {prompt}\n")
    
    intent_prompt = (
        "Parse this supermarket price comparison request. "
        "Return a JSON object with: \n"
        "- 'coles_query': precise search term for Coles website (e.g. 'Connoisseur Ice Cream')\n"
        "- 'ww_query': precise search term for Woolworths website\n"
        "- 'product_name': simple name of the product being compared\n"
        f"Request: {prompt}"
    )
    
    try:
        response = completion(
            model="openai/gemini-2.0-flash",
            messages=[{"role": "user", "content": intent_prompt}],
            api_key=LITELLM_API_KEY,
            api_base=LITELLM_API_BASE,
            response_format={ "type": "json_object" }
        )
        content = response.choices[0].message.content
        data = json.loads(content)
        
        # Ensure we return a dictionary
        if isinstance(data, list) and len(data) > 0:
            return data[0]
        elif isinstance(data, dict):
            return data
            
        return {
            "coles_query": prompt,
            "ww_query": prompt,
            "product_name": prompt
        }
    except Exception as e:
        sys.stderr.write(f"Intent extraction failed: {e}\n")
        # Fallback to simple query if LLM fails
        return {
            "coles_query": prompt,
            "ww_query": prompt,
            "product_name": prompt
        }

async def get_page_data(page, store_name):
    """Extracts relevant text data from the page for LLM processing."""
    try:
        # Get visible text from product grid
        # This is more robust than just raw text
        products = await page.evaluate("""() => {
            const results = [];
            // Generic selectors that often catch product tiles
            const tiles = document.querySelectorAll('data-testimonial-id, .product-tile, [data-testid="product-tile"], .coles-targeting-ProductTileChild');
            tiles.forEach(tile => {
                results.push(tile.innerText.replace(/\\s+/g, ' ').trim());
            });
            
            // Fallback: Just get all text if no tiles found
            if (results.length === 0) {
                return document.body.innerText.substring(0, 5000); 
            }
            return results.slice(0, 10).join('\\n---\\n');
        }""")
        return products
    except Exception as e:
        sys.stderr.write(f"Data extraction failed for {store_name}: {e}\n")
        return None

async def capture_and_extract(intent: dict):
    results = {}
    coles_query = intent.get('coles_query', '')
    ww_query = intent.get('ww_query', '')
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled', '--no-sandbox']
        )
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            }
        )
        
        stealth = Stealth()
        filename = intent.get('product_name', 'product').replace(' ', '_').lower()

        # 1. Coles
        page = await context.new_page()
        await stealth.apply_stealth_async(page)
        coles_url = f"https://www.coles.com.au/search?q={coles_query.replace(' ', '%20')}"
        sys.stderr.write(f"Navigating to Coles: {coles_url}\n")
        results['coles_text'] = None
        results['coles_img'] = None
        try:
            await page.goto(coles_url, wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(5)
            # Extract text data
            results['coles_text'] = await get_page_data(page, "Coles")
            # Take screenshot
            coles_path = f"public/screenshots/coles_{filename}.png"
            await page.screenshot(path=coles_path, full_page=False)
            results['coles_img'] = coles_path.replace('public/', '')
        except Exception as e:
            sys.stderr.write(f"Coles capture failed: {e}\n")
        
        # 2. Woolworths
        page = await context.new_page()
        await stealth.apply_stealth_async(page)
        ww_url = f"https://woolworths.com.au/shop/search/products?searchTerm={ww_query.replace(' ', '%20')}"
        sys.stderr.write(f"Navigating to Woolworths: {ww_url}\n")
        results['ww_text'] = None
        results['ww_img'] = None
        try:
            await page.goto(ww_url, wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(5)
            # Extract text data
            results['ww_text'] = await get_page_data(page, "Woolworths")
            # Take screenshot
            ww_path = f"public/screenshots/woolworths_{filename}.png"
            await page.screenshot(path=ww_path, full_page=False)
            results['ww_img'] = ww_path.replace('public/', '')
        except Exception as e:
            sys.stderr.write(f"Woolworths capture failed: {e}\n")
            
        await browser.close()
    return results

def encode_image(image_rel_path):
    if not image_rel_path:
        return None
    image_path = os.path.join("public", image_rel_path)
    if not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

async def compare_with_llm(data: dict, original_prompt: str):
    """Performs comparison using both text and vision if available."""
    coles_b64 = encode_image(data.get('coles_img'))
    ww_b64 = encode_image(data.get('ww_img'))
    coles_text = data.get('coles_text')
    ww_text = data.get('ww_text')
    
    if not coles_text and not ww_text and not coles_b64 and not ww_b64:
        return {"error": "Failed to retrieve any data from either site."}
    
    # Construct combined prompt
    prompt_content = [
        {"type": "text", "text": f"Instruction: {original_prompt}\n\n"
                                  "Below is the data extracted from the supermarket sites.\n\n"
                                  "COLES DATA:\n"
                                  f"{coles_text or 'No text data captured.'}\n\n"
                                  "WOOLWORTHS DATA:\n"
                                  f"{ww_text or 'No text data captured.'}\n\n"
                                  "Compare the products and prices. Return a JSON object with:\n"
                                  "- 'matches': a list of objects with 'product_name', 'coles_price', 'ww_price', 'unit'.\n"
                                  "- 'summary': a detailed textual comparison following the user's instructions.\n"
                                  "Focus on accurate price extraction from both the text and the images (if provided)."}
    ]
    
    if coles_b64:
        prompt_content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{coles_b64}"}})
        prompt_content.append({"type": "text", "text": "Screenshot 1: Coles"})
        
    if ww_b64:
        prompt_content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{ww_b64}"}})
        prompt_content.append({"type": "text", "text": "Screenshot 2: Woolworths"})

    try:
        sys.stderr.write(f"Sending comparison request to LLM (Gemini 2.0 Flash)...\n")
        response = completion(
            model="openai/gemini-2.0-flash", 
            messages=[{"role": "user", "content": prompt_content}],
            api_key=LITELLM_API_KEY,
            api_base=LITELLM_API_BASE,
            response_format={ "type": "json_object" }
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        sys.stderr.write(f"LLM analysis failed: {str(e)}\n")
        return {"error": f"LLM analysis failed: {str(e)}", "matches": [], "summary": "Could not extract price information."}

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    args = parser.parse_args()
    
    # Phase 1: Intent
    intent = await extract_intent(args.prompt)
    
    # Phase 2: Capture & Extract
    data = await capture_and_extract(intent)
    
    # Phase 3: Compare
    comparison = await compare_with_llm(data, args.prompt)
    
    # Add screenshot info for UI
    comparison['screenshots'] = {
        'coles': data.get('coles_img'),
        'woolworths': data.get('ww_img')
    }
    
    print(json.dumps(comparison))

if __name__ == "__main__":
    asyncio.run(main())
