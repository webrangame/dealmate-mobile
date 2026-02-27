# Troubleshooting LiteLLM Deployment

## Issue: 404 Error on Service URL

### Current Status
- **Service Status**: `OPERATION_IN_PROGRESS` (still deploying)
- **Service URL**: `https://swzissb82u.us-east-1.awsapprunner.com`

### Why You're Getting 404

The service is still in the deployment phase. App Runner typically takes **5-10 minutes** to:
1. Pull the Docker image from ECR
2. Start the container
3. Run health checks
4. Make the service available

### Check Service Status

```bash
aws apprunner describe-service \
  --service-arn arn:aws:apprunner:us-east-1:724772062824:service/litellm-proxy/b2128e35aa754cffbd7128eedca9ed5d \
  --region us-east-1 \
  --query 'Service.Status' \
  --output text
```

**Expected Statuses:**
- `OPERATION_IN_PROGRESS` - Still deploying (wait)
- `RUNNING` - Service is live ✅
- `CREATE_FAILED` - Deployment failed ❌
- `PAUSED` - Service is paused

### Wait for Deployment

The service needs time to:
1. Download the Docker image (~2-3 minutes)
2. Start the container (~1-2 minutes)
3. Pass health checks (~1-2 minutes)

**Total time: ~5-10 minutes**

### Test When Ready

Once status is `RUNNING`, test these endpoints:

```bash
# Health check
curl https://swzissb82u.us-east-1.awsapprunner.com/health

# Root endpoint
curl https://swzissb82u.us-east-1.awsapprunner.com/

# UI (if enabled)
curl https://swzissb82u.us-east-1.awsapprunner.com/ui

# Models list
curl -H "x-litellm-api-key: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642" \
  https://swzissb82u.us-east-1.awsapprunner.com/v1/models
```

### Check Logs (When Available)

Once the service is running, check logs:

```bash
# List log groups
aws logs describe-log-groups \
  --log-group-name-prefix /aws/apprunner \
  --region us-east-1

# View logs (replace with actual log group name)
aws logs tail /aws/apprunner/litellm-proxy/service --follow --region us-east-1
```

### Common Issues

#### 1. Service Still Deploying
**Solution**: Wait 5-10 minutes and check status again

#### 2. Container Fails to Start
**Check**: 
- Environment variables are correct
- Database connection is working
- Port 4000 is configured correctly

#### 3. Health Check Failing
**Check**:
- Container is listening on port 4000
- Health endpoint is accessible
- LiteLLM is starting correctly

### Manual Status Check Script

```bash
#!/bin/bash
SERVICE_ARN="arn:aws:apprunner:us-east-1:724772062824:service/litellm-proxy/b2128e35aa754cffbd7128eedca9ed5d"

while true; do
    STATUS=$(aws apprunner describe-service \
        --service-arn $SERVICE_ARN \
        --region us-east-1 \
        --query 'Service.Status' \
        --output text)
    
    echo "Status: $STATUS"
    
    if [ "$STATUS" == "RUNNING" ]; then
        echo "✅ Service is RUNNING!"
        URL=$(aws apprunner describe-service \
            --service-arn $SERVICE_ARN \
            --region us-east-1 \
            --query 'Service.ServiceUrl' \
            --output text)
        echo "🌐 URL: https://$URL"
        break
    elif [ "$STATUS" == "CREATE_FAILED" ]; then
        echo "❌ Service creation failed!"
        break
    else
        echo "⏳ Still deploying... waiting 30 seconds"
        sleep 30
    fi
done
```

### Next Steps

1. **Wait 5-10 minutes** for deployment to complete
2. **Check status** using the command above
3. **Test endpoints** once status is `RUNNING`
4. **Check logs** if there are any issues

### If Service Fails

If status becomes `CREATE_FAILED`:

1. Check the operation details:
```bash
aws apprunner list-operations \
  --service-arn arn:aws:apprunner:us-east-1:724772062824:service/litellm-proxy/b2128e35aa754cffbd7128eedca9ed5d \
  --region us-east-1 \
  --max-results 1
```

2. Review logs for errors
3. Verify Docker image is correct
4. Check environment variables
5. Verify database connection

### Quick Status Check

Run this to get current status:

```bash
aws apprunner describe-service \
  --service-arn arn:aws:apprunner:us-east-1:724772062824:service/litellm-proxy/b2128e35aa754cffbd7128eedca9ed5d \
  --region us-east-1 \
  --query 'Service.{Status:Status,Url:ServiceUrl,UpdatedAt:UpdatedAt}' \
  --output json
```
