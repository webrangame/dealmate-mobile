#!/bin/bash

# Rebuild and redeploy LiteLLM Docker image with updated config.yaml
# This ensures the config uses environment variables instead of hardcoded keys

set -e

AWS_REGION=${AWS_REGION:-us-east-1}
ECR_REPO_NAME="litellm-proxy"
IMAGE_TAG="latest"

echo "🔄 Rebuilding and Redeploying LiteLLM"
echo "======================================"
echo ""

# Get AWS account ID
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REPO_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}"

echo "📦 Step 1: Building Docker image with updated config.yaml..."
docker build -t ${ECR_REPO_NAME}:${IMAGE_TAG} .
echo "✅ Image built"
echo ""

echo "🔐 Step 2: Logging in to ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO_URI}
echo "✅ Logged in"
echo ""

echo "🏷️  Step 3: Tagging image..."
docker tag ${ECR_REPO_NAME}:${IMAGE_TAG} ${ECR_REPO_URI}:${IMAGE_TAG}
echo "✅ Image tagged"
echo ""

echo "📤 Step 4: Pushing image to ECR..."
docker push ${ECR_REPO_URI}:${IMAGE_TAG}
echo "✅ Image pushed"
echo ""

echo "✅ Docker image rebuilt and pushed successfully!"
echo ""
echo "⏳ AWS App Runner will automatically detect the new image and redeploy"
echo "   This typically takes 5-10 minutes"
echo ""
echo "📋 To check deployment status:"
echo "   aws apprunner describe-service --service-arn arn:aws:apprunner:us-east-1:724772062824:service/litellm-proxy/b2128e35aa754cffbd7128eedca9ed5d --region us-east-1 --query 'Service.Status' --output text"
echo ""
echo "🧪 To test after deployment:"
echo "   curl https://swzissb82u.us-east-1.awsapprunner.com/health"
echo ""
