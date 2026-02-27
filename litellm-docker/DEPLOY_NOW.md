# Deploy LiteLLM to AWS - Right Now! 🚀

## 🏆 Best Way: AWS App Runner (15 minutes)

### Why App Runner?
- ✅ **Simplest** - No complex setup
- ✅ **Fastest** - 15 minutes total
- ✅ **Automatic HTTPS** - SSL included
- ✅ **Auto-scaling** - Handles traffic
- ✅ **Fully managed** - No server management

---

## 🚀 Deploy in 2 Steps

### Step 1: Push Docker Image (5 minutes)

```bash
cd /home/ranga/code/pragith/whatssapp-chat/litellm-docker
./deploy-to-aws.sh
```

Wait for it to complete (~3-5 minutes)

### Step 2: Create App Runner Service (10 minutes)

**Option A: Use the helper script**
```bash
./create-app-runner.sh
```
This will show you exactly what to do.

**Option B: Manual steps**

1. **Open AWS Console**: https://console.aws.amazon.com/apprunner

2. **Click "Create service"**

3. **Source**:
   - Container registry → Amazon ECR
   - Image URI: `724772062824.dkr.ecr.us-east-1.amazonaws.com/litellm-proxy:latest`
   - Deployment: Automatic

4. **Service Settings**:
   - Name: `litellm-proxy`
   - CPU: 0.5 vCPU
   - Memory: 1 GB
   - Port: `4000`

5. **Environment Variables** (click "Add environment variable" for each):
   ```
   LITELLM_MASTER_KEY = sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642
   DATABASE_URL = postgresql://postgres:it371Ananda@agent-marketplace-db.cmt466aga8u0.us-east-1.rds.amazonaws.com:5432/litellm_db?sslmode=require
   GOOGLE_API_KEY = AIzaSyDDSkUUl7gmWbqxVaE9iVB2KQzLh9SpwV8
   STORE_MODEL_IN_DB = True
   LITELLM_LOG = INFO
   CONFIG = /app/config.yaml
   ```

6. **Click "Create & Deploy"**

7. **Wait 5 minutes** - Your LiteLLM will be live!

---

## ✅ After Deployment

1. **Get your URL**:
   - Go to App Runner → Your service
   - Copy the "Default domain" URL
   - Example: `https://xxxxx.us-east-1.awsapprunner.com`

2. **Test it**:
   ```bash
   curl https://your-app-runner-url/health
   ```

3. **Update Next.js app**:
   - Go to Vercel → Environment Variables
   - Update `LITELLM_API_URL` to your App Runner URL
   - Redeploy

---

## 🎉 Done!

Your LiteLLM is now running on AWS! 🚀

**Access**:
- API: `https://your-app-runner-url`
- UI: `https://your-app-runner-url/ui`
- Health: `https://your-app-runner-url/health`

---

## 💰 Cost

- **~$25-80/month** (depending on traffic)
- Pay only for what you use
- No upfront costs

---

## 🔄 Update LiteLLM

When you need to update:

```bash
cd /home/ranga/code/pragith/whatssapp-chat/litellm-docker
./deploy-to-aws.sh
```

App Runner will automatically detect the new image and deploy it!

---

## 🆘 Troubleshooting

**Service not starting?**
- Check CloudWatch logs in App Runner console
- Verify environment variables are correct
- Check database connection

**Can't access?**
- Wait 5-10 minutes for deployment to complete
- Check service status in App Runner console
- Verify port is 4000

---

## 📚 More Options

- **Need more control?** → See `AWS_DEPLOYMENT.md` (ECS Fargate)
- **Want simpler?** → Use App Runner (this guide) ⭐
