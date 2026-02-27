# LiteLLM API Information

## Quick Reference

### API Base URL
```
Production: https://swzissb82u.us-east-1.awsapprunner.com
Local:       http://localhost:4000
UI:         https://swzissb82u.us-east-1.awsapprunner.com/ui/login/
```

### Master Key (Admin)
```
sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642
```

### Environment Variables
```bash
LITELLM_API_URL=https://swzissb82u.us-east-1.awsapprunner.com
LITELLM_API_KEY=sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642
GOOGLE_API_KEY=AIzaSyDDSkUUl7gmWbqxVaE9iVB2KQzLh9SpwV8
```

### Key Endpoints
- `POST /user/new` - Create user (requires master key)
- `GET /user/info?user_id=<id>` - Get user info (requires master key)
- `POST /key/generate` - Generate virtual key (requires master key)
- `POST /v1/chat/completions` - Chat completion (requires user API key)

### Available Models
- gemini-2.5-pro
- gemini-2.5-flash
- gemini-2.0-flash
- gemini-pro (alias)
- gemini-1.5-pro (alias)
- gemini-1.5-flash (alias)

For complete API reference, see: `litellm-react-app/LITELLM_API_REFERENCE.md`
