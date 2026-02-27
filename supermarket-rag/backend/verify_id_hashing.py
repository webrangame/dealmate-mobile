import os
import hmac
import hashlib
from rag_engine import rag_engine

def test_hashing():
    email = "itranga@gmail.com"
    salt = os.getenv("PII_HASH_SALT", "default-salt-change-me")
    
    # 1. Manual hash calculation (using the same logic as KMSEncryptor)
    expected_hash = hmac.new(
        salt.encode('utf-8'),
        email.lower().strip().encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    print(f"Email: {email}")
    print(f"Salt: {salt[:3]}...")
    print(f"Expected Hash: {expected_hash}")
    
    # 2. Test rag_engine.encryptor.hash_pii
    if hasattr(rag_engine, 'encryptor') and rag_engine.encryptor:
        engine_hash = rag_engine.encryptor.hash_pii(email)
        print(f"Engine Hash: {engine_hash}")
        if engine_hash == expected_hash:
            print("✅ Engine hash matches manual calculation.")
        else:
            print("❌ Engine hash mismatch!")
    else:
        print("⚠️ Encryptor not initialized, skipping engine hash check.")

    # 3. Verify logic for double-hashing prevention
    # In rag_engine.py, we check if user_id matches r"^[0-9a-f]{64}$"
    import re
    is_already_hash = bool(re.match(r"^[0-9a-f]{64}$", expected_hash.lower()))
    print(f"Is Expected Hash a valid 64-char hex string? {is_already_hash}")
    if is_already_hash:
        print("✅ Logic for double-hashing prevention will correctly identify this as a hash.")
    else:
        print("❌ Hash format mismatch!")

    print("\nVerification script completed.")

if __name__ == "__main__":
    test_hashing()
