import os
import boto3
from dotenv import load_dotenv

def test_kms():
    load_dotenv()
    
    region = os.getenv('AWS_REGION', 'us-east-1')
    key_id = os.getenv('AWS_KMS_KEY_ID')
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    print(f"--- Diagnostic Report ---")
    print(f"Region: {region}")
    print(f"Key ID: {key_id}")
    print(f"Access Key: {access_key[:5]}...{access_key[-4:] if access_key else ''}")
    print(f"-------------------------")
    
    try:
        from botocore.config import Config
        config = Config(
            connect_timeout=5,
            read_timeout=5,
            retries={'max_attempts': 0}
        )
        session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        kms = session.client('kms', config=config)
        
        print(f"Testing KMS GenerateDataKey for: {key_id}")
        resp = kms.generate_data_key(KeyId=key_id, KeySpec='AES_256')
        print("✅ SUCCESS: KMS GenerateDataKey authorized.")
        print(f"KMS Key ARN: {resp.get('KeyId')}")
        
    except Exception as e:
        print(f"❌ FAILURE: KMS operation failed.")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")

if __name__ == "__main__":
    test_kms()
