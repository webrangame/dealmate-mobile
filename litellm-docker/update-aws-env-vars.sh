#!/bin/bash

# Update AWS App Runner service environment variables
# Specifically updates GOOGLE_API_KEY

set -e

SERVICE_ARN="arn:aws:apprunner:us-east-1:724772062824:service/litellm-proxy/b2128e35aa754cffbd7128eedca9ed5d"
AWS_REGION="us-east-1"
GOOGLE_API_KEY="AIzaSyB363hm_J0BoJ_EZ8Da_cg0-EBjItKLsA8"

echo "🔄 Updating AWS App Runner Service Environment Variables"
echo "========================================================"
echo ""
echo "Service ARN: ${SERVICE_ARN}"
echo "Region: ${AWS_REGION}"
echo ""

# Get current service configuration
echo "📥 Fetching current service configuration..."
CURRENT_CONFIG=$(aws apprunner describe-service \
  --service-arn "${SERVICE_ARN}" \
  --region "${AWS_REGION}" \
  --query 'Service.SourceConfiguration' \
  --output json)

# Extract current environment variables
echo "📝 Preparing updated configuration..."

# Get current service configuration to preserve other settings
echo "📥 Fetching current service configuration..."
CURRENT_CONFIG=$(aws apprunner describe-service \
  --service-arn "${SERVICE_ARN}" \
  --region "${AWS_REGION}" \
  --query 'Service.SourceConfiguration' \
  --output json)

# Create update configuration with correct structure
cat > /tmp/update-config.json << EOF
{
  "ImageRepository": {
    "ImageIdentifier": "724772062824.dkr.ecr.us-east-1.amazonaws.com/litellm-proxy:latest",
    "ImageRepositoryType": "ECR",
    "ImageConfiguration": {
      "Port": "4000",
      "RuntimeEnvironmentVariables": {
        "LITELLM_MASTER_KEY": "sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642",
        "DATABASE_URL": "postgresql://postgres:it371Ananda@agent-marketplace-db.cmt466aga8u0.us-east-1.rds.amazonaws.com:5432/litellm_db?sslmode=require",
        "GOOGLE_API_KEY": "${GOOGLE_API_KEY}",
        "STORE_MODEL_IN_DB": "True",
        "LITELLM_LOG": "INFO",
        "CONFIG": "/app/config.yaml"
      }
    }
  },
  "AutoDeploymentsEnabled": true
}
EOF

echo "✅ Configuration prepared"
echo ""
echo "🚀 Updating App Runner service..."
echo ""

# Update the service
aws apprunner update-service \
  --service-arn "${SERVICE_ARN}" \
  --source-configuration file:///tmp/update-config.json \
  --region "${AWS_REGION}" \
  --output json

echo ""
echo "✅ Service update initiated!"
echo ""
echo "⏳ The service will redeploy with updated environment variables"
echo "   This typically takes 5-10 minutes"
echo ""
echo "📋 To check deployment status:"
echo "   aws apprunner describe-service --service-arn ${SERVICE_ARN} --region ${AWS_REGION} --query 'Service.Status' --output text"
echo ""
echo "📊 To view logs:"
echo "   aws logs tail /aws/apprunner/litellm-proxy/b2128e35aa754cffbd7128eedca9ed5d/application --follow --region ${AWS_REGION}"
echo ""
echo "🧪 To test after deployment:"
echo "   curl https://swzissb82u.us-east-1.awsapprunner.com/health"
echo ""
