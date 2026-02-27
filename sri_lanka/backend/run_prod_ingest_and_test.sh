#!/bin/bash
# Production Ingestion and Test Runner
# Usage: ./run_prod_ingest_and_test.sh YOUR_ADMIN_API_KEY

ADMIN_KEY="$1"
API_URL="https://xfukqtd5pc.us-east-1.awsapprunner.com"

if [ -z "$ADMIN_KEY" ]; then
    echo "❌ Error: ADMIN_API_KEY required"
    echo ""
    echo "Usage: ./run_prod_ingest_and_test.sh YOUR_ADMIN_API_KEY"
    echo ""
    echo "Or set it in .env file:"
    echo "  echo 'ADMIN_API_KEY=your_key_here' >> .env"
    echo "  python3 run_production_update.py"
    exit 1
fi

echo "=========================================="
echo "STEP 1: Triggering Production Ingestion"
echo "=========================================="
echo ""

curl -X POST "$API_URL/api/admin/ingest" \
  -H "X-Admin-Key: $ADMIN_KEY" \
  -H "Content-Type: application/json" \
  -v

echo ""
echo ""
echo "Waiting 10 seconds for ingestion to settle..."
sleep 10
echo ""

echo "=========================================="
echo "STEP 2: Running 20x20 Live Test"
echo "=========================================="
echo ""

python3 test_20x20_live.py

echo ""
echo "=========================================="
echo "COMPLETE!"
echo "=========================================="
echo "Check test_results_live_20x20.json for detailed results"
