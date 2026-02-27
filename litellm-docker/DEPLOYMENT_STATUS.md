# LiteLLM AWS Deployment Status

## ✅ Completed Steps

1. ✅ **AWS Credentials Configured**
   - Access Key: AKIAYPJPI6FZXORNUHMT
   - Region: us-east-1

2. ✅ **Docker Image Built & Pushed**
   - ECR Repository: `724772062824.dkr.ecr.us-east-1.amazonaws.com/litellm-proxy:latest`
   - Image successfully pushed to ECR

3. ✅ **ECS Cluster Created**
   - Cluster: `litellm-cluster`
   - Status: Active

4. ✅ **CloudWatch Logs Configured**
   - Log Group: `/ecs/litellm-proxy`

## 🔄 Next Steps

### Step 1: Create LiteLLM Database

The database `litellm_db` needs to be created on your RDS instance.

**Option A: Using psql (if installed)**
```bash
PGPASSWORD=it371Ananda psql -h agent-marketplace-db.cmt466aga8u0.us-east-1.rds.amazonaws.com -p 5432 -U postgres -d postgres -c "CREATE DATABASE litellm_db;"
```

**Option B: Using AWS Console**
1. Go to AWS RDS Console
2. Select your database: `agent-marketplace-db`
3. Connect using a database client (DBeaver, pgAdmin, etc.)
4. Run: `CREATE DATABASE litellm_db;`

**Option C: Using AWS CLI (if you have RDS Data API enabled)**
```bash
# This requires RDS Data API to be enabled
aws rds-data execute-statement \
  --resource-arn <DB_CLUSTER_ARN> \
  --secret-arn <SECRET_ARN> \
  --database postgres \
  --sql "CREATE DATABASE litellm_db;"
```

### Step 2: Create App Runner Service

**Option A: Using AWS Console (Recommended)**
1. Go to: https://console.aws.amazon.com/apprunner
2. Click "Create service"
3. Select: Container registry → Amazon ECR
4. Image URI: `724772062824.dkr.ecr.us-east-1.amazonaws.com/litellm-proxy:latest`
5. Configure:
   - Service name: `litellm-proxy`
   - CPU: 0.5 vCPU
   - Memory: 1 GB
   - Port: 4000
6. Add Environment Variables:
   ```
   LITELLM_MASTER_KEY=sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642
   DATABASE_URL=postgresql://postgres:it371Ananda@agent-marketplace-db.cmt466aga8u0.us-east-1.rds.amazonaws.com:5432/litellm_db?sslmode=require
   GOOGLE_API_KEY=AIzaSyDDSkUUl7gmWbqxVaE9iVB2KQzLh9SpwV8
   STORE_MODEL_IN_DB=True
   LITELLM_LOG=INFO
   CONFIG=/app/config.yaml
   ```
7. Click "Create & Deploy"

**Option B: Using AWS CLI**
```bash
cd /home/ranga/code/pragith/whatssapp-chat/litellm-docker
aws apprunner create-service \
  --cli-input-json file://app-runner-service.json \
  --region us-east-1
```

### Step 3: Update .env.local

Add this to your `.env.local` file (lines 2-3):

```bash
# LiteLLM Database URL
LITELLM_DATABASE_URL=postgresql://postgres:it371Ananda@agent-marketplace-db.cmt466aga8u0.us-east-1.rds.amazonaws.com:5432/litellm_db?sslmode=require
```

Or run:
```bash
cd /home/ranga/code/pragith/whatssapp-chat/agent-market-place
echo "" >> .env.local
echo "# LiteLLM Database URL" >> .env.local
echo "LITELLM_DATABASE_URL=postgresql://postgres:it371Ananda@agent-marketplace-db.cmt466aga8u0.us-east-1.rds.amazonaws.com:5432/litellm_db?sslmode=require" >> .env.local
```

## 📋 Configuration Summary

- **ECR Image**: `724772062824.dkr.ecr.us-east-1.amazonaws.com/litellm-proxy:latest`
- **Database Host**: `agent-marketplace-db.cmt466aga8u0.us-east-1.rds.amazonaws.com`
- **Database Name**: `litellm_db` (needs to be created)
- **Database User**: `postgres`
- **Database Password**: `it371Ananda`
- **Port**: `5432`

## 🎯 After Deployment

Once App Runner service is created:

1. **Get Service URL**:
   ```bash
   aws apprunner describe-service \
     --service-arn <SERVICE_ARN> \
     --region us-east-1 \
     --query 'Service.ServiceUrl' \
     --output text
   ```

2. **Test LiteLLM**:
   ```bash
   curl https://your-app-runner-url/health
   ```

3. **Update Next.js App**:
   - Update `LITELLM_API_URL` in Vercel environment variables
   - Point to your App Runner URL

## ✅ Checklist

- [x] AWS credentials configured
- [x] Docker image built and pushed to ECR
- [x] ECS cluster created
- [ ] LiteLLM database created (`litellm_db`)
- [ ] App Runner service created
- [ ] App Runner service deployed and running
- [ ] .env.local updated with database URL
- [ ] LiteLLM tested and working
- [ ] Next.js app updated with new LiteLLM URL
