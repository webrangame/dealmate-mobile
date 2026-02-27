import os
import httpx
import asyncio
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
from rag_engine import rag_engine
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
UPLOAD_DIR = "uploaded_docs"
COLES_CATALOG_URL = "https://www.coles.com.au/catalogues"
WOOLWORTHS_CATALOG_URL = "https://www.woolworths.com.au/shop/catalogue/view"

# Remote regions to support national coverage
REGIONS = ["NSW", "VIC", "QLD", "WA"]

# Email Configuration (Moved to Environment Variables)
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER") # Critical: Pull from env
SMTP_PASS = os.getenv("SMTP_PASS") # Critical: Pull from env
SMTP_FROM = os.getenv("SMTP_FROM_EMAIL", "api@niyogen.com")
TO_EMAIL = os.getenv("NOTIFICATION_EMAIL", "itranga@gmail.com")

def get_recent_wednesdays(n=5):
    """Returns a list of the last N Wednesdays in DDMMYY format.
    
    We check 5 weeks back because the CDN sometimes delays publishing
    the latest catalogue by 1-2 weeks.
    """
    now = datetime.now()
    dates = []
    # Find the most recent Wednesday (or today if today is Wednesday)
    days_to_sub = (now.weekday() - 2) % 7
    latest = now - timedelta(days=days_to_sub)
    for i in range(n):
        dates.append((latest - timedelta(weeks=i)).strftime("%d%m%y"))
    return dates

async def get_coles_pdf_url(region="NSW"):
    """Attempts to find the latest Coles PDF for a specific region."""
    date_codes = get_recent_wednesdays()
    
    # Common suffix patterns
    suffixes = ["AQM6NRS", "AQH86RS", "AQMNNRS", "AQHTNRS"] 
    
    region_map = {
        "NSW": "COLNSWMETRO",
        "VIC": "COLVICMETRO",
        "QLD": "COLQLDMETRO",
        "WA": "COLWAMETRO"
    }
    
    prefix = region_map.get(region, "COLNSWMETRO")
    
    async with httpx.AsyncClient(follow_redirects=True, timeout=5.0) as client:
        for date_code in date_codes:
            print(f"Checking Coles {region} for date {date_code}...")
            for suffix in suffixes:
                url = f"https://d3vvi2v9oj75wh.cloudfront.net/uploads/pdf/{prefix}_{date_code}_{suffix}.pdf"
                try:
                    resp = await client.head(url)
                    if resp.status_code == 200:
                        print(f"✓ Found Coles {region} PDF: {url}")
                        return url
                except Exception:
                    continue
    return None

async def get_woolworths_pdf_url(region="NSW"):
    """Attempts to find the latest Woolworths PDF for a specific region."""
    date_codes = get_recent_wednesdays()
    
    suffixes = ["5UK7TA7434", "5UK7TA8545", "5UK7TA1122"]
    
    region_map = {
        "NSW": "WW_NSW",
        "VIC": "WW_VIC",
        "QLD": "WW_QLD",
        "WA": "WW_WA"
    }
    
    prefix = region_map.get(region, "WW_NSW")
    
    async with httpx.AsyncClient(follow_redirects=True, timeout=5.0) as client:
        for date_code in date_codes:
            print(f"Checking Woolworths {region} for date {date_code}...")
            for suffix in suffixes:
                url = f"https://d3vvi2v9oj75wh.cloudfront.net/uploads/pdf/{prefix}_{date_code}_{suffix}.pdf"
                try:
                    resp = await client.head(url)
                    if resp.status_code == 200:
                        print(f"✓ Found Woolworths {region} PDF: {url}")
                        return url
                except Exception:
                    continue
    return None

async def download_file(url, filename):
    """Downloads a file to the upload directory if it doesn't already exist."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    print(f"Downloading {url} to {file_path}...")
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=300.0) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(resp.content)
                print(f"Successfully downloaded {filename}")
                return file_path
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
    return None

def send_email(subject, body):
    """Sends an email notification with support for SMTP and AWS SES."""
    if not SMTP_USER or not SMTP_PASS:
        print("⚠ SMTP credentials missing. Skipping email report.")
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_FROM
        msg['To'] = TO_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_FROM, TO_EMAIL, msg.as_string())
        server.quit()
        print(f"✓ Email sent successfully to {TO_EMAIL}")
    except Exception as e:
        print(f"⚠ Email delivery failed: {e}")

async def run_update(dry_run=False):
    print(f"=== Supermarket Catalog Automated Update Pipeline {'(DRY RUN)' if dry_run else ''} ===")
    summary = []
    
    if not dry_run:
        print("Cleaning up outdated records...")
    
    total_ingested = 0
    
    for region in REGIONS:
        print(f"\n--- Processing Region: {region} ---")
        
        # Coles
        coles_url = await get_coles_pdf_url(region)
        if coles_url:
            if dry_run:
                summary.append(f"✓ Coles {region}: URL Found: {coles_url}")
            else:
                filename = f"Coles_{region}.pdf"
                path = await download_file(coles_url, filename)
                if path:
                    try:
                        await rag_engine.delete_documents_by_file(filename)
                        count = await rag_engine.ingest_documents(UPLOAD_DIR, specific_file=filename)
                        summary.append(f"✅ Coles {region}: {count} chunks")
                        total_ingested += count
                        os.remove(path)
                    except Exception as e:
                        summary.append(f"❌ Coles {region}: Ingestion Error: {e}")
        else:
            summary.append(f"❌ Coles {region}: URL Not Found")
            
        # Woolworths
        ww_url = await get_woolworths_pdf_url(region)
        if ww_url:
            if dry_run:
                summary.append(f"✓ Woolworths {region}: URL Found: {ww_url}")
            else:
                filename = f"Woolworths_{region}.pdf"
                path = await download_file(ww_url, filename)
                if path:
                    try:
                        await rag_engine.delete_documents_by_file(filename)
                        count = await rag_engine.ingest_documents(UPLOAD_DIR, specific_file=filename)
                        summary.append(f"✅ Woolworths {region}: {count} chunks")
                        total_ingested += count
                        os.remove(path)
                    except Exception as e:
                        summary.append(f"❌ Woolworths {region}: Ingestion Error: {e}")
        else:
            summary.append(f"❌ Woolworths {region}: URL Not Found")

    print("\n=== Update Pipeline Finished ===")
    if not dry_run:
        print(f"Total Chunks Ingested: {total_ingested}")
        body = "Continuous Update Summary:\n\n" + "\n".join(summary)
        send_email("Supermarket RAG Daily Update Report", body)
    else:
        print("Dry run summary:")
        for s in summary:
            print(s)

if __name__ == "__main__":
    import sys
    dry_run = "--dry-run" in sys.argv
    test_email = "--test-email" in sys.argv
    
    if test_email:
        print("Testing email configuration...")
        send_email("Test Email from Supermarket RAG", "This is a test email to verify SMTP configuration.")
    else:
        asyncio.run(run_update(dry_run=dry_run))
