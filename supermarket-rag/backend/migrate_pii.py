import os
import psycopg2
from sqlalchemy import make_url
from dotenv import load_dotenv
from rag_engine import KMSEncryptor
import datetime

load_dotenv()

def migrate_users():
    print("--- Starting PII Encryption Migration ---")
    
    db_url = os.getenv("DATABASE_URL")
    kms_key_id = os.getenv("AWS_KMS_KEY_ID")
    
    if not db_url or not kms_key_id:
        print("❌ Error: DATABASE_URL or AWS_KMS_KEY_ID not set")
        return

    encryptor = KMSEncryptor(kms_key_id, os.getenv("AWS_REGION", "us-east-1"))
    
    try:
        url = make_url(db_url)
        conn = psycopg2.connect(
            host=url.host,
            port=url.port,
            database=url.database,
            user=url.username,
            password=url.password,
            sslmode='require'
        )
        conn.autocommit = False # Use transactions
        cur = conn.cursor()
        
        # 1. Fetch ALL users
        cur.execute("SELECT id, email, name, phone_number, billing_address_line1, billing_address_line2, billing_city, billing_state, billing_postal_code FROM users")
        users = cur.fetchall()
        print(f"Checking {len(users)} users for PII encryption and HASH update (New Salt)...")
        
        for user_id, email, name, phone, addr1, addr2, city, state, zip_code in users:
            updates = {}
            
            # Helper: decrypt if encrypted
            def get_plaintext(val):
                if val and "::" in val:
                    try:
                        return encryptor.decrypt(val)
                    except:
                        return val
                return val

            # Always update email_hash with NEW salt
            plain_email = get_plaintext(email)
            if plain_email:
                updates["email_hash"] = encryptor.hash_pii(plain_email)

            # Check and Encrypt each field if not encrypted
            if email and "::" not in email:
                updates["email"] = encryptor.encrypt(email.lower().strip())
            
            if name and "::" not in name:
                updates["name"] = encryptor.encrypt(name.strip())

            if phone and "::" not in phone:
                updates["phone_number"] = encryptor.encrypt(phone.strip())

            if addr1 and "::" not in addr1:
                updates["billing_address_line1"] = encryptor.encrypt(addr1.strip())
            
            if addr2 and "::" not in addr2:
                updates["billing_address_line2"] = encryptor.encrypt(addr2.strip())
            
            if city and "::" not in city:
                updates["billing_city"] = encryptor.encrypt(city.strip())
            
            if state and "::" not in state:
                updates["billing_state"] = encryptor.encrypt(state.strip())
            
            if zip_code and "::" not in zip_code:
                updates["billing_postal_code"] = encryptor.encrypt(zip_code.strip())

            if updates:
                print(f"Updating User ID {user_id} ({len(updates)} fields)...")
                updates["pii_version"] = 1
                updates["updated_at"] = datetime.datetime.now()
                
                set_clause = ", ".join([f"{k} = %s" for k in updates.keys()])
                params = list(updates.values()) + [user_id]
                
                cur.execute(f"UPDATE users SET {set_clause} WHERE id = %s", tuple(params))

        conn.commit()
        print("--- Migration Finished Successfully ---")
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Migration Failed: {e}")

if __name__ == "__main__":
    migrate_users()
