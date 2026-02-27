# How to Create LiteLLM Virtual Keys

LiteLLM virtual keys are API keys that start with `sk-` and are used to authenticate API requests. Here are several ways to create them:

## Method 1: Using LiteLLM API Endpoint `/key/generate`

### Basic Request

```bash
curl -X POST "https://swzissb82u.us-east-1.awsapprunner.com/key/generate" \
  -H "x-litellm-api-key: YOUR_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "admin",
    "duration": null
  }'
```

### Response

```json
{
  "key": "sk-abc123def456...",
  "user_id": "admin",
  "expires": null
}
```

## Method 2: Create Key for Existing User

```bash
curl -X POST "https://swzissb82u.us-east-1.awsapprunner.com/key/generate" \
  -H "x-litellm-api-key: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "admin",
    "duration": null,
    "key_alias": "My API Key",
    "tpm_limit": 100000,
    "rpm_limit": 100
  }'
```

## Method 3: Create User with Auto-Generated Key

When creating a new user, you can automatically create a key:

```bash
curl -X POST "https://swzissb82u.us-east-1.awsapprunner.com/user/new" \
  -H "x-litellm-api-key: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "newuser",
    "user_email": "user@example.com",
    "user_alias": "New User",
    "auto_create_key": true,
    "tpm_limit": 100000,
    "rpm_limit": 100
  }'
```

**Response includes the key:**
```json
{
  "user_id": "newuser",
  "key": "sk-xyz789abc123...",
  "user_email": "user@example.com"
}
```

## Method 4: Using JavaScript/TypeScript

```javascript
async function createVirtualKey(userId, masterKey) {
  const response = await fetch('https://swzissb82u.us-east-1.awsapprunner.com/key/new', {
    method: 'POST',
    headers: {
      'x-litellm-api-key': masterKey,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_id: userId,
      duration: null, // null = no expiration
      key_alias: 'My API Key',
      tpm_limit: 100000,
      rpm_limit: 100,
    }),
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Failed to create key: ${error}`);
  }

  const data = await response.json();
  return data.key; // Returns: "sk-abc123..."
}

// Usage
const masterKey = 'sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642';
const virtualKey = await createVirtualKey('admin', masterKey);
console.log('Virtual Key:', virtualKey);
```

## Method 5: Using Python

```python
import requests

def create_virtual_key(user_id, master_key):
    url = "https://swzissb82u.us-east-1.awsapprunner.com/key/new"
    headers = {
        "x-litellm-api-key": master_key,
        "Content-Type": "application/json"
    }
    data = {
        "user_id": user_id,
        "duration": None,  # None = no expiration
        "key_alias": "My API Key",
        "tpm_limit": 100000,
        "rpm_limit": 100
    }
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    
    return response.json()["key"]

# Usage
master_key = "sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642"
virtual_key = create_virtual_key("admin", master_key)
print(f"Virtual Key: {virtual_key}")
```

## Method 6: Using LiteLLM UI Dashboard

1. Go to: `https://swzissb82u.us-east-1.awsapprunner.com/ui/login/`
2. Login with your master key
3. Navigate to "Keys" section
4. Click "Create New Key"
5. Select the user
6. Configure limits and settings
7. Click "Create"
8. Copy the generated key (starts with `sk-`)

## Key Parameters

When creating a key, you can specify:

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `user_id` | string | User ID to associate key with | `"admin"` |
| `duration` | number/null | Key expiration in seconds (null = no expiration) | `null` or `86400` (1 day) |
| `key_alias` | string | Friendly name for the key | `"Production Key"` |
| `tpm_limit` | number | Tokens per minute limit | `100000` |
| `rpm_limit` | number | Requests per minute limit | `100` |
| `max_budget` | number | Maximum spending budget | `100.0` |
| `models` | array | Allowed models | `["gemini-2.5-pro"]` |

## Important Notes

1. **Master Key Required**: You need the master key (`x-litellm-api-key` header) to create keys
2. **Virtual Keys Start with `sk-`**: All virtual keys start with `sk-` prefix
3. **Hashed Tokens**: The `/user/info` endpoint returns hashed tokens (not virtual keys) for security
4. **Key Storage**: Save the key immediately after creation - it's only shown once
5. **Key Expiration**: Set `duration: null` for keys that never expire

## Troubleshooting

### Error: "Authentication Error, LiteLLM Virtual Key expected"

This means you're using a hashed token instead of a virtual key. Solution:
1. Create a new virtual key using `/key/new` endpoint
2. Use the returned `key` value (starts with `sk-`)
3. Never use hashed tokens from `/user/info` for API requests

### Error: "Failed to create API key"

Check:
- Master key is correct
- User exists in LiteLLM
- API endpoint is accessible
- Request format is correct

## Example: Complete Flow

```javascript
// 1. Create user with auto-generated key
const createUserResponse = await fetch('https://swzissb82u.us-east-1.awsapprunner.com/user/new', {
  method: 'POST',
  headers: {
    'x-litellm-api-key': MASTER_KEY,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    user_id: 'myuser',
    user_email: 'user@example.com',
    auto_create_key: true,
  }),
});

const userData = await createUserResponse.json();
const virtualKey = userData.key; // "sk-abc123..."

// 2. Use the virtual key for API requests
const chatResponse = await fetch('https://swzissb82u.us-east-1.awsapprunner.com/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${virtualKey}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'gemini-2.5-pro',
    messages: [{ role: 'user', content: 'Hello!' }],
  }),
});
```

## Quick Test Script

Save this as `create-key.sh`:

```bash
#!/bin/bash

MASTER_KEY="sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642"
USER_ID="admin"
API_URL="https://swzissb82u.us-east-1.awsapprunner.com"

echo "Creating virtual key for user: $USER_ID"
echo ""

RESPONSE=$(curl -s -X POST "$API_URL/key/new" \
  -H "x-litellm-api-key: $MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"user_id\": \"$USER_ID\",
    \"duration\": null
  }")

echo "Response:"
echo "$RESPONSE" | jq '.'

KEY=$(echo "$RESPONSE" | jq -r '.key')
if [ "$KEY" != "null" ] && [ -n "$KEY" ]; then
  echo ""
  echo "✅ Virtual Key Created:"
  echo "$KEY"
else
  echo ""
  echo "❌ Failed to create key"
fi
```

Run it:
```bash
chmod +x create-key.sh
./create-key.sh
```
