# AWS Manual Update & Testing Guide

## ✅ What's Already Done

1. **Code pushed to GitHub** (commit `f6290949`)
2. **Local automation configured** (cron job runs daily at 8 AM)
3. **PDF URLs verified** for Feb 11-17, 2026:
   - Coles: `COLNSWMETRO_110226_AQM6NRS.pdf` (28.3 MB)
   - Woolworths: `WW_NSW_110226_5UK7TA7434.pdf` (28.1 MB)

## 📋 Manual Steps for AWS

### Step 1: Wait for AWS App Runner Deployment

AWS App Runner automatically deploys from GitHub. This usually takes **5-10 minutes**.

**Check deployment status:**
- Go to: https://console.aws.amazon.com/apprunner
- Or run: `aws apprunner list-operations --service-arn YOUR_ARN --region us-east-1`

### Step 2: Trigger Production Ingestion

Once deployment is complete, run this command to ingest the latest catalogs:

```bash
curl -X POST https://xfukqtd5pc.us-east-1.awsapprunner.com/api/admin/ingest \
  -H "X-Admin-Key: YOUR_ADMIN_KEY" \
  -H "Content-Type: application/json" \
  -v
```

**Expected response:**
```json
{
  "message": "Ingestion completed successfully",
  "nodes_created": 111
}
```

This will take **3-5 minutes** to complete.

### Step 3: Run 20x20 Live Test

After ingestion completes, test the production API:

```bash
cd /home/ranga/code/pragith/whatssapp-chat/supermarket-rag/backend
python3 test_20x20_live.py
```

**Expected results:**
- ✅ 40/40 questions successful (100%)
- ✅ 95%+ multi-shop coverage
- ✅ Response time < 5 seconds per query

Results will be saved to: `test_results_live_20x20.json`

### Step 4: Verify with Quick Test

Quick smoke test:

```bash
curl -X POST https://xfukqtd5pc.us-east-1.awsapprunner.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "ice cream price", "user_id": "test@example.com"}' \
  | jq
```

**Expected response should include:**
- Prices from both Coles and Woolworths
- Product names and details
- Shop names clearly mentioned

## 🔍 Troubleshooting

### If Deployment Fails:
- Check AWS App Runner logs in console
- Verify GitHub connection is active
- Review environment variables are set

### If Ingestion Fails:
- Check database connection
- Verify PDF URLs are accessible: `python3 test_pdf_urls.py`
- Check S3 bucket permissions

### If Tests Fail:
- Verify API is up: `curl https://xfukqtd5pc.us-east-1.awsapprunner.com/health`
- Check database has data
- Review application logs in AWS Console

## 📊 Success Criteria

- [x] Code deployed to GitHub
- [ ] AWS App Runner deployment complete
- [ ] Production ingestion successful (111 nodes)
- [ ] 20x20 test passes with 95%+ success
- [ ] Multi-shop coverage working

---

**Ready to proceed?** Just follow the steps above after AWS deployment completes!
