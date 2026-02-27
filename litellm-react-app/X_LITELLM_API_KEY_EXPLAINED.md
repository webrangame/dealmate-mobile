# What is `x-litellm-api-key`?

## Quick Answer

`x-litellm-api-key` is an **HTTP header** used to authenticate admin operations with LiteLLM. The **value** of this header is your **Master Key** (also called Admin Key).

---

## Detailed Explanation

### 1. What is it?

`x-litellm-api-key` is the **header name** you use in HTTP requests to authenticate with LiteLLM for admin operations.

### 2. What is the value?

The **value** is your **LiteLLM Master Key** - a secret key that grants admin privileges.

**Current Master Key:**
```
sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642
```

### 3. Where is it defined?

The master key is defined in:

**Configuration File:**
- `litellm-docker/config.yaml` (line 52):
  ```yaml
  general_settings:
    master_key: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642
  ```

**Environment Variables:**
- `LITELLM_MASTER_KEY` (in Docker/AWS)
- `LITELLM_API_KEY` (in agent-market-place application)

---

## How to Use It

### In HTTP Requests

```bash
curl -X POST "https://swzissb82u.us-east-1.awsapprunner.com/user/new" \
  -H "x-litellm-api-key: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "123", "user_email": "user@example.com"}'
```

### In TypeScript/JavaScript

```typescript
const response = await fetch(`${LITELLM_API_URL}/user/new`, {
  method: 'POST',
  headers: {
    'x-litellm-api-key': 'sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642',
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    user_id: '123',
    user_email: 'user@example.com',
  }),
});
```

### In Python

```python
import requests

response = requests.post(
    f"{LITELLM_API_URL}/user/new",
    headers={
        "x-litellm-api-key": "sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642",
        "Content-Type": "application/json",
    },
    json={
        "user_id": "123",
        "user_email": "user@example.com",
    },
)
```

---

## What Operations Require It?

The `x-litellm-api-key` header is required for **admin operations**:

✅ **Requires Master Key:**
- `POST /user/new` - Create new user
- `GET /user/info` - Get user information
- `GET /user/list` - List all users
- `POST /key/generate` - Generate virtual keys
- `GET /key/list` - List user keys
- `POST /user/update` - Update user settings

❌ **Does NOT Require Master Key:**
- `POST /v1/chat/completions` - Uses `Authorization: Bearer <user-api-key>` instead
- `GET /health` - Public health check

---

## Key Types Comparison

| Key Type | Header | Format | Used For |
|----------|--------|--------|----------|
| **Master Key** | `x-litellm-api-key` | `sk-...` (long) | Admin operations |
| **User Virtual Key** | `Authorization: Bearer` | `sk-...` (shorter) | Making LLM requests |

### Example Master Key:
```
sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642
```

### Example User Virtual Key:
```
sk-N00S6nZMl_1xqzIZ13mdpw
```

---

## Security Notes

⚠️ **Important Security Considerations:**

1. **Never expose in client-side code** - Master keys should only be used server-side
2. **Store in environment variables** - Never hardcode in source files
3. **Don't commit to git** - Use `.env.local` or secure secret management
4. **Rotate if compromised** - If exposed, generate a new master key

### Where to Store:

✅ **Safe:**
- Server environment variables
- `.env.local` file (not committed)
- Vercel/AWS environment variables
- Secret management services

❌ **Unsafe:**
- Client-side JavaScript
- Public repositories
- Logs or error messages
- Browser localStorage (for master key)

---

## How to Find Your Master Key

### Option 1: Check Configuration File

```bash
cat litellm-docker/config.yaml | grep master_key
```

### Option 2: Check Environment Variables

```bash
# In Docker
docker-compose exec litellm env | grep LITELLM_MASTER_KEY

# In AWS App Runner
# Check AWS Console → App Runner → Service → Configuration → Environment Variables
```

### Option 3: Check Application Environment

```bash
# In agent-market-place
cat .env.local | grep LITELLM_API_KEY
```

---

## Current Setup

In your current setup:

**Master Key:**
```
sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642
```

**Where it's used:**
- `litellm-docker/config.yaml` - LiteLLM server configuration
- `agent-market-place/.env.local` - As `LITELLM_API_KEY`
- `agent-market-place/src/lib/litellm.ts` - In all admin API calls

**Example usage in code:**
```typescript
// From agent-market-place/src/lib/litellm.ts
const LITELLM_API_KEY = process.env.LITELLM_API_KEY || '';

headers['x-litellm-api-key'] = LITELLM_API_KEY;
```

---

## Summary

| Question | Answer |
|----------|--------|
| **What is `x-litellm-api-key`?** | HTTP header name for authentication |
| **What is the value?** | Your LiteLLM Master Key (starts with `sk-`) |
| **Where is it defined?** | `config.yaml` and environment variables |
| **When to use it?** | For all admin operations (create user, list users, generate keys, etc.) |
| **Current value?** | `sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642` |

---

## Quick Reference

```bash
# Set as environment variable
export LITELLM_API_KEY="sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642"

# Use in curl
curl -H "x-litellm-api-key: $LITELLM_API_KEY" ...

# Use in code
headers: {
  'x-litellm-api-key': process.env.LITELLM_API_KEY
}
```
