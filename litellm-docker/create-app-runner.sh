#!/bin/bash

# Script to help create AWS App Runner service for LiteLLM
# This provides the exact commands and configuration needed

set -e

echo "🚀 LiteLLM AWS App Runner Setup"
echo "================================"
echo ""

AWS_REGION=${AWS_REGION:-us-east-1}
ECR_REPO_NAME="litellm-proxy"
SERVICE_NAME="litellm-proxy"

# Get AWS account ID and ECR URI
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REPO_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}"

echo "✅ AWS Account: ${AWS_ACCOUNT_ID}"
echo "✅ ECR Repository: ${ECR_REPO_URI}"
echo ""

# Check if image exists
echo "📦 Checking if Docker image exists in ECR..."
if aws ecr describe-images --repository-name $ECR_REPO_NAME --image-ids imageTag=latest --region $AWS_REGION &> /dev/null; then
    echo "✅ Image found in ECR"
else
    echo "⚠️  Image not found. Please run ./deploy-to-aws.sh first"
    exit 1
fi

echo ""
echo "📝 App Runner Configuration:"
echo "============================"
echo ""
echo "1. Go to: https://console.aws.amazon.com/apprunner"
echo ""
echo "2. Click 'Create service'"
echo ""
echo "3. Source Configuration:"
echo "   - Source: Container registry"
echo "   - Provider: Amazon ECR"
echo "   - Container image URI: ${ECR_REPO_URI}:latest"
echo "   - Deployment trigger: Automatic"
echo ""
echo "4. Service Settings:"
echo "   - Service name: ${SERVICE_NAME}"
echo "   - Virtual CPU: 0.5 vCPU"
echo "   - Memory: 1 GB"
echo "   - Port: 4000"
echo ""
echo "5. Environment Variables (add these):"
echo "   LITELLM_MASTER_KEY=sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642"
echo "   DATABASE_URL=postgresql://postgres:it371Ananda@agent-marketplace-db.cmt466aga8u0.us-east-1.rds.amazonaws.com:5432/litellm_db?sslmode=require"
echo "   GOOGLE_API_KEY=AIzaSyDDSkUUl7gmWbqxVaE9iVB2KQzLh9SpwV8"
echo "   STORE_MODEL_IN_DB=True"
echo "   LITELLM_LOG=INFO"
echo "   CONFIG=/app/config.yaml"
echo ""
echo "6. Click 'Create & Deploy'"
echo ""
echo "✅ Your LiteLLM will be live in ~5 minutes!"
echo ""
echo "📚 After deployment:"
echo "   - Get your App Runner URL from the console"
echo "   - Update LITELLM_API_URL in your Next.js app"
echo "   - Test: curl https://your-app-runner-url/health"
echo ""
