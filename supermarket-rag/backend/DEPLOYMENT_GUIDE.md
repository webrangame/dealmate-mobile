# Deployment Guide - Local Embeddings Fix

## Summary
Switched from remote LiteLLM embeddings to local HuggingFace embeddings (`BAAI/bge-small-en-v1.5`) to resolve stability issues.

## AWS Deployment Steps

### 1. Deploy to AWS App Runner (Account: 582604091763)

```bash
# Push latest code
git push origin main

# If using AWS App Runner with source-based deployment, it will auto-deploy
# Otherwise, trigger manual deployment via AWS Console or CLI
```

### 2. Re-index Database (CRITICAL)

After deployment, you MUST re-index the database because the embedding dimensions changed (768→384):

**Option A: Via Server SSH/Console**
```bash
cd /app  # or wherever the app is deployed
python manual_ingest.py
```

**Option B: Via API (if you have an ingest endpoint)**
```bash
curl -X POST https://YOUR_APP_URL/ingest
```

### 3. Run 20x20 Test

```bash
# Set API URL if different from default
export API_URL="https://xfukqtd5pc.us-east-1.awsapprunner.com/chat"

# Run test
python test_api_20x20.py
```

## What Changed

- **Embeddings**: `LiteLLMEmbedding` → `HuggingFaceEmbedding(BAAI/bge-small-en-v1.5)`
- **Dimension**: 768 → 384
- **Benefits**: Local, faster, no remote API dependency
- **Database**: Old embeddings cleared, needs re-indexing

## Files Modified

- `rag_engine.py` - Switched embedding model
- `requirements.txt` - Added `llama-index-embeddings-huggingface`
- `verify_embedding.py` - Updated verification script
- `manual_ingest.py` - Added env loading
