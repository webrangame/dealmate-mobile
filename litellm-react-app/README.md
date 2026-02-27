# LiteLLM React Application

A sample React application to interact with LiteLLM proxy API.

## Features

- 🔐 **Authentication**: Login with LiteLLM UI credentials
- 💬 **Chat Interface**: Interactive chat with multiple Gemini models
- 📊 **Dashboard**: View API keys, token usage, and user information
- 🔑 **API Key Management**: Copy and use your LiteLLM API keys
- 📈 **Usage Tracking**: Monitor token usage and spending

## Quick Start

### 1. Install Dependencies

```bash
cd litellm-react-app
npm install
```

### 2. Configure LiteLLM URL

The app is pre-configured to use:
- **LiteLLM API URL**: `https://swzissb82u.us-east-1.awsapprunner.com`
- **Default Username**: `admin`
- **Default Password**: Master key (for UI login)

### 3. Run the Application

```bash
npm run dev
```

The app will open at `http://localhost:3001`

## Usage

### Login

1. Enter username: `admin`
2. Enter password/master key: Your LiteLLM master key
3. Click "Login"

**Note**: The app will attempt to get your user API key from LiteLLM. If you don't have a user account, you may need to create one first via the LiteLLM API.

### Using the Chat Interface

1. Select a model from the dropdown (e.g., `gemini-2.5-pro`)
2. Type your message in the input field
3. Press Enter or click "Send"
4. View the assistant's response

### Available Models

- `gemini-2.5-pro` - Latest Gemini Pro model
- `gemini-2.5-flash` - Fast Gemini Flash model
- `gemini-2.0-flash` - Gemini 2.0 Flash
- `gemini-pro` (alias)
- `gemini-1.5-pro` (alias)
- `gemini-1.5-flash` (alias)

## Project Structure

```
litellm-react-app/
├── src/
│   ├── components/
│   │   ├── Login.jsx          # Login component
│   │   ├── Dashboard.jsx      # User dashboard with API keys and usage
│   │   └── ChatInterface.jsx  # Chat interface
│   ├── App.jsx                # Main app component
│   ├── App.css                # App styles
│   ├── main.jsx               # Entry point
│   └── index.css              # Global styles
├── index.html
├── package.json
├── vite.config.js
└── README.md
```

## API Integration

### Making Chat Requests

```javascript
const response = await fetch('https://swzissb82u.us-east-1.awsapprunner.com/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'gemini-2.5-pro',
    messages: [
      { role: 'user', content: 'Hello!' }
    ],
    temperature: 0.7,
    max_tokens: 1000,
  }),
})
```

### Getting User Info

```javascript
const response = await fetch(
  'https://swzissb82u.us-east-1.awsapprunner.com/user/info?user_id=YOUR_USER_ID',
  {
    headers: {
      'x-litellm-api-key': 'YOUR_MASTER_KEY',
    },
  }
)
```

## Environment Variables

You can customize the LiteLLM URL by creating a `.env` file:

```bash
VITE_LITELLM_API_URL=https://swzissb82u.us-east-1.awsapprunner.com
```

Then update `App.jsx` to use:
```javascript
const LITELLM_API_URL = import.meta.env.VITE_LITELLM_API_URL || 'https://swzissb82u.us-east-1.awsapprunner.com'
```

## Building for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

## Troubleshooting

### "No API keys found for user"
- Make sure you're using the correct master key
- The user account may need to be created first
- Check that `auto_create_key: true` was set when creating the user

### "Authentication failed"
- Verify the master key is correct
- Check that the LiteLLM service is running
- Ensure the API URL is correct

### CORS Errors
- LiteLLM proxy should handle CORS automatically
- If issues persist, check LiteLLM configuration

## Security Notes

- ⚠️ **Never commit API keys** to version control
- 🔒 Store API keys securely (localStorage is used for demo only)
- 🛡️ In production, use secure backend to manage API keys
- 🔐 Master keys should only be used server-side

## License

MIT
