# LiteLLM AWS Deployment - Quick Start

## 🏆 Recommended: AWS ECS Fargate

**Best for production LiteLLM deployments**

### Why ECS Fargate?

✅ **No server management** - Fully managed containers  
✅ **Auto-scaling** - Handles traffic automatically  
✅ **Load balancing** - Distributes traffic  
✅ **HTTPS/SSL** - Automatic with ALB  
✅ **Production-ready** - Used by many AWS customers  
✅ **Easy updates** - Deploy new versions easily  

**Cost**: ~$30-100/month  
**Setup Time**: ~30-60 minutes  

---

## 🚀 Quick Deploy (3 Steps)

### Step 1: Push Docker Image to ECR

```bash
cd /home/ranga/code/pragith/whatssapp-chat/litellm-docker

# Run automated script
./deploy-to-aws.sh
```

This script will:
- ✅ Create ECR repository
- ✅ Build Docker image
- ✅ Push to AWS ECR
- ✅ Create ECS cluster
- ✅ Set up CloudWatch logs

### Step 2: Create Task Definition

Go to AWS Console → ECS → Task Definitions → Create new

**Configuration**:
- **Family**: `litellm-proxy`
- **Launch type**: Fargate
- **CPU**: 0.5 vCPU (512)
- **Memory**: 1 GB (1024)
- **Image**: `<ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/litellm-proxy:latest`
- **Port**: 4000

**Environment Variables**:
```
LITELLM_MASTER_KEY=sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642
DATABASE_URL=postgresql://postgres:it371Ananda@agent-marketplace-db.cmt466aga8u0.us-east-1.rds.amazonaws.com:5432/litellm_db?sslmode=require
GOOGLE_API_KEY=AIzaSyDDSkUUl7gmWbqxVaE9iVB2KQzLh9SpwV8
STORE_MODEL_IN_DB=True
LITELLM_LOG=INFO
UI_PASSWORD=your-password
```

### Step 3: Create ECS Service

1. Go to ECS → Clusters → `litellm-cluster`
2. Click "Create Service"
3. Configure:
   - **Task Definition**: `litellm-proxy`
   - **Service name**: `litellm-service`
   - **Desired tasks**: 1
   - **VPC**: Default VPC
   - **Subnets**: Select all
   - **Security group**: Allow port 4000
   - **Public IP**: Enable

4. Click "Create"

---

## 🌐 Access Your LiteLLM

After deployment:

1. **Get task IP**:
   - Go to ECS → Clusters → `litellm-cluster` → Tasks
   - Click on running task
   - Note the **Public IP**

2. **Access LiteLLM**:
   - API: `http://<PUBLIC_IP>:4000`
   - UI: `http://<PUBLIC_IP>:4000/ui`

---

## 🔒 Add Load Balancer (Recommended)

For production, add an Application Load Balancer:

1. **Create ALB**:
   - Go to EC2 → Load Balancers → Create
   - Type: Application Load Balancer
   - Scheme: Internet-facing
   - Listeners: HTTP:80

2. **Create Target Group**:
   - Protocol: HTTP
   - Port: 4000
   - Health check: `/health`

3. **Register ECS Service**:
   - Update ECS service to use ALB
   - Your LiteLLM will be at: `http://<ALB-DNS-NAME>`

---

## 🔄 Update LiteLLM

```bash
cd /home/ranga/code/pragith/whatssapp-chat/litellm-docker

# Rebuild and push
./deploy-to-aws.sh

# Force new deployment
aws ecs update-service \
  --cluster litellm-cluster \
  --service litellm-service \
  --force-new-deployment \
  --region us-east-1
```

---

## 📊 Alternative: AWS App Runner (Simpler)

**Setup Time**: ~15 minutes  
**Cost**: ~$25-80/month  

1. **Push to ECR** (same as Step 1 above)

2. **Create App Runner Service**:
   - Go to AWS App Runner Console
   - Click "Create service"
   - Select "Container registry" → ECR
   - Choose: `litellm-proxy:latest`
   - Configure:
     - CPU: 0.5 vCPU
     - Memory: 1 GB
     - Port: 4000
   - Add environment variables
   - Deploy!

**Done!** Your LiteLLM will be live in ~5 minutes.

---

## 💰 Cost Comparison

| Option | Monthly Cost | Setup Time | Best For |
|--------|-------------|------------|----------|
| **ECS Fargate** | $30-100 | 30-60 min | Production ⭐ |
| **App Runner** | $25-80 | 15 min | Simple deployment |
| **EC2** | $10-50 | 20 min | Dev/Testing |

---

## 📝 Update Your Next.js App

After deployment, update your environment variables:

```bash
# In Vercel or your deployment platform
LITELLM_API_URL=http://<ALB-DNS-NAME>  # or <PUBLIC_IP>:4000
LITELLM_API_KEY=sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642
```

---

## 🆘 Troubleshooting

### Check Service Status
```bash
aws ecs describe-services \
  --cluster litellm-cluster \
  --services litellm-service \
  --region us-east-1
```

### View Logs
```bash
aws logs tail /ecs/litellm-proxy --follow --region us-east-1
```

### Check Tasks
```bash
aws ecs list-tasks \
  --cluster litellm-cluster \
  --service-name litellm-service \
  --region us-east-1
```

---

## 📚 Full Guide

For detailed instructions, see: **AWS_DEPLOYMENT.md**

---

## ✅ Checklist

- [ ] AWS CLI installed and configured
- [ ] Docker installed
- [ ] ECR repository created
- [ ] Docker image pushed
- [ ] ECS cluster created
- [ ] Task definition created
- [ ] ECS service running
- [ ] Load balancer configured (optional)
- [ ] Environment variables updated in Next.js app
- [ ] LiteLLM accessible and working

---

## 🎉 You're Done!

Your LiteLLM is now running on AWS! 🚀
