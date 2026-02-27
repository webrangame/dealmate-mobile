# LiteLLM UI Credentials

## Default Access

If the UI is asking for username and password, try these options:

### Option 1: Use Master Key as Password

**Username**: `admin` (or leave blank)  
**Password**: `sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642`

### Option 2: Disable Password (Current Setup)

The UI password has been disabled. If you're still seeing a login prompt:

1. **Clear browser cache** and try again
2. **Use incognito/private mode**
3. **Try accessing directly**: http://localhost:4000/ui

### Option 3: Set Custom Password

If you want to set a custom password, update `.env`:

```bash
UI_PASSWORD=your-password-here
```

Then update `docker-compose.yml`:
```yaml
UI_PASSWORD: ${UI_PASSWORD:-your-password-here}
```

Restart:
```bash
docker-compose restart
```

## Troubleshooting

### If Login Still Required

1. **Check if UI_PASSWORD is set**:
   ```bash
   docker-compose exec litellm env | grep UI_PASSWORD
   ```

2. **Remove UI_PASSWORD completely**:
   - Remove from `docker-compose.yml`
   - Restart container

3. **Access via API key in URL**:
   ```
   http://localhost:4000/ui?api_key=sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642
   ```

## Current Configuration

- **UI Enabled**: Yes (`ui: true` in config.yaml)
- **UI Password**: Disabled (no password set)
- **Master Key**: `sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642`

## Quick Access

Try these URLs:
- http://localhost:4000/ui
- http://localhost:4000/ui?api_key=sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642
