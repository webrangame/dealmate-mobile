# LiteLLM Quick Start Guide

## ✅ Status

LiteLLM is now running locally!

- **URL**: http://localhost:4000
- **UI**: http://localhost:4000/ui
- **API Docs**: http://localhost:4000/docs
- **Master Key**: `sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642`

## 🚀 Quick Commands

### Check Status
```bash
docker-compose ps
```

### View Logs
```bash
docker-compose logs -f litellm
```

### Stop LiteLLM
```bash
docker-compose down
```

### Start LiteLLM
```bash
docker-compose up -d
```

### Restart LiteLLM
```bash
docker-compose restart
```

## 🧪 Test the API

### Health Check
```bash
curl http://localhost:4000/health
```

### Create a User
```bash
curl -X POST 'http://localhost:4000/user/new' \
  -H 'x-litellm-api-key: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "123",
    "user_email": "test@example.com",
    "user_alias": "Test User"
  }'
```

### List User Keys
```bash
curl -X GET 'http://localhost:4000/key/list?user_id=123' \
  -H 'x-litellm-api-key: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642'
```

### Get User Info
```bash
curl -X GET 'http://localhost:4000/user/info?user_id=123' \
  -H 'x-litellm-api-key: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642'
```

## 🔧 Update Agent Marketplace to Use Local LiteLLM

To test with your agent marketplace, update the environment variable:

```bash
# In your agent-market-place project
export LITELLM_API_URL=http://localhost:4000
export LITELLM_API_KEY=sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642
```

Then run the sync script:
```bash
cd /home/ranga/code/pragith/whatssapp-chat/agent-market-place
export DATABASE_URL="postgresql://postgres:it371Ananda@agent-marketplace-db.cmt466aga8u0.us-east-1.rds.amazonaws.com:5432/postgres?sslmode=require"
export LITELLM_API_URL="http://localhost:4000"
export LITELLM_API_KEY="sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642"
npm run sync-litellm-users
```

## 📝 Notes

- This LiteLLM instance uses **in-memory storage** (no database)
- Data will be lost when you restart the container
- For production, you should configure a database
- The master key is stored in `.env` and `config.yaml`

## 🔒 Security

⚠️ **Important**: The master key in this setup is for local development only. 
- Never commit the `.env` file to git
- Use a different key for production
- Keep the master key secure
