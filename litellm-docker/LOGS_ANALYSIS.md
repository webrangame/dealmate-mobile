# Logs Analysis - Container Startup Issue

## Error Found in Logs

```
Usage: litellm [OPTIONS]
Try 'litellm --help' for help.
Error: Got unexpected extra argument (litellm)
```

## Root Cause

The LiteLLM base image (`ghcr.io/berriai/litellm:main-latest`) has `litellm` as the ENTRYPOINT. When we use:
- `CMD ["litellm", "--config", ...]` → It tries to run `litellm litellm --config ...` ❌

## Solution Applied

**Updated Dockerfile:**
```dockerfile
# Clear the entrypoint from base image
ENTRYPOINT []

# Use full command in CMD
CMD ["litellm", "--config", "/app/config.yaml", "--port", "4000", "--host", "0.0.0.0"]
```

This ensures:
- ENTRYPOINT is cleared (no default `litellm` entrypoint)
- CMD runs the full `litellm` command with all arguments

## Actions Taken

1. ✅ Fixed Dockerfile (cleared ENTRYPOINT, added full CMD)
2. ✅ Rebuilt Docker image
3. ✅ Pushed to ECR
4. ✅ Triggered new deployment

## Next Steps

Wait ~5-10 minutes for deployment, then check:

```bash
# Check status
aws apprunner describe-service \
  --service-arn arn:aws:apprunner:us-east-1:724772062824:service/litellm-proxy/b2128e35aa754cffbd7128eedca9ed5d \
  --region us-east-1 \
  --query 'Service.Status' \
  --output text

# Test when RUNNING
curl https://swzissb82u.us-east-1.awsapprunner.com/health
```

## Expected Result

With the fixed Dockerfile, the container should:
1. Start successfully ✅
2. Listen on port 4000 ✅
3. Respond to health checks ✅
4. Serve the LiteLLM API ✅
