# Model Configuration Fix

## Problem
Error: `models/gemini-1.5-pro is not found` or `models/gemini-pro is not found`

## Solution
Updated to use the latest available Gemini models from Google API.

## Available Models (Verified)
- ✅ `gemini-2.5-pro` - Latest Pro model
- ✅ `gemini-2.5-flash` - Latest Flash model  
- ✅ `gemini-2.0-flash` - Stable Flash model
- ✅ `gemini-pro-latest` - Alias for latest Pro
- ✅ `gemini-flash-latest` - Alias for latest Flash

## Configuration

### config.yaml
```yaml
model_list:
  - model_name: gemini-2.5-pro
    litellm_params:
      model: gemini/gemini-2.5-pro
      api_key: AIzaSyDDSkUUl7gmWbqxVaE9iVB2KQzLh9SpwV8
  
  - model_name: gemini-2.5-flash
    litellm_params:
      model: gemini/gemini-2.5-flash
      api_key: AIzaSyDDSkUUl7gmWbqxVaE9iVB2KQzLh9SpwV8
```

## Testing

Test the connection:
```bash
curl http://localhost:4000/v1/chat/completions \
  -H 'x-litellm-api-key: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "gemini-2.5-flash",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

## UI Configuration

In the LiteLLM UI:
1. Go to Models page
2. Use model name: `gemini-2.5-flash` or `gemini-2.5-pro`
3. API Key: `AIzaSyDDSkUUl7gmWbqxVaE9iVB2KQzLh9SpwV8`
4. Test connection should work now!
