import os
import httpx
import asyncio
from bs4 import BeautifulSoup
import re
from rag_engine import rag_engine

# Configuration
UPLOAD_DIR = "uploaded_docs"
COLES_CATALOG_URL = "https://www.coles.com.au/catalogues"
WOOLWORTHS_CATALOG_URL = "https://www.woolworths.com.au/shop/catalogue/view"

async def get_coles_pdf_url():
    """
    Attempts to find the latest Coles NSW Metro PDF.
    Strategy: Try Cloudfront patterns first, then fallback to manual URLs.
    """
    print("Searching for Coles PDF...")
    
    # Current week pattern (Feb 11-17, 2026)
    current_week_urls = [
        "https://d3vvi2v9oj75wh.cloudfront.net/uploads/pdf/COLNSWMETRO_110226_AQM6NRS.pdf",
        "https://d3vvi2v9oj75wh.cloudfront.net/uploads/pdf/COLVICMETRO_110226_AQM6NRS.pdf"
    ]
    
    # Try current week URLs first
    async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
        for url in current_week_urls:
            try:
                resp = await client.head(url)
                if resp.status_code == 200:
                    print(f"✓ Found Coles PDF: {url}")
                    return url
            except Exception:
                continue
    
    # Fallback: Try scraping (unlikely to work but worth trying)
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            headers = {"User-Agent": "Mozilla/5.0"}
            resp = await client.get(COLES_CATALOG_URL, headers=headers)
            pdf_links = re.findall(r'https?://d3vvi2v9oj75wh\.cloudfront\.net/uploads/pdf/COL[A-Z0-9_]+\.pdf', resp.text)
            if pdf_links:
                print(f"✓ Found Coles PDF via scraping: {pdf_links[0]}")
                return pdf_links[0]
    except Exception as e:
        print(f"Scraping Coles failed: {e}")
    
    print(f"⚠ Using fallback Coles URL (may be outdated): {current_week_urls[0]}")
    return current_week_urls[0]

async def get_woolworths_pdf_url():
    """
    Attempts to find the latest Woolworths NSW PDF.
    Strategy: Try Cloudfront patterns first, then fallback to manual URLs.
    """
    print("Searching for Woolworths PDF...")
    
    # Current week pattern (Feb 11-17, 2026)
    current_week_urls = [
        "https://d3vvi2v9oj75wh.cloudfront.net/uploads/pdf/WW_NSW_110226_5UK7TA7434.pdf",
        "https://d3vvi2v9oj75wh.cloudfront.net/uploads/pdf/WW_VIC_110226_5UK7TA7434.pdf"
    ]
    
    # Try current week URLs first
    async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
        for url in current_week_urls:
            try:
                resp = await client.head(url)
                if resp.status_code == 200:
                    print(f"✓ Found Woolworths PDF: {url}")
                    return url
            except Exception:
                continue
    
    # Fallback: Try scraping (unlikely to work but worth trying)
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            headers = {"User-Agent": "Mozilla/5.0"}
            resp = await client.get(WOOLWORTHS_CATALOG_URL, headers=headers)
            pdf_links = re.findall(r'https?://d3vvi2v9oj75wh\.cloudfront\.net/uploads/pdf/WW_[A-Z0-9_]+\.pdf', resp.text)
            if pdf_links:
                print(f"✓ Found Woolworths PDF via scraping: {pdf_links[0]}")
                return pdf_links[0]
    except Exception as e:
        print(f"Scraping Woolworths failed: {e}")
    
    print(f"⚠ Using fallback Woolworths URL (may be outdated): {current_week_urls[0]}")
    return current_week_urls[0]

async def download_file(url, filename):
    """Downloads a file to the upload directory."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, filename)
    print(f"Downloading {url} to {file_path}...")
    
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=120.0) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(resp.content)
                print(f"Successfully downloaded {filename}")
                return file_path
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
    return None

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ... (existing imports)

# Email Configuration
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "api@niyogen.com")
SMTP_PASS = os.getenv("SMTP_PASS", "sicnznjbiswbasqx")
SMTP_FROM = os.getenv("SMTP_FROM_EMAIL", "api@niyogen.com")
TO_EMAIL = "itranga@gmail.com"

# ... (existing code)

def send_email(subject, body):
    """Sends an email notification using Gmail SMTP (primary) or AWS SES (fallback)."""
    # 1. Try Gmail SMTP
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_FROM
        msg['To'] = TO_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        print(f"Attempting Gmail SMTP: {SMTP_HOST}:{SMTP_PORT}...")
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_FROM, TO_EMAIL, msg.as_string())
        server.quit()
        print(f"✓ Email sent successfully via Gmail SMTP to {TO_EMAIL}")
        return
    except Exception as e:
        print(f"⚠ Gmail SMTP failed: {e}")

    # 2. Try AWS SES Fallback
    try:
        print(f"Attempting AWS SES fallback for {TO_EMAIL}...")
        import boto3
        ses = boto3.client(
            'ses',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )
        
        # Check if verified (optional check, send_email will fail anyway if not verified)
        # However, it's better to just try and catch the error
        ses.send_email(
            Source=SMTP_FROM,
            Destination={'ToAddresses': [TO_EMAIL]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}}
            }
        )
        print(f"✓ Email sent successfully via AWS SES to {TO_EMAIL}")
        return
    except Exception as ses_e:
        print(f"CRITICAL ERROR: All email delivery methods failed for {TO_EMAIL}.")
        print(f"SES Error: {ses_e}")

async def run_update():
    print("=== Supermarket Catalog Weekly Automation ===")
    summary = []
    
    # 0. Optional: Cleanup orphans (None shop_name)
    print("Cleaning up orphan database records...")
    await rag_engine.delete_documents_by_shop("None")
    await rag_engine.delete_documents_by_shop("")

    shops = [
        {"name": "Coles", "filename": "Coles.pdf", "finder": get_coles_pdf_url},
        {"name": "Woolworths", "filename": "Woolworths.pdf", "finder": get_woolworths_pdf_url}
    ]
    
    for shop in shops:
        print(f"\n--- Processing {shop['name']} ---")
        
        url = await shop['finder']()
        if not url:
            summary.append(f"❌ {shop['name']}: Could not find PDF URL.")
            continue
            
        path = await download_file(url, shop['filename'])
        if not path:
            summary.append(f"❌ {shop['name']}: Download failed.")
            continue
            
        print(f"Cleaning database for {shop['name']}...")
        await rag_engine.delete_documents_by_shop(shop['name'])
        
        print(f"Ingesting {shop['filename']} into database...")
        try:
            count = await rag_engine.ingest_documents(UPLOAD_DIR, specific_file=shop['filename'])
            print(f"Completed {shop['name']}. Documents processed in session: {count}")
            summary.append(f"✅ {shop['name']}: Updated successfully ({count} chunks ingested).")
        except Exception as e:
            print(f"Ingestion failed for {shop['name']}: {e}")
            summary.append(f"❌ {shop['name']}: Ingestion failed ({str(e)}).")

    print("\n=== Automation Finished ===")
    
    
    # Send Email Report
    email_subject = "Daily Catalog Update"
    email_body = "The daily catalog update has completed.\n\n" + "\n".join(summary)
    
    try:
        send_email(email_subject, email_body)
    except Exception as e:
        print(f"Error in final report email trigger: {e}")

if __name__ == "__main__":
    import sys
    if "--test-email" in sys.argv:
        print("Testing email configuration...")
        try:
            send_email("Test Email from Supermarket RAG", "This is a test email to verify SMTP configuration.")
            print("Test email sent successfully.")
        except Exception as e:
            print(f"Test email failed: {e}")
    else:
        asyncio.run(run_update())
