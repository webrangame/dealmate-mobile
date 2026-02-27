#!/usr/bin/env python3
import asyncio
import os
import io
import base64
import json
import pdfplumber
from litellm import acompletion

# Configuration
LITELLM_API_KEY = os.getenv("LITELLM_API_KEY", "sk-dYB1jYkLtjgz6gaARNDGng")
LITELLM_API_BASE = os.getenv("LITELLM_API_BASE", "https://swzissb82u.us-east-1.awsapprunner.com")
MODEL = "openai/gemini-2.0-flash"

async def extract_products_from_image(image_bytes, page_num, shop_name):
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    
    prompt = (
        f"Extract all products from this {shop_name} catalog page.\n"
        "Return a JSON object with a single key 'products' containing a list of objects.\n"
        "Each object must have:\n"
        "- 'name': Full product name including brand and copy\n"
        "- 'price': The price (e.g. '$5.00')\n"
        "- 'size': Weight or volume if available (e.g. '500g')\n"
        "- 'deal': Any deal info (e.g. 'Save $2', '1/2 Price')\n"
        "If no products are found, return {'products': []}.\n"
        "Do not include markdown formatting like ```json ... ```. Just the raw JSON string."
    )

    try:
        response = await acompletion(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        }
                    ]
                }
            ],
            api_key=LITELLM_API_KEY,
            api_base=LITELLM_API_BASE,
            temperature=0.1
        )
        content = response.choices[0].message.content
        # Clean up markdown code blocks if present
        content = content.replace("```json", "").replace("```", "").strip()
        data = json.loads(content)
        return data.get('products', [])
    except Exception as e:
        print(f"Error processing {shop_name} page {page_num}: {e}")
        return []

async def process_pdf(pdf_path, max_pages=None):
    shop_name = os.path.splitext(os.path.basename(pdf_path))[0]
    print(f"Processing {shop_name}...")
    
    products = []
    tasks = []
    
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        pages_to_process = pdf.pages[:max_pages] if max_pages else pdf.pages
        
        # Create a semaphore to limit concurrency
        sem = asyncio.Semaphore(5) 
        
        async def bounded_process(page, page_num):
            async with sem:
                print(f"  - Scanning page {page_num}/{len(pages_to_process)}...")
                # high resolution for better OCR
                img = page.to_image(resolution=200).original 
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='JPEG')
                page_products = await extract_products_from_image(img_byte_arr.getvalue(), page_num, shop_name)
                
                # Add page info
                for p in page_products:
                    p['page'] = page_num
                    p['shop'] = shop_name
                
                return page_products

        for i, page in enumerate(pages_to_process, 1):
             tasks.append(bounded_process(page, i))
        
        results = await asyncio.gather(*tasks)
        for res in results:
            products.extend(res)
            
    return products

async def main():
    base_dir = "/home/ranga/code/pragith/whatssapp-chat/supermarket-rag"
    pdfs = [
        # os.path.join(base_dir, 'Coles.pdf'),
        os.path.join(base_dir, 'Woolworths.pdf') # Woolworths failed previously, prioritize it
    ]
    # Add Coles if it exists
    if os.path.exists(os.path.join(base_dir, 'Coles.pdf')):
         pdfs.insert(0, os.path.join(base_dir, 'Coles.pdf'))

    all_products = []
    
    for pdf_path in pdfs:
        if os.path.exists(pdf_path):
            # Limit pages for speed if needed, but user asked for ALL. 
            # I'll do all but handled concurrently.
            shop_products = await process_pdf(pdf_path)
            all_products.extend(shop_products)
    
    # Output Results
    output_dir = os.path.join(base_dir, 'product_listings_vision')
    os.makedirs(output_dir, exist_ok=True)
    
    # JSON
    with open(os.path.join(output_dir, 'all_products.json'), 'w') as f:
        json.dump(all_products, f, indent=2)
        
    # Text
    with open(os.path.join(output_dir, 'all_products.txt'), 'w') as f:
        f.write("PRODUCT LISTING (VISION EXTRACTED)\n")
        f.write("==================================\n\n")
        
        current_shop = ""
        for p in all_products:
            if p['shop'] != current_shop:
                current_shop = p['shop']
                f.write(f"\n--- {current_shop} ---\n")
            
            line = f"[{p.get('price', 'N/A')}] {p.get('name', 'Unknown')} ({p.get('size', '')})"
            if p.get('deal'):
                line += f" | {p['deal']}"
            f.write(line + "\n")
            
    print(f"\nDone! Saved {len(all_products)} products to {output_dir}")

if __name__ == "__main__":
    asyncio.run(main())
