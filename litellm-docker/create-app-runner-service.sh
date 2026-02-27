#!/bin/bash

# Create AWS App Runner service for LiteLLM
set -e

AWS_REGION=${AWS_REGION:-us-east-1}
ECR_REPO_NAME="litellm-proxy"
SERVICE_NAME="litellm-proxy"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REPO_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}"

echo "🚀 Creating AWS App Runner Service for LiteLLM"
echo "=============================================="
echo ""

# Create service configuration JSON
cat > app-runner-config.json << EOF
{
  "ServiceName": "${SERVICE_NAME}",
  "SourceConfiguration": {
    "ImageRepository": {
      "ImageIdentifier": "${ECR_REPO_URI}:latest",
      "ImageRepositoryType": "ECR",
      "ImageConfiguration": {
        "Port": "4000",
        "RuntimeEnvironmentVariables": {
          "LITELLM_MASTER_KEY": "sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642",
          "DATABASE_URL": "postgresql://postgres:it371Ananda@agent-marketplace-db.cmt466aga8u0.us-east-1.rds.amazonaws.com:5432/litellm_db?sslmode=require",
          "GOOGLE_API_KEY": "AIzaSyB363hm_J0BoJ_EZ8Da_cg0-EBjItKLsA8",
          "STORE_MODEL_IN_DB": "True",
          "LITELLM_LOG": "INFO",
          "CONFIG": "/app/config.yaml"
        }
      }
    },
    "AutoDeploymentsEnabled": true
  },
  "InstanceConfiguration": {
    "Cpu": "0.5 vCPU",
    "Memory": "1 GB"
  }
}
EOF

echo "📝 Service configuration created"
echo ""
echo "Creating App Runner service..."
echo ""

# Create the service
aws apprunner create-service \
  --cli-input-json file://app-runner-config.json \
  --region $AWS_REGION

echo ""
echo "✅ App Runner service creation initiated!"
echo ""
echo "⏳ Service will be available in ~5 minutes"
echo ""
echo "📋 To check status:"
echo "   aws apprunner describe-service --service-arn <SERVICE_ARN> --region $AWS_REGION"
echo ""
echo "🌐 To get service URL:"
echo "   aws apprunner describe-service --service-arn <SERVICE_ARN> --region $AWS_REGION --query 'Service.ServiceUrl' --output text"
echo ""
