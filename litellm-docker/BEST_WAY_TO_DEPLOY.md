# Best Way to Deploy LiteLLM to AWS

## 🏆 Recommended: AWS App Runner (Simplest & Fastest)

**Why App Runner is the best choice:**
- ✅ **15 minutes setup** - Fastest deployment
- ✅ **Fully managed** - No server management needed
- ✅ **Auto-scaling** - Handles traffic automatically
- ✅ **HTTPS included** - Automatic SSL certificate
- ✅ **Simple pricing** - ~$25-80/month
- ✅ **Easy updates** - Just push new image

---

## 🚀 Quick Deploy (3 Simple Steps)

### Step 1: Push Docker Image to ECR

```bash
cd /home/ranga/code/pragith/whatssapp-chat/litellm-docker

# Run this script (it does everything automatically)
./deploy-to-aws.sh
```

This will:
- Create ECR repository
- Build Docker image
- Push to AWS ECR
- Set up CloudWatch logs

### Step 2: Create App Runner Service (5 minutes)

1. **Go to AWS Console**:
   - https://console.aws.amazon.com/apprunner
   - Click "Create service"

2. **Select Source**:
   - Choose "Container registry"
   - Select "Amazon ECR"
   - Choose your repository: `litellm-proxy`
   - Image tag: `latest`

3. **Configure Service**:
   - **Service name**: `litellm-proxy`
   - **Virtual CPU**: 0.5 vCPU
   - **Memory**: 1 GB
   - **Port**: `4000`

4. **Add Environment Variables**:
   ```
   LITELLM_MASTER_KEY=sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642
   DATABASE_URL=postgresql://postgres:it371Ananda@agent-marketplace-db.cmt466aga8u0.us-east-1.rds.amazonaws.com:5432/litellm_db?sslmode=require
   GOOGLE_API_KEY=AIzaSyDDSkUUl7gmWbqxVaE9iVB2KQzLh9SpwV8
   STORE_MODEL_IN_DB=True
   LITELLM_LOG=INFO
   CONFIG=/app/config.yaml
   ```

5. **Click "Create & Deploy"**

**Done!** Your LiteLLM will be live in ~5 minutes at:
`https://xxxxx.us-east-1.awsapprunner.com`

---

## 📊 Comparison: App Runner vs ECS

| Feature | App Runner ⭐ | ECS Fargate |
|---------|--------------|-------------|
| **Setup Time** | 15 min | 30-60 min |
| **Complexity** | Very Simple | Moderate |
| **Auto-scaling** | ✅ Yes | ✅ Yes |
| **HTTPS/SSL** | ✅ Automatic | ⚠️ Manual (ALB) |
| **Cost** | $25-80/mo | $30-100/mo |
| **Best For** | Quick deployment | Full control |

**Winner: App Runner** - It's simpler and faster! 🏆

---

## 🔄 Alternative: ECS Fargate (If You Need More Control)

If you need more control over networking, load balancing, or custom configurations, use ECS Fargate.

**See**: `AWS_DEPLOYMENT.md` for detailed ECS setup

---

## 💰 Cost Estimate

**App Runner**:
- Base: ~$0.007 per vCPU-hour
- Memory: ~$0.0008 per GB-hour
- **Total**: ~$25-80/month (depending on traffic)

**ECS Fargate**:
- Base: ~$0.04 per vCPU-hour
- Memory: ~$0.004 per GB-hour
- ALB: ~$16/month
- **Total**: ~$30-100/month

---

## ✅ Quick Checklist

- [ ] Run `./deploy-to-aws.sh` to push image
- [ ] Go to AWS App Runner Console
- [ ] Create service with ECR image
- [ ] Add environment variables
- [ ] Deploy!
- [ ] Update `LITELLM_API_URL` in your Next.js app

---

## 🎯 Summary

**Best Way = AWS App Runner**

1. ✅ Simplest setup (15 minutes)
2. ✅ Fully managed
3. ✅ Automatic HTTPS
4. ✅ Auto-scaling
5. ✅ Cost-effective

**Just run `./deploy-to-aws.sh` and create App Runner service!**
