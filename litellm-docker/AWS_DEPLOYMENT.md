# Deploy LiteLLM to AWS - Complete Guide

## 🎯 Best Options for LiteLLM on AWS

### Option 1: AWS ECS Fargate (Recommended) ⭐

**Best for**: Production LiteLLM deployments, auto-scaling, no server management

**Pros**:
- ✅ No server management (Fargate)
- ✅ Auto-scaling based on demand
- ✅ Load balancing included
- ✅ Automatic HTTPS with ALB
- ✅ Works with existing Docker setup
- ✅ Easy to update/deploy
- ✅ Cost-effective for production

**Cons**:
- ⚠️ Requires some AWS knowledge
- ⚠️ Setup takes ~30-60 minutes

**Cost**: ~$30-100/month (depending on traffic)

---

### Option 2: AWS App Runner

**Best for**: Simple container deployment, quick setup

**Pros**:
- ✅ Very easy setup (~15 minutes)
- ✅ Auto-scaling
- ✅ Built-in HTTPS
- ✅ Simple pricing
- ✅ Works with Docker

**Cons**:
- ⚠️ Less control than ECS
- ⚠️ Limited customization

**Cost**: ~$25-80/month

---

### Option 3: EC2 Instance with Docker

**Best for**: Development, testing, cost-effective for small scale

**Pros**:
- ✅ Full control
- ✅ Predictable pricing
- ✅ Easy to debug
- ✅ Good for development/testing

**Cons**:
- ⚠️ Manual scaling
- ⚠️ Server management required
- ⚠️ SSL/HTTPS setup needed

**Cost**: ~$10-50/month (t2.medium/t3.medium)

---

## 🏆 Recommended: AWS ECS Fargate

For production LiteLLM deployment, **ECS Fargate is the best choice**:

1. ✅ **No server management** - Fully managed containers
2. ✅ **Auto-scaling** - Handles traffic spikes automatically
3. ✅ **Load balancing** - Distributes traffic across instances
4. ✅ **HTTPS/SSL** - Automatic with Application Load Balancer
5. ✅ **Easy updates** - Deploy new versions with one click
6. ✅ **Production-ready** - Used by many AWS customers

---

## 🚀 Quick Start: Deploy LiteLLM to ECS Fargate

### Prerequisites

1. AWS Account
2. AWS CLI installed and configured
3. Docker installed locally
4. LiteLLM Docker setup (already done ✅)

### Step 1: Create ECR Repository

ECR (Elastic Container Registry) stores your Docker images.

```bash
# Set your AWS region
export AWS_REGION=us-east-1

# Create ECR repository
aws ecr create-repository \
  --repository-name litellm-proxy \
  --region $AWS_REGION

# Get login token
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.$AWS_REGION.amazonaws.com
```

**Note**: Replace `<ACCOUNT_ID>` with your AWS account ID (12 digits).

### Step 2: Build and Push Docker Image

```bash
cd /home/ranga/code/pragith/whatssapp-chat/litellm-docker

# Build the image
docker build -t litellm-proxy:latest .

# Tag for ECR
docker tag litellm-proxy:latest <ACCOUNT_ID>.dkr.ecr.$AWS_REGION.amazonaws.com/litellm-proxy:latest

# Push to ECR
docker push <ACCOUNT_ID>.dkr.ecr.$AWS_REGION.amazonaws.com/litellm-proxy:latest
```

### Step 3: Create ECS Cluster

```bash
# Create cluster
aws ecs create-cluster --cluster-name litellm-cluster --region $AWS_REGION
```

### Step 4: Create Task Definition

Create `task-definition.json`:

```json
{
  "family": "litellm-proxy",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "litellm-proxy",
      "image": "<ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/litellm-proxy:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 4000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "LITELLM_MASTER_KEY",
          "value": "sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642"
        },
        {
          "name": "DATABASE_URL",
          "value": "postgresql://postgres:it371Ananda@agent-marketplace-db.cmt466aga8u0.us-east-1.rds.amazonaws.com:5432/litellm_db?sslmode=require"
        },
        {
          "name": "LITELLM_LOG",
          "value": "INFO"
        },
        {
          "name": "UI_PASSWORD",
          "value": "your-ui-password"
        },
        {
          "name": "GOOGLE_API_KEY",
          "value": "AIzaSyDDSkUUl7gmWbqxVaE9iVB2KQzLh9SpwV8"
        },
        {
          "name": "STORE_MODEL_IN_DB",
          "value": "True"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/litellm-proxy",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

Register the task definition:

```bash
aws ecs register-task-definition \
  --cli-input-json file://task-definition.json \
  --region $AWS_REGION
```

### Step 5: Create CloudWatch Log Group

```bash
aws logs create-log-group \
  --log-group-name /ecs/litellm-proxy \
  --region $AWS_REGION
```

### Step 6: Create VPC and Networking (if needed)

If you don't have a VPC, create one:

```bash
# Get default VPC ID
export VPC_ID=$(aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --query "Vpcs[0].VpcId" --output text --region $AWS_REGION)

# Get subnet IDs
export SUBNET_IDS=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --query "Subnets[*].SubnetId" --output text --region $AWS_REGION | tr '\t' ',')

# Get security group (or create new one)
export SECURITY_GROUP_ID=$(aws ec2 describe-security-groups --filters "Name=vpc-id,Values=$VPC_ID" "Name=group-name,Values=default" --query "SecurityGroups[0].GroupId" --output text --region $AWS_REGION)
```

### Step 7: Create ECS Service

```bash
aws ecs create-service \
  --cluster litellm-cluster \
  --service-name litellm-service \
  --task-definition litellm-proxy \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[$SUBNET_IDS],assignPublicIp=ENABLED,securityGroups=[$SECURITY_GROUP_ID]}" \
  --region $AWS_REGION
```

### Step 8: Create Application Load Balancer (ALB)

For HTTPS and public access:

```bash
# Create ALB
aws elbv2 create-load-balancer \
  --name litellm-alb \
  --subnets $SUBNET_IDS \
  --security-groups $SECURITY_GROUP_ID \
  --region $AWS_REGION

# Get ALB ARN (save this)
export ALB_ARN=$(aws elbv2 describe-load-balancers --names litellm-alb --query "LoadBalancers[0].LoadBalancerArn" --output text --region $AWS_REGION)

# Create target group
aws elbv2 create-target-group \
  --name litellm-targets \
  --protocol HTTP \
  --port 4000 \
  --vpc-id $VPC_ID \
  --target-type ip \
  --health-check-path /health \
  --region $AWS_REGION

# Get target group ARN
export TARGET_GROUP_ARN=$(aws elbv2 describe-target-groups --names litellm-targets --query "TargetGroups[0].TargetGroupArn" --output text --region $AWS_REGION)

# Create listener (HTTP)
aws elbv2 create-listener \
  --load-balancer-arn $ALB_ARN \
  --protocol HTTP \
  --port 80 \
  --default-actions Type=forward,TargetGroupArn=$TARGET_GROUP_ARN \
  --region $AWS_REGION
```

### Step 9: Update ECS Service to Use ALB

```bash
aws ecs update-service \
  --cluster litellm-cluster \
  --service litellm-service \
  --load-balancers "targetGroupArn=$TARGET_GROUP_ARN,containerName=litellm-proxy,containerPort=4000" \
  --region $AWS_REGION
```

### Step 10: Get Your LiteLLM URL

```bash
# Get ALB DNS name
aws elbv2 describe-load-balancers \
  --names litellm-alb \
  --query "LoadBalancers[0].DNSName" \
  --output text \
  --region $AWS_REGION
```

Your LiteLLM will be available at: `http://<ALB-DNS-NAME>`

---

## 🔒 Add HTTPS/SSL (Optional but Recommended)

### Using AWS Certificate Manager (ACM)

1. **Request Certificate**:
   ```bash
   aws acm request-certificate \
     --domain-name litellm.yourdomain.com \
     --validation-method DNS \
     --region us-east-1
   ```

2. **Validate Certificate** (add DNS records)

3. **Create HTTPS Listener**:
   ```bash
   aws elbv2 create-listener \
     --load-balancer-arn $ALB_ARN \
     --protocol HTTPS \
     --port 443 \
     --certificates CertificateArn=<CERTIFICATE_ARN> \
     --default-actions Type=forward,TargetGroupArn=$TARGET_GROUP_ARN \
     --region $AWS_REGION
   ```

---

## 📊 Alternative: AWS App Runner (Simpler)

### Quick Setup with App Runner

1. **Push to ECR** (same as Step 2 above)

2. **Create App Runner Service**:
   - Go to AWS App Runner Console
   - Click "Create service"
   - Select "Container registry" → ECR
   - Choose your image
   - Configure:
     - CPU: 0.5 vCPU
     - Memory: 1 GB
     - Port: 4000
   - Add environment variables
   - Deploy!

**Time**: ~15 minutes  
**Cost**: ~$25-80/month

---

## 💰 Cost Comparison

| Option | Monthly Cost | Setup Time | Best For |
|--------|-------------|------------|----------|
| **ECS Fargate** | $30-100 | 30-60 min | Production |
| **App Runner** | $25-80 | 15 min | Simple deployment |
| **EC2** | $10-50 | 20 min | Dev/Testing |

---

## 🔄 Updating LiteLLM

### Update Docker Image

```bash
cd /home/ranga/code/pragith/whatssapp-chat/litellm-docker

# Build new image
docker build -t litellm-proxy:latest .

# Tag and push
docker tag litellm-proxy:latest <ACCOUNT_ID>.dkr.ecr.$AWS_REGION.amazonaws.com/litellm-proxy:latest
docker push <ACCOUNT_ID>.dkr.ecr.$AWS_REGION.amazonaws.com/litellm-proxy:latest

# Force new deployment
aws ecs update-service \
  --cluster litellm-cluster \
  --service litellm-service \
  --force-new-deployment \
  --region $AWS_REGION
```

---

## 📝 Environment Variables

Make sure to set these in your task definition or App Runner:

- `LITELLM_MASTER_KEY` - Your master key
- `DATABASE_URL` - PostgreSQL connection string
- `GOOGLE_API_KEY` - Google API key
- `UI_PASSWORD` - UI password (optional)
- `STORE_MODEL_IN_DB` - "True" to store models in DB
- `LITELLM_LOG` - Log level (INFO, DEBUG, etc.)

---

## 🆘 Troubleshooting

### Check Service Status

```bash
aws ecs describe-services \
  --cluster litellm-cluster \
  --services litellm-service \
  --region $AWS_REGION
```

### View Logs

```bash
aws logs tail /ecs/litellm-proxy --follow --region $AWS_REGION
```

### Check Task Status

```bash
aws ecs list-tasks \
  --cluster litellm-cluster \
  --service-name litellm-service \
  --region $AWS_REGION
```

---

## 🚀 Quick Deploy Script

I'll create an automated deployment script for you!

See: `deploy-to-aws.sh` (coming next)

---

## 📚 Next Steps

1. ✅ Choose deployment method (ECS Fargate recommended)
2. ✅ Create ECR repository
3. ✅ Build and push Docker image
4. ✅ Create ECS cluster and service
5. ✅ Configure ALB for public access
6. ✅ Update `LITELLM_API_URL` in your Next.js app

---

## 🔗 Useful Links

- [ECS Fargate Docs](https://docs.aws.amazon.com/ecs/latest/developerguide/AWS_Fargate.html)
- [App Runner Docs](https://docs.aws.amazon.com/apprunner/)
- [ECR Docs](https://docs.aws.amazon.com/ecr/)
