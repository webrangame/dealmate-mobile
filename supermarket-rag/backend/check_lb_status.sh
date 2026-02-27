#!/bin/bash
# Consolidated script to check AWS App Runner Load Balancer and Service Status

SERVICE_ARN="arn:aws:apprunner:us-east-1:582604091763:service/supermarket-rag-api/"
PUBLIC_URL="https://xfukqtd5pc.us-east-1.awsapprunner.com"
REGION="us-east-1"

echo "=========================================="
echo "Backend Load Balancer & Service Check"
echo "=========================================="
echo ""

echo "STEP 1: Public Health Check (External Load Balancer)"
echo "------------------------------------------"
HEALTH_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$PUBLIC_URL/health")

if [ "$HEALTH_RESPONSE" -eq 200 ]; then
    echo "✅ Success: Health endpoint returned 200 OK"
    echo "   URL: $PUBLIC_URL/health"
else
    echo "❌ ERROR: Health endpoint returned HTTP $HEALTH_RESPONSE"
    echo "   Check if the service is running and the health check path is correct."
fi
echo ""

echo "STEP 2: AWS App Runner Service Status"
echo "------------------------------------------"
if ! command -v aws &> /dev/null; then
    echo "⚠️  AWS CLI not found. Skipping service description."
    echo "   Manual check: https://console.aws.amazon.com/apprunner/home?region=$REGION#/services/supermarket-rag-api/status"
else
    STATUS=$(aws apprunner describe-service --service-arn "$SERVICE_ARN" --region "$REGION" --query 'Service.Status' --output text 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        echo "✅ Service Status (AWS): $STATUS"
        if [ "$STATUS" != "RUNNING" ]; then
            echo "   ⚠️  Warning: Service is not in 'RUNNING' state."
        fi
    else
        echo "❌ ERROR: Could not fetch service status. Check AWS credentials and ARN."
    fi
fi
echo ""

echo "STEP 3: Guidance for Deep Checks"
echo "------------------------------------------"
echo "If the above checks fail, verify the following in AWS Console:"
echo "1. Service Event Logs: Look for 'Health check failed' messages."
echo "2. Port Mapping: Ensure App Runner is listening on port 8000."
echo "3. CloudWatch Metrics: Check 'RequestCount' and '4xx/5xxErrorCount'."
echo "   URL: https://console.aws.amazon.com/cloudwatch/home?region=$REGION#metricsV2:graph=~();query=~'AWS*2fAppRunner*20Service"
echo ""
echo "=========================================="
