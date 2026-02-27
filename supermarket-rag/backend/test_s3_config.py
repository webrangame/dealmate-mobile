"""
Simple S3 configuration test - checks if AWS credentials are set up correctly
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_s3_config():
    """Test S3 configuration"""
    print("=" * 60)
    print("S3 Configuration Check")
    print("=" * 60)
    
    # Check required environment variables
    required_vars = {
        "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
        "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "AWS_REGION": os.getenv("AWS_REGION", "us-east-1"),
        "S3_BUCKET_NAME": os.getenv("S3_BUCKET_NAME"),
    }
    
    optional_vars = {
        "CLOUDFRONT_DOMAIN": os.getenv("CLOUDFRONT_DOMAIN"),
    }
    
    print("\n1. Required Configuration:")
    all_set = True
    for var, value in required_vars.items():
        if value:
            # Mask sensitive values
            if "SECRET" in var or "KEY" in var:
                display_value = value[:8] + "..." if len(value) > 8 else "***"
            else:
                display_value = value
            print(f"   ✓ {var}: {display_value}")
        else:
            print(f"   ❌ {var}: NOT SET")
            all_set = False
    
    print("\n2. Optional Configuration:")
    for var, value in optional_vars.items():
        if value:
            print(f"   ✓ {var}: {value}")
        else:
            print(f"   ℹ️  {var}: Not configured (will use S3 direct URLs)")
    
    if not all_set:
        print("\n❌ Configuration incomplete!")
        print("\nTo enable S3 image storage, add these to your .env file:")
        print("AWS_ACCESS_KEY_ID=your-access-key")
        print("AWS_SECRET_ACCESS_KEY=your-secret-key")
        print("AWS_REGION=us-east-1")
        print("S3_BUCKET_NAME=your-bucket-name")
        print("CLOUDFRONT_DOMAIN=optional-cdn-domain.cloudfront.net")
        return False
    
    # Try to connect to S3
    print("\n3. Testing S3 Connection...")
    try:
        import boto3
        from botocore.exceptions import ClientError
        
        s3_client = boto3.client(
            's3',
            aws_access_key_id=required_vars["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=required_vars["AWS_SECRET_ACCESS_KEY"],
            region_name=required_vars["AWS_REGION"]
        )
        
        # Try to list buckets
        response = s3_client.list_buckets()
        print(f"   ✓ Successfully connected to AWS S3")
        print(f"   ✓ Found {len(response['Buckets'])} bucket(s)")
        
        # Check if our bucket exists
        bucket_name = required_vars["S3_BUCKET_NAME"]
        bucket_exists = any(b['Name'] == bucket_name for b in response['Buckets'])
        
        if bucket_exists:
            print(f"   ✓ Target bucket '{bucket_name}' exists")
        else:
            print(f"   ⚠️  Target bucket '{bucket_name}' not found")
            print(f"   Available buckets:")
            for bucket in response['Buckets']:
                print(f"      - {bucket['Name']}")
            print(f"\n   You may need to create the bucket or update S3_BUCKET_NAME")
        
        return True
        
    except ImportError:
        print(f"   ❌ boto3 not installed. Run: pip install boto3")
        return False
    except ClientError as e:
        print(f"   ❌ AWS Error: {e}")
        print(f"   Check your AWS credentials and permissions")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("\n🔍 S3 Configuration Test\n")
    success = test_s3_config()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ S3 is properly configured!")
        print("\nNext steps:")
        print("1. Ensure your S3 bucket exists (or create it)")
        print("2. Run PDF ingestion to test image upload")
        print("3. Check S3 bucket for uploaded images")
    else:
        print("❌ S3 configuration needs attention")
        print("\nPlease configure AWS credentials in .env file")
    print("=" * 60)
