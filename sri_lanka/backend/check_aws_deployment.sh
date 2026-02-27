#!/bin/bash
# Quick AWS deployment checker and production tester

echo "=========================================="
echo "AWS DEPLOYMENT & PRODUCTION TEST"
echo "=========================================="
echo ""

# Check if AWS CLI is configured
if ! command -v aws &> /dev/null; then
    echo "⚠️  AWS CLI not found. Install with: pip install awscli"
    echo ""
    echo "Manual check:"
    echo "1. Go to: https://console.aws.amazon.com/apprunner"
    echo "2. Check service status (should show 'Running' with latest deployment)"
    echo ""
else
    echo "Checking AWS App Runner deployment status..."
    echo ""
    # Note: Replace with your actual service ARN
    # aws apprunner describe-service --service-arn YOUR_ARN --region us-east-1 --query 'Service.Status'
fi

echo "=========================================="
echo "STEP 1: Verify API is responding"
echo "=========================================="
echo ""
echo "Testing health endpoint..."
curl -s https://xfukqtd5pc.us-east-1.awsapprunner.com/health || echo "❌ API not responding"
echo ""
echo ""

echo "=========================================="
echo "STEP 2: Trigger Production Ingestion"
echo "=========================================="
echo ""
echo "⚠️  You need to manually run this command with your ADMIN_API_KEY:"
echo ""
echo "curl -X POST https://xfukqtd5pc.us-east-1.awsapprunner.com/api/admin/ingest \\"
echo "  -H \"X-Admin-Key: YOUR_ADMIN_KEY\" \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -v"
echo ""
echo "This will download the latest PDFs and ingest them (takes 3-5 minutes)"
echo ""
echo ""

echo "=========================================="
echo "STEP 3: Run 20x20 Test Suite"
echo "=========================================="
echo ""
echo "After ingestion completes, run:"
echo "  python3 test_20x20_live.py"
echo ""
echo "Expected: 40/40 success, 95%+ multi-shop coverage"
echo ""
echo "=========================================="
