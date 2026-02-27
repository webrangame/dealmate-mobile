#!/bin/bash

# LiteLLM AWS Deployment Script
# This script automates deploying LiteLLM to AWS ECS Fargate

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 LiteLLM AWS Deployment Script${NC}"
echo "=================================="
echo ""

# Configuration
AWS_REGION=${AWS_REGION:-us-east-1}
ECR_REPO_NAME="litellm-proxy"
CLUSTER_NAME="litellm-cluster"
SERVICE_NAME="litellm-service"
IMAGE_TAG="latest"

# Check prerequisites
echo -e "${YELLOW}📋 Checking prerequisites...${NC}"

if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI not found. Please install it first.${NC}"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Please install it first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"
echo ""

# Get AWS account ID
echo -e "${YELLOW}🔍 Getting AWS account ID...${NC}"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REPO_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}"

echo -e "${GREEN}✅ Account ID: ${AWS_ACCOUNT_ID}${NC}"
echo -e "${GREEN}✅ ECR URI: ${ECR_REPO_URI}${NC}"
echo ""

# Step 1: Create ECR repository
echo -e "${YELLOW}📦 Step 1: Creating ECR repository...${NC}"
if aws ecr describe-repositories --repository-names $ECR_REPO_NAME --region $AWS_REGION &> /dev/null; then
    echo -e "${GREEN}✅ Repository already exists${NC}"
else
    aws ecr create-repository --repository-name $ECR_REPO_NAME --region $AWS_REGION
    echo -e "${GREEN}✅ Repository created${NC}"
fi
echo ""

# Step 2: Login to ECR
echo -e "${YELLOW}🔐 Step 2: Logging in to ECR...${NC}"
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO_URI
echo -e "${GREEN}✅ Logged in${NC}"
echo ""

# Step 3: Build Docker image
echo -e "${YELLOW}🔨 Step 3: Building Docker image...${NC}"
docker build -t $ECR_REPO_NAME:$IMAGE_TAG .
echo -e "${GREEN}✅ Image built${NC}"
echo ""

# Step 4: Tag image
echo -e "${YELLOW}🏷️  Step 4: Tagging image...${NC}"
docker tag $ECR_REPO_NAME:$IMAGE_TAG $ECR_REPO_URI:$IMAGE_TAG
echo -e "${GREEN}✅ Image tagged${NC}"
echo ""

# Step 5: Push to ECR
echo -e "${YELLOW}📤 Step 5: Pushing image to ECR...${NC}"
docker push $ECR_REPO_URI:$IMAGE_TAG
echo -e "${GREEN}✅ Image pushed${NC}"
echo ""

# Step 6: Create CloudWatch log group
echo -e "${YELLOW}📊 Step 6: Creating CloudWatch log group...${NC}"
if aws logs describe-log-groups --log-group-name-prefix /ecs/litellm-proxy --region $AWS_REGION --query 'logGroups[0].logGroupName' --output text &> /dev/null; then
    echo -e "${GREEN}✅ Log group already exists${NC}"
else
    aws logs create-log-group --log-group-name /ecs/litellm-proxy --region $AWS_REGION
    echo -e "${GREEN}✅ Log group created${NC}"
fi
echo ""

# Step 7: Create ECS cluster
echo -e "${YELLOW}🏗️  Step 7: Creating ECS cluster...${NC}"
if aws ecs describe-clusters --clusters $CLUSTER_NAME --region $AWS_REGION --query 'clusters[0].status' --output text 2>/dev/null | grep -q ACTIVE; then
    echo -e "${GREEN}✅ Cluster already exists${NC}"
else
    aws ecs create-cluster --cluster-name $CLUSTER_NAME --region $AWS_REGION
    echo -e "${GREEN}✅ Cluster created${NC}"
fi
echo ""

echo -e "${GREEN}✅ Docker image pushed successfully!${NC}"
echo ""
echo -e "${YELLOW}📝 Next steps:${NC}"
echo "  1. Create task definition (see AWS_DEPLOYMENT.md)"
echo "  2. Create ECS service"
echo "  3. Configure Application Load Balancer"
echo ""
echo -e "${GREEN}📚 Full instructions: See AWS_DEPLOYMENT.md${NC}"
echo ""
echo -e "${GREEN}🎉 Deployment preparation complete!${NC}"
