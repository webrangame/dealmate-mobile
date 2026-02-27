# Manual Credentials Configuration Guide

## Option 1: Configure via LiteLLM UI

### Steps:

1. **Open LiteLLM UI**: http://localhost:4000/ui

2. **Navigate to Models Page**:
   - Click on "Models" in the sidebar
   - Or go directly to: http://localhost:4000/ui/?page=models

3. **Edit Model Configuration**:
   - Find the model you want to configure (e.g., `gemini-1.5-pro`)
   - Click on the model or the "Edit" button
   - Look for "Credentials" or "API Key" field
   - Enter: `AIzaSyDDSkUUl7gmWbqxVaE9iVB2KQzLh9SpwV8`
   - Save the configuration

4. **Alternative: Add New Model**:
   - Click "Add Model" or "+" button
   - Model Name: `gemini-1.5-pro`
   - Provider: Google / Gemini
   - API Key: `AIzaSyDDSkUUl7gmWbqxVaE9iVB2KQzLh9SpwV8`
   - Save

## Option 2: Configure via API

### Add/Update Model with Credentials

```bash
curl -X POST 'http://localhost:4000/model/new' \
  -H 'x-litellm-api-key: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642' \
  -H 'Content-Type: application/json' \
  -d '{
    "model_name": "gemini-1.5-pro",
    "litellm_params": {
      "model": "gemini/gemini-1.5-pro",
      "api_key": "AIzaSyDDSkUUl7gmWbqxVaE9iVB2KQzLh9SpwV8"
    }
  }'
```

### Update Existing Model

```bash
curl -X PUT 'http://localhost:4000/model/update' \
  -H 'x-litellm-api-key: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642' \
  -H 'Content-Type: application/json' \
  -d '{
    "model_name": "gemini-1.5-pro",
    "litellm_params": {
      "api_key": "AIzaSyDDSkUUl7gmWbqxVaE9iVB2KQzLh9SpwV8"
    }
  }'
```

## Option 3: Update Config File and Restart

Edit `config.yaml` and ensure API keys are set:

```yaml
model_list:
  - model_name: gemini-1.5-pro
    litellm_params:
      model: gemini/gemini-1.5-pro
      api_key: AIzaSyDDSkUUl7gmWbqxVaE9iVB2KQzLh9SpwV8
```

Then restart:
```bash
docker-compose restart litellm
```

## Quick Setup Script

Run this to configure all models:

```bash
cd /home/ranga/code/pragith/whatssapp-chat/litellm-docker

# Configure gemini-1.5-pro
curl -X POST 'http://localhost:4000/model/new' \
  -H 'x-litellm-api-key: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642' \
  -H 'Content-Type: application/json' \
  -d '{
    "model_name": "gemini-1.5-pro",
    "litellm_params": {
      "model": "gemini/gemini-1.5-pro",
      "api_key": "AIzaSyDDSkUUl7gmWbqxVaE9iVB2KQzLh9SpwV8"
    }
  }'

# Configure gemini-1.5-flash
curl -X POST 'http://localhost:4000/model/new' \
  -H 'x-litellm-api-key: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642' \
  -H 'Content-Type: application/json' \
  -d '{
    "model_name": "gemini-1.5-flash",
    "litellm_params": {
      "model": "gemini/gemini-1.5-flash",
      "api_key": "AIzaSyDDSkUUl7gmWbqxVaE9iVB2KQzLh9SpwV8"
    }
  }'
```

## Verify Configuration

Check if credentials are configured:

```bash
curl http://localhost:4000/model/info \
  -H 'x-litellm-api-key: sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642'
```

## Google API Key

Your Google API Key: `AIzaSyDDSkUUl7gmWbqxVaE9iVB2KQzLh9SpwV8`

## Troubleshooting

1. **If UI doesn't show edit option**: Use API method (Option 2)
2. **If API returns error**: Check if model name matches exactly
3. **If still not working**: Check logs: `docker-compose logs litellm`
