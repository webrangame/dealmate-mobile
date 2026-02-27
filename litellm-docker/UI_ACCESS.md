# LiteLLM Admin Interface Access

## 🌐 Access URLs

### Admin Dashboard (UI)
**URL**: http://localhost:4000/ui

### API Documentation (Swagger)
**URL**: http://localhost:4000/docs

### Health Check
**URL**: http://localhost:4000/health

## 🔐 Authentication

The UI uses the **master key** for authentication:
- **Master Key**: `sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642`

### How to Access

1. **Open your browser** and navigate to:
   ```
   http://localhost:4000/ui
   ```

2. **Enter the master key** when prompted:
   ```
   sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642
   ```

3. **You'll have access to**:
   - User management
   - API key management
   - Usage statistics
   - Budget tracking
   - Model configuration
   - Team management

## 📋 Features Available in UI

### User Management
- View all users
- Create new users
- Edit user settings
- Manage user API keys
- Set user budgets and limits

### API Key Management
- View all API keys
- Create new keys
- Revoke keys
- Set key permissions
- Track key usage

### Analytics & Monitoring
- Usage statistics
- Cost tracking
- Request logs
- Performance metrics
- Error tracking

### Configuration
- Model settings
- Rate limits
- Budget configurations
- Team settings

## 🔧 Setting UI Password (Optional)

To add password protection to the UI, update `docker-compose.yml`:

```yaml
environment:
  UI_PASSWORD: your-secure-password-here
```

Then restart:
```bash
docker-compose restart
```

## 🚀 Quick Access

### From Command Line
```bash
# Open in default browser (Linux)
xdg-open http://localhost:4000/ui

# Or copy the URL
echo "http://localhost:4000/ui"
```

### Direct Links
- **UI Dashboard**: http://localhost:4000/ui
- **API Docs**: http://localhost:4000/docs
- **OpenAPI Spec**: http://localhost:4000/openapi.json

## 📝 Notes

- The UI is enabled by default (`ui: true` in config.yaml)
- No password is set by default (you can add one via `UI_PASSWORD`)
- The master key is required for all admin operations
- The UI provides a visual interface for all API operations

## 🎯 Next Steps

1. Open http://localhost:4000/ui in your browser
2. Enter the master key when prompted
3. Explore the dashboard features
4. Manage users and API keys through the UI
