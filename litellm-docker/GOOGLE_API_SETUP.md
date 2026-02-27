# Google API Key Configuration for LiteLLM

## ✅ Configuration Complete

Google API key has been configured for LiteLLM to use Google Gemini models.

### API Key
- **Key**: `AIzaSyDDSkUUl7gmWbqxVaE9iVB2KQzLh9SpwV8`
- **Provider**: Google (Gemini)
- **Status**: Configured in Docker environment

### Available Models

The following Google Gemini models are now available:

1. **gemini/gemini-pro** - Standard Gemini Pro model
2. **gemini/gemini-1.5-pro** - Latest Gemini 1.5 Pro
3. **gemini/gemini-1.5-flash** - Fast Gemini 1.5 Flash

## Testing

### List Available Models
```bash
curl http://localhost:4000/v1/models \
  -H 'x-litellm-api-key: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642'
```

### Test Chat Completion
```bash
curl http://localhost:4000/v1/chat/completions \
  -H 'x-litellm-api-key: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "gemini/gemini-pro",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```

## Configuration Files

### docker-compose.yml
```yaml
environment:
  GOOGLE_API_KEY: AIzaSyDDSkUUl7gmWbqxVaE9iVB2KQzLh9SpwV8
```

### config.yaml
```yaml
model_list:
  - model_name: gemini/gemini-pro
    litellm_params:
      model: gemini/gemini-pro
      api_key: os.environ/GOOGLE_API_KEY
```

## Usage in Your Application

### Using LiteLLM Proxy with Google Models

```javascript
// Example: Using Gemini via LiteLLM proxy
const response = await fetch('http://localhost:4000/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'x-litellm-api-key': 'sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642'
  },
  body: JSON.stringify({
    model: 'gemini/gemini-pro',
    messages: [
      { role: 'user', content: 'Your message here' }
    ]
  })
});
```

### Using User API Keys

Users created in LiteLLM can use their own API keys:

```javascript
const response = await fetch('http://localhost:4000/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer sk-user-api-key-here' // User's API key
  },
  body: JSON.stringify({
    model: 'gemini/gemini-pro',
    messages: [
      { role: 'user', content: 'Your message here' }
    ]
  })
});
```

## Security Notes

⚠️ **Important**:
- The Google API key is stored in environment variables
- Never commit API keys to git
- Rotate keys if compromised
- Monitor usage in Google Cloud Console

## Next Steps

1. ✅ Google API key configured
2. ✅ Models added to config
3. ✅ LiteLLM restarted
4. 🧪 Test models via API
5. 📊 Monitor usage in LiteLLM UI

## Access

- **LiteLLM UI**: http://localhost:4000/ui
- **API Endpoint**: http://localhost:4000/v1/chat/completions
- **Models List**: http://localhost:4000/v1/models
