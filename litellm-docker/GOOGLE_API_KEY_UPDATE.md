# Google API Key Update - AWS App Runner

## ✅ Updates Completed

### 1. Updated `config.yaml`
- **Changed from**: Hardcoded API keys in config file
- **Changed to**: Using environment variables (`os.environ/GOOGLE_API_KEY`)
- **Benefit**: More secure, easier to update without rebuilding image

**Before:**
```yaml
api_key: AIzaSyDDSkUUl7gmWbqxVaE9iVB2KQzLh9SpwV8
```

**After:**
```yaml
api_key: os.environ/GOOGLE_API_KEY
```

### 2. Updated AWS App Runner Environment Variables
- **GOOGLE_API_KEY**: `AIzaSyDDSkUUl7gmWbqxVaE9iVB2KQzLh9SpwV8`
- **Status**: ✅ Set in App Runner service configuration
- **Service ARN**: `arn:aws:apprunner:us-east-1:724772062824:service/litellm-proxy/b2128e35aa754cffbd7128eedca9ed5d`

### 3. Rebuilt and Redeployed Docker Image
- **Image**: `724772062824.dkr.ecr.us-east-1.amazonaws.com/litellm-proxy:latest`
- **Status**: ✅ Pushed to ECR
- **Auto-deployment**: Enabled (App Runner will automatically deploy new image)

## 🔄 Current Status

**Service Status**: `OPERATION_IN_PROGRESS` (Redeploying)
- The service is currently redeploying with the updated configuration
- Expected completion: 5-10 minutes
- Service URL: `https://swzissb82u.us-east-1.awsapprunner.com`

## 📋 Environment Variables in AWS App Runner

The following environment variables are now configured:

```bash
LITELLM_MASTER_KEY=sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642
DATABASE_URL=postgresql://postgres:it371Ananda@agent-marketplace-db.cmt466aga8u0.us-east-1.rds.amazonaws.com:5432/litellm_db?sslmode=require
GOOGLE_API_KEY=AIzaSyDDSkUUl7gmWbqxVaE9iVB2KQzLh9SpwV8
STORE_MODEL_IN_DB=True
LITELLM_LOG=INFO
CONFIG=/app/config.yaml
```

## 🧪 Testing After Deployment

### 1. Check Service Status
```bash
aws apprunner describe-service \
  --service-arn arn:aws:apprunner:us-east-1:724772062824:service/litellm-proxy/b2128e35aa754cffbd7128eedca9ed5d \
  --region us-east-1 \
  --query 'Service.Status' \
  --output text
```

Expected: `RUNNING`

### 2. Test Health Endpoint
```bash
curl https://swzissb82u.us-east-1.awsapprunner.com/health
```

### 3. Test Chat Completion (with user API key)
```bash
curl -X POST https://swzissb82u.us-east-1.awsapprunner.com/v1/chat/completions \
  -H "Authorization: Bearer <user-api-key>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.5-pro",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## 🔧 Scripts Created

### `update-aws-env-vars.sh`
Updates AWS App Runner service environment variables without rebuilding the image.

**Usage:**
```bash
./update-aws-env-vars.sh
```

### `rebuild-and-deploy.sh`
Rebuilds the Docker image with updated config.yaml and pushes to ECR.

**Usage:**
```bash
./rebuild-and-deploy.sh
```

## 📝 How It Works

1. **Environment Variable**: `GOOGLE_API_KEY` is set in AWS App Runner
2. **Config File**: `config.yaml` references `os.environ/GOOGLE_API_KEY`
3. **LiteLLM**: Reads the environment variable and uses it for all Gemini models
4. **Result**: All models (gemini-2.5-pro, gemini-2.5-flash, etc.) use the same API key from environment

## ⚠️ Troubleshooting

### If "GOOGLE_API_KEY not set" error persists:

1. **Verify environment variable is set:**
   ```bash
   aws apprunner describe-service \
     --service-arn <SERVICE_ARN> \
     --region us-east-1 \
     --query 'Service.SourceConfiguration.ImageRepository.ImageConfiguration.RuntimeEnvironmentVariables.GOOGLE_API_KEY' \
     --output text
   ```

2. **Check service logs:**
   ```bash
   aws logs tail /aws/apprunner/litellm-proxy/b2128e35aa754cffbd7128eedca9ed5d/application --follow --region us-east-1
   ```

3. **Verify config.yaml in container:**
   - The config should use `os.environ/GOOGLE_API_KEY`
   - Not hardcoded values

4. **Wait for deployment to complete:**
   - Status should be `RUNNING`
   - Not `OPERATION_IN_PROGRESS` or `CREATE_FAILED`

## ✅ Verification Checklist

- [x] `config.yaml` updated to use `os.environ/GOOGLE_API_KEY`
- [x] `GOOGLE_API_KEY` environment variable set in AWS App Runner
- [x] Docker image rebuilt with updated config
- [x] Image pushed to ECR
- [x] Service redeploying (OPERATION_IN_PROGRESS)
- [ ] Service status: RUNNING (wait for deployment)
- [ ] Health endpoint responds
- [ ] Chat completion works with Gemini models

## 🎯 Next Steps

1. **Wait for deployment** (~5-10 minutes)
2. **Verify service status** is `RUNNING`
3. **Test API endpoints** to confirm GOOGLE_API_KEY is working
4. **Monitor logs** for any errors

## 📚 Related Files

- `config.yaml` - LiteLLM configuration (now uses env vars)
- `update-aws-env-vars.sh` - Script to update App Runner env vars
- `rebuild-and-deploy.sh` - Script to rebuild and redeploy image
- `Dockerfile` - Docker image definition
- `app-runner-service.json` - App Runner service configuration
