# LiteLLM API Reference

Complete reference guide for LiteLLM API integration.

## 📍 API Base URLs

### Production
```
https://swzissb82u.us-east-1.awsapprunner.com
```

### Local Development
```
http://localhost:4000
```

### UI Dashboard
```
https://swzissb82u.us-east-1.awsapprunner.com/ui/login/
```

---

## 🔑 Authentication

### Master Key (Admin Operations)

**Header Format:**
```http
x-litellm-api-key: <master-key>
```

**Current Master Key:**
```
sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642
```

**Used For:**
- Creating users
- Managing API keys
- Viewing user information
- Admin operations

**Example:**
```bash
curl -X GET "https://swzissb82u.us-east-1.awsapprunner.com/user/info?user_id=123" \
  -H "x-litellm-api-key: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642"
```

### User API Key (Regular Operations)

**Header Format:**
```http
Authorization: Bearer <user-api-key>
```

**Used For:**
- Making LLM chat completion requests
- User-specific operations

**Example:**
```bash
curl -X POST "https://swzissb82u.us-east-1.awsapprunner.com/v1/chat/completions" \
  -H "Authorization: Bearer sk-user-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{"model": "gemini-2.5-pro", "messages": [{"role": "user", "content": "Hello!"}]}'
```

---

## 📡 API Endpoints

### 1. Health Check

**Endpoint:** `GET /health`

**Description:** Check if LiteLLM service is running

**Headers:** None required

**Example:**
```bash
curl https://swzissb82u.us-east-1.awsapprunner.com/health
```

**Response:**
```json
{"status": "healthy"}
```

---

### 2. Create User

**Endpoint:** `POST /user/new`

**Description:** Create a new user in LiteLLM

**Headers:**
```http
x-litellm-api-key: <master-key>
Content-Type: application/json
```

**Request Body:**
```json
{
  "user_id": "123",
  "user_email": "user@example.com",
  "user_alias": "John Doe",
  "user_role": "internal_user",
  "auto_create_key": true,
  "tpm_limit": 100000,
  "rpm_limit": 100,
  "max_parallel_requests": 10,
  "send_invite_email": false,
  "metadata": {
    "created_from": "agent-marketplace"
  }
}
```

**Response:**
```json
{
  "user_id": "123",
  "key": "sk-abc123...",
  "user_email": "user@example.com"
}
```

**Example:**
```bash
curl -X POST "https://swzissb82u.us-east-1.awsapprunner.com/user/new" \
  -H "x-litellm-api-key: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "123",
    "user_email": "user@example.com",
    "user_alias": "John Doe",
    "auto_create_key": true,
    "tpm_limit": 100000,
    "rpm_limit": 100
  }'
```

---

### 3. Get User Info

**Endpoint:** `GET /user/info?user_id=<user_id>`

**Description:** Get user information including keys and usage

**Headers:**
```http
x-litellm-api-key: <master-key>
```

**Query Parameters:**
- `user_id` (required): User ID

**Response:**
```json
{
  "user_id": "123",
  "user_info": {
    "user_email": "user@example.com",
    "user_alias": "John Doe",
    "user_role": "internal_user",
    "spend": 0.0,
    "total_tokens": 0,
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "tpm_limit": 100000,
    "rpm_limit": 100
  },
  "keys": ["hash1", "hash2"],
  "teams": []
}
```

**Example:**
```bash
curl "https://swzissb82u.us-east-1.awsapprunner.com/user/info?user_id=123" \
  -H "x-litellm-api-key: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642"
```

---

### 4. List User Keys

**Endpoint:** `GET /key/list?user_id=<user_id>`

**Description:** List all API keys for a user

**Headers:**
```http
x-litellm-api-key: <master-key>
```

**Query Parameters:**
- `user_id` (required): User ID

**Response:**
```json
{
  "keys": ["hash1", "hash2"],
  "total_count": 2,
  "current_page": 1,
  "total_pages": 1
}
```

**Example:**
```bash
curl "https://swzissb82u.us-east-1.awsapprunner.com/key/list?user_id=123" \
  -H "x-litellm-api-key: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642"
```

---

### 5. Generate New Key

**Endpoint:** `POST /key/generate`

**Description:** Create a new virtual API key for a user

**Headers:**
```http
x-litellm-api-key: <master-key>
Content-Type: application/json
```

**Request Body:**
```json
{
  "user_id": "123",
  "duration": null,
  "key_alias": "My API Key",
  "tpm_limit": 100000,
  "rpm_limit": 100
}
```

**Response:**
```json
{
  "key": "sk-abc123...",
  "user_id": "123",
  "key_alias": "My API Key",
  "tpm_limit": 100000,
  "rpm_limit": 100,
  "expires": null
}
```

**Example:**
```bash
curl -X POST "https://swzissb82u.us-east-1.awsapprunner.com/key/generate" \
  -H "x-litellm-api-key: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "123",
    "duration": null
  }'
```

---

### 6. Chat Completions

**Endpoint:** `POST /v1/chat/completions`

**Description:** Make LLM chat completion requests

**Headers:**
```http
Authorization: Bearer <user-api-key>
Content-Type: application/json
```

**Request Body:**
```json
{
  "model": "gemini-2.5-pro",
  "messages": [
    {"role": "user", "content": "Hello!"}
  ],
  "temperature": 0.7,
  "max_tokens": 1000
}
```

**Response:**
```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "Hello! How can I help you today?"
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 12,
    "total_tokens": 21
  }
}
```

**Example:**
```bash
curl -X POST "https://swzissb82u.us-east-1.awsapprunner.com/v1/chat/completions" \
  -H "Authorization: Bearer sk-user-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.5-pro",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

---

## 🤖 Available Models

Based on the current configuration, these models are available:

### Primary Models
- `gemini-2.5-pro` - Latest Gemini Pro model
- `gemini-2.5-flash` - Fast Gemini Flash model
- `gemini-2.0-flash` - Gemini 2.0 Flash

### Legacy Aliases
- `gemini-pro` → maps to `gemini-2.0-flash`
- `gemini-1.5-pro` → maps to `gemini-2.5-pro`
- `gemini-1.5-flash` → maps to `gemini-2.5-flash`

---

## 🔧 Environment Variables

### Required for Backend Integration

```bash
# LiteLLM API URL
LITELLM_API_URL=https://swzissb82u.us-east-1.awsapprunner.com

# LiteLLM Master Key (for admin operations)
LITELLM_API_KEY=sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642
```

### LiteLLM Server Configuration

```bash
# Master Key (must match config.yaml)
LITELLM_MASTER_KEY=sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642

# Google API Key (for Gemini models)
GOOGLE_API_KEY=AIzaSyDDSkUUl7gmWbqxVaE9iVB2KQzLh9SpwV8

# Database URL (optional)
DATABASE_URL=postgresql://postgres:password@host:5432/litellm_db

# Configuration file path
CONFIG=/app/config.yaml

# Logging level
LITELLM_LOG=INFO

# Store models in database
STORE_MODEL_IN_DB=True
```

---

## 📊 User Configuration Defaults

When creating users, these defaults are applied:

```typescript
{
  user_role: 'internal_user',
  auto_create_key: true,
  send_invite_email: false,
  max_parallel_requests: 10,
  tpm_limit: 100000,      // Tokens per minute
  rpm_limit: 100,         // Requests per minute
  metadata: {
    created_from: 'agent-marketplace',
    created_at: '<timestamp>'
  }
}
```

---

## 🔐 Key Types

### Master Key
- **Format:** Starts with `sk-`
- **Usage:** Admin operations
- **Header:** `x-litellm-api-key`
- **Example:** `sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642`

### Virtual Key (User API Key)
- **Format:** Starts with `sk-`
- **Usage:** User API requests
- **Header:** `Authorization: Bearer`
- **Example:** `sk-N00S6nZMl_1xqzIZ13mdpw`

### Hashed Token
- **Format:** Long hexadecimal string (64 chars)
- **Usage:** Internal reference only (NOT for API calls)
- **Example:** `ffeac5fae97e9ea4e6cb8874d7d5cf72b71707ad77d176178011b080198e625c`
- **Note:** Cannot be used for API requests, only for tracking

---

## 💻 Code Examples

### TypeScript/JavaScript

```typescript
const LITELLM_API_URL = 'https://swzissb82u.us-east-1.awsapprunner.com';
const MASTER_KEY = 'sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642';

// Create User
async function createUser(userId: string, email: string, name: string) {
  const response = await fetch(`${LITELLM_API_URL}/user/new`, {
    method: 'POST',
    headers: {
      'x-litellm-api-key': MASTER_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_id: userId,
      user_email: email,
      user_alias: name,
      auto_create_key: true,
      tpm_limit: 100000,
      rpm_limit: 100,
    }),
  });
  return await response.json();
}

// Get User Info
async function getUserInfo(userId: string) {
  const response = await fetch(
    `${LITELLM_API_URL}/user/info?user_id=${userId}`,
    {
      headers: {
        'x-litellm-api-key': MASTER_KEY,
      },
    }
  );
  return await response.json();
}

// Generate Key
async function generateKey(userId: string) {
  const response = await fetch(`${LITELLM_API_URL}/key/generate`, {
    method: 'POST',
    headers: {
      'x-litellm-api-key': MASTER_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_id: userId,
      duration: null,
    }),
  });
  return await response.json();
}

// Chat Completion
async function chatCompletion(apiKey: string, messages: any[], model: string = 'gemini-2.5-pro') {
  const response = await fetch(`${LITELLM_API_URL}/v1/chat/completions`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model,
      messages,
      temperature: 0.7,
      max_tokens: 1000,
    }),
  });
  return await response.json();
}
```

### Python

```python
import requests

LITELLM_API_URL = "https://swzissb82u.us-east-1.awsapprunner.com"
MASTER_KEY = "sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642"

def create_user(user_id: str, email: str, name: str):
    response = requests.post(
        f"{LITELLM_API_URL}/user/new",
        headers={
            "x-litellm-api-key": MASTER_KEY,
            "Content-Type": "application/json",
        },
        json={
            "user_id": user_id,
            "user_email": email,
            "user_alias": name,
            "auto_create_key": True,
            "tpm_limit": 100000,
            "rpm_limit": 100,
        },
    )
    return response.json()

def chat_completion(api_key: str, messages: list, model: str = "gemini-2.5-pro"):
    response = requests.post(
        f"{LITELLM_API_URL}/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000,
        },
    )
    return response.json()
```

---

## ⚠️ Important Notes

1. **Master Key Security:**
   - Never expose master key in client-side code
   - Always use master key server-side only
   - Store in environment variables, never commit to git

2. **Virtual Keys:**
   - Virtual keys (starting with `sk-`) are required for API requests
   - Hashed tokens from `/user/info` cannot be used for API calls
   - Always use `/key/generate` to create new virtual keys

3. **Rate Limits:**
   - Default: 100,000 TPM (tokens per minute)
   - Default: 100 RPM (requests per minute)
   - Can be customized per user

4. **Error Handling:**
   - Always check response status codes
   - Handle authentication errors (401)
   - Handle rate limit errors (429)

---

## 📚 Additional Resources

- **Frontend Integration Guide:** `FRONTEND_INTEGRATION.md`
- **How to Create Virtual Keys:** `HOW_TO_CREATE_VIRTUAL_KEY.md`
- **LiteLLM Documentation:** https://docs.litellm.ai
- **UI Dashboard:** https://swzissb82u.us-east-1.awsapprunner.com/ui/login/

---

## 🔍 Quick Reference

| Operation | Endpoint | Method | Auth Header |
|-----------|----------|--------|-------------|
| Health Check | `/health` | GET | None |
| Create User | `/user/new` | POST | `x-litellm-api-key` |
| Get User Info | `/user/info?user_id=<id>` | GET | `x-litellm-api-key` |
| List Keys | `/key/list?user_id=<id>` | GET | `x-litellm-api-key` |
| Generate Key | `/key/generate` | POST | `x-litellm-api-key` |
| Chat Completion | `/v1/chat/completions` | POST | `Authorization: Bearer` |

---

**Last Updated:** 2026-01-01
**API Version:** LiteLLM Proxy v1.x
