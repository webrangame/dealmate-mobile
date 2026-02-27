#!/bin/bash
# Script to rebuild and deploy the supermarket-rag-api backend to AWS ECR

# Exit on error
set -e

REGION="us-east-1"
ACCOUNT_ID="582604091763"
REPO_NAME="supermarket-rag-api"
IMAGE_TAG="latest"
ECR_URL="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com"

echo "Logging in to AWS ECR..."
aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${ECR_URL}

echo "Building Docker image..."
# Backend is in the current directory
docker build -t ${REPO_NAME} .

echo "Tagging image..."
docker tag ${REPO_NAME}:${IMAGE_TAG} ${ECR_URL}/${REPO_NAME}:${IMAGE_TAG}

echo "Pushing image to ECR..."
docker push ${ECR_URL}/${REPO_NAME}:${IMAGE_TAG}

echo "Deployment triggered! AWS App Runner will automatically start the deployment."
echo "You can monitor the status using: aws apprunner list-operations --service-arn arn:aws:apprunner:us-east-1:582604091763:service/supermarket-rag-api/bed1eb2079694639a2530c2e4e6f4624 --region ${REGION}"
