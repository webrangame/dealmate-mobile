# LiteLLM API: Get Virtual Key by User ID or Email

## Overview

LiteLLM provides several endpoints to retrieve user information and keys. However, **important note**: LiteLLM typically returns **hashed tokens** (not the actual virtual keys starting with `sk-`) for security reasons. The actual virtual keys are only returned when:
1. Creating a new user with `auto_create_key: true`
2. Generating a new key with `/key/generate`

## Available Endpoints

### 1. Get User Info by User ID

**Endpoint:** `GET /user/info?user_id=<user_id>`

**Description:** Get user information including keys (may return hashed tokens)

**Headers:**
```http
x-litellm-api-key: <master-key>
```

**Example:**
```bash
curl "https://swzissb82u.us-east-1.awsapprunner.com/user/info?user_id=123" \
  -H "x-litellm-api-key: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642"
```

**Response:**
```json
{
  "user_id": "123",
  "user_info": {
    "user_email": "user@example.com",
    "user_alias": "John Doe",
    "spend": 0.0,
    "tpm_limit": 100000,
    "rpm_limit": 100
  },
  "keys": [
    "ffeac5fae97e9ea4e6cb8874d7d5cf72b71707ad77d176178011b080198e625c"
  ]
}
```

**Note:** The `keys` array contains **hashed tokens**, not the actual virtual keys (`sk-...`). These cannot be used for API requests.

---

### 2. List Users by Email

**Endpoint:** `GET /user/list?user_email=<email>`

**Description:** Search for users by email (partial match supported)

**Headers:**
```http
x-litellm-api-key: <master-key>
```

**Query Parameters:**
- `user_email` (optional): Partial email match
- `user_ids` (optional): Comma-separated list of user IDs
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 10)

**Example:**
```bash
# Search by email
curl "https://swzissb82u.us-east-1.awsapprunner.com/user/list?user_email=example.com" \
  -H "x-litellm-api-key: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642"

# Get specific user IDs
curl "https://swzissb82u.us-east-1.awsapprunner.com/user/list?user_ids=123,456" \
  -H "x-litellm-api-key: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642"
```

**Response:**
```json
{
  "data": [
    {
      "user_id": "123",
      "user_email": "user@example.com",
      "user_alias": "John Doe",
      "spend": 0.0,
      "total_tokens": 0
    }
  ],
  "total_count": 1,
  "current_page": 1,
  "total_pages": 1
}
```

**Note:** This endpoint returns user information but **not the virtual keys**.

---

### 3. List Keys by User ID

**Endpoint:** `GET /key/list?user_id=<user_id>`

**Description:** List all keys for a specific user

**Headers:**
```http
x-litellm-api-key: <master-key>
```

**Example:**
```bash
curl "https://swzissb82u.us-east-1.awsapprunner.com/key/list?user_id=123" \
  -H "x-litellm-api-key: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642"
```

**Response:**
```json
{
  "keys": [
    "ffeac5fae97e9ea4e6cb8874d7d5cf72b71707ad77d176178011b080198e625c"
  ],
  "total_count": 1
}
```

**Note:** Again, this returns **hashed tokens**, not actual virtual keys.

---

### 4. Generate New Virtual Key (Recommended)

**Endpoint:** `POST /key/generate`

**Description:** Create a new virtual key for a user (returns the actual `sk-...` key)

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

**Response:**
```json
{
  "key": "sk-N00S6nZMl_1xqzIZ13mdpw",
  "user_id": "123",
  "key_alias": "My API Key",
  "tpm_limit": 100000,
  "rpm_limit": 100,
  "expires": null
}
```

**✅ This is the only endpoint that returns the actual virtual key (`sk-...`).**

---

## Complete Workflow: Get Virtual Key by Email

Since LiteLLM doesn't directly return existing virtual keys, here's the recommended workflow:

### Step 1: Find User by Email

```bash
curl "https://swzissb82u.us-east-1.awsapprunner.com/user/list?user_email=user@example.com" \
  -H "x-litellm-api-key: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642"
```

### Step 2: Get User ID from Response

Extract `user_id` from the response.

### Step 3: Generate New Virtual Key (or use existing if stored)

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

## TypeScript/JavaScript Implementation

```typescript
const LITELLM_API_URL = 'https://swzissb82u.us-east-1.awsapprunner.com';
const MASTER_KEY = 'sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642';

/**
 * Get user ID by email
 */
async function getUserByEmail(email: string): Promise<string | null> {
  const response = await fetch(
    `${LITELLM_API_URL}/user/list?user_email=${encodeURIComponent(email)}`,
    {
      headers: {
        'x-litellm-api-key': MASTER_KEY,
      },
    }
  );
  
  if (!response.ok) {
    return null;
  }
  
  const data = await response.json();
  if (data.data && data.data.length > 0) {
    return data.data[0].user_id;
  }
  
  return null;
}

/**
 * Get user info by user ID
 */
async function getUserInfo(userId: string) {
  const response = await fetch(
    `${LITELLM_API_URL}/user/info?user_id=${userId}`,
    {
      headers: {
        'x-litellm-api-key': MASTER_KEY,
      },
    }
  );
  
  if (!response.ok) {
    return null;
  }
  
  return await response.json();
}

/**
 * Generate new virtual key for user
 */
async function generateVirtualKey(userId: string) {
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
  
  if (!response.ok) {
    return null;
  }
  
  const data = await response.json();
  return data.key; // Returns: "sk-..."
}

/**
 * Complete workflow: Get virtual key by email
 */
async function getVirtualKeyByEmail(email: string): Promise<string | null> {
  // Step 1: Find user by email
  const userId = await getUserByEmail(email);
  if (!userId) {
    console.error('User not found');
    return null;
  }
  
  // Step 2: Generate new virtual key
  const virtualKey = await generateVirtualKey(userId);
  return virtualKey;
}

// Usage
getVirtualKeyByEmail('user@example.com').then(key => {
  console.log('Virtual Key:', key);
});
```

---

## Python Implementation

```python
import requests

LITELLM_API_URL = "https://swzissb82u.us-east-1.awsapprunner.com"
MASTER_KEY = "sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642"

def get_user_by_email(email: str) -> str | None:
    """Get user ID by email"""
    response = requests.get(
        f"{LITELLM_API_URL}/user/list",
        params={"user_email": email},
        headers={"x-litellm-api-key": MASTER_KEY},
    )
    
    if not response.ok:
        return None
    
    data = response.json()
    if data.get("data") and len(data["data"]) > 0:
        return data["data"][0]["user_id"]
    
    return None

def generate_virtual_key(user_id: str) -> str | None:
    """Generate new virtual key for user"""
    response = requests.post(
        f"{LITELLM_API_URL}/key/generate",
        headers={
            "x-litellm-api-key": MASTER_KEY,
            "Content-Type": "application/json",
        },
        json={
            "user_id": user_id,
            "duration": None,
        },
    )
    
    if not response.ok:
        return None
    
    data = response.json()
    return data.get("key")

def get_virtual_key_by_email(email: str) -> str | None:
    """Get virtual key by email (complete workflow)"""
    user_id = get_user_by_email(email)
    if not user_id:
        print("User not found")
        return None
    
    virtual_key = generate_virtual_key(user_id)
    return virtual_key

# Usage
key = get_virtual_key_by_email("user@example.com")
print(f"Virtual Key: {key}")
```

---

## Important Notes

1. **Security Limitation**: LiteLLM doesn't return existing virtual keys for security reasons. You can only get them when:
   - Creating a new user with `auto_create_key: true`
   - Generating a new key with `/key/generate`

2. **Key Storage**: If you need to retrieve virtual keys later, you should:
   - Store them securely when first created
   - Use `/key/generate` to create new keys when needed
   - Track keys in your own database

3. **Hashed Tokens**: The hashed tokens returned by `/user/info` and `/key/list` are for tracking purposes only and **cannot be used** for API requests.

4. **Best Practice**: Generate a new virtual key when needed, or store the key securely when first created.

---

## Summary

| Endpoint | By User ID | By Email | Returns Virtual Key? |
|----------|-----------|----------|---------------------|
| `/user/info?user_id=<id>` | ✅ | ❌ | ❌ (hashed tokens only) |
| `/user/list?user_email=<email>` | ❌ | ✅ | ❌ (user info only) |
| `/key/list?user_id=<id>` | ✅ | ❌ | ❌ (hashed tokens only) |
| `/key/generate` | ✅ | ❌ | ✅ (actual `sk-...` key) |

**To get a virtual key:**
1. Use `/user/list?user_email=<email>` to find user_id
2. Use `/key/generate` with the user_id to create/get a virtual key
