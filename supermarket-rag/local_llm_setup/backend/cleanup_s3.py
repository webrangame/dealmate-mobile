
import asyncio
from rag_engine import RAGEngine
import os

async def main():
    print("=== Supermarket RAG S3 Cleanup Utility ===")
    engine = RAGEngine()
    
    # Enable S3 if credentials are in env (which they should be)
    if engine.s3_bucket:
        engine.s3_enabled = True
        import boto3
        engine.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )
    
    # Run in dry-run mode first to see what would be deleted
    print("\nRunning in DRY-RUN mode...")
    orphans = await engine.cleanup_orphaned_s3_images(dry_run=True)
    
    if not orphans:
        print("No orphaned images found.")
        return

    confirm = input(f"\nProceed to delete {len(orphans)} orphaned objects from S3? (y/N): ")
    if confirm.lower() == 'y':
        print("Deleting orphans...")
        await engine.cleanup_orphaned_s3_images(dry_run=False)
        print("Cleanup complete.")
    else:
        print("Cleanup cancelled.")

if __name__ == "__main__":
    asyncio.run(main())
