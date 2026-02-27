#!/bin/bash
# Create App Runner service with proper IAM role

set -e

AWS_REGION="us-east-1"
SERVICE_NAME="litellm-proxy"
ECR_REPO_URI="724772062824.dkr.ecr.us-east-1.amazonaws.com/litellm-proxy:latest"

echo "🚀 Creating App Runner Service..."
echo ""

# Create IAM role for App Runner to access ECR
ROLE_NAME="AppRunnerECRAccessRole"

echo "📝 Creating IAM role for ECR access..."

# Check if role exists
if aws iam get-role --role-name $ROLE_NAME 2>/dev/null; then
    echo "✅ Role already exists"
    ROLE_ARN=$(aws iam get-role --role-name $ROLE_NAME --query 'Role.Arn' --output text)
else
    # Create trust policy
    cat > /tmp/trust-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "build.apprunner.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

    # Create role
    aws iam create-role \
        --role-name $ROLE_NAME \
        --assume-role-policy-document file:///tmp/trust-policy.json

    # Attach ECR read policy
    aws iam attach-role-policy \
        --role-name $ROLE_NAME \
        --policy-arn arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess

    ROLE_ARN=$(aws iam get-role --role-name $ROLE_NAME --query 'Role.Arn' --output text)
    echo "✅ Role created: $ROLE_ARN"
fi

# Create service configuration
cat > /tmp/app-runner-config.json << EOF
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
      },
      "EcrAccessRoleArn": "${ROLE_ARN}"
    },
    "AutoDeploymentsEnabled": true
  },
  "InstanceConfiguration": {
    "Cpu": "0.5 vCPU",
    "Memory": "1 GB"
  }
}
EOF

echo "📝 Creating App Runner service..."
aws apprunner create-service \
  --cli-input-json file:///tmp/app-runner-config.json \
  --region $AWS_REGION

echo ""
echo "✅ Service creation initiated!"
echo "⏳ Wait ~5 minutes for deployment..."
