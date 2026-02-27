import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "api@niyogen.com")
SMTP_PASS = os.getenv("SMTP_PASS", "sicnznjbiswbasqx")
SMTP_FROM = os.getenv("SMTP_FROM_EMAIL", "api@niyogen.com")
TO_EMAIL = "itranga@gmail.com"

def send_test_email():
    print(f"Testing email to {TO_EMAIL}...")
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_FROM
        msg['To'] = TO_EMAIL
        msg['Subject'] = "Supermarket RAG - Verification Email"
        msg.attach(MIMEText("This is a verification email to confirm you will receive daily updates.", 'plain'))

        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_FROM, TO_EMAIL, msg.as_string())
        server.quit()
        print("✓ Test email sent successfully via Gmail SMTP!")
        return True
    except Exception as e:
        print(f"✗ Gmail SMTP failed: {e}")
        return False

if __name__ == "__main__":
    send_test_email()
