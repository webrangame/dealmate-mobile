#!/bin/bash

# Quick status check script for LiteLLM App Runner service

SERVICE_ARN="arn:aws:apprunner:us-east-1:724772062824:service/litellm-proxy/b2128e35aa754cffbd7128eedca9ed5d"
SERVICE_URL="swzissb82u.us-east-1.awsapprunner.com"

echo "🔍 Checking LiteLLM Service Status..."
echo ""

# Get service status
STATUS=$(aws apprunner describe-service \
    --service-arn $SERVICE_ARN \
    --region us-east-1 \
    --query 'Service.Status' \
    --output text 2>/dev/null)

echo "📊 Service Status: $STATUS"
echo "🌐 Service URL: https://$SERVICE_URL"
echo ""

if [ "$STATUS" == "RUNNING" ]; then
    echo "✅ Service is RUNNING!"
    echo ""
    echo "🧪 Testing endpoints..."
    echo ""
    
    # Test health
    echo "1. Health Check:"
    curl -s https://$SERVICE_URL/health || echo "   ❌ Health check failed"
    echo ""
    
    # Test root
    echo "2. Root Endpoint:"
    curl -s -I https://$SERVICE_URL/ | head -1 || echo "   ❌ Root endpoint failed"
    echo ""
    
    # Test UI
    echo "3. UI Endpoint:"
    curl -s -I https://$SERVICE_URL/ui | head -1 || echo "   ❌ UI endpoint failed"
    echo ""
    
    echo "✅ Service is ready to use!"
    
elif [ "$STATUS" == "OPERATION_IN_PROGRESS" ]; then
    echo "⏳ Service is still deploying..."
    echo "   This typically takes 5-10 minutes from creation time"
    echo ""
    echo "📝 Check logs:"
    echo "   aws logs tail /aws/apprunner/litellm-proxy/b2128e35aa754cffbd7128eedca9ed5d/application --follow --region us-east-1"
    echo ""
    echo "🔄 Run this script again in a few minutes:"
    echo "   ./check-status.sh"
    
elif [ "$STATUS" == "CREATE_FAILED" ]; then
    echo "❌ Service creation failed!"
    echo ""
    echo "📋 Check operation details:"
    aws apprunner list-operations \
        --service-arn $SERVICE_ARN \
        --region us-east-1 \
        --max-results 1 \
        --query 'OperationSummaryList[0]' \
        --output json
    echo ""
    echo "📝 Check logs for errors:"
    echo "   aws logs tail /aws/apprunner/litellm-proxy/b2128e35aa754cffbd7128eedca9ed5d/service --region us-east-1"
    
else
    echo "⚠️  Unknown status: $STATUS"
fi
