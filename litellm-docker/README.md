# LiteLLM Docker Setup

This directory contains a Docker setup for running LiteLLM proxy locally.

## Quick Start

1. **Generate a secure master key**:
   ```bash
   openssl rand -hex 32
   ```
   This will generate a key like `sk-abc123...` (add `sk-` prefix)

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and set LITELLM_MASTER_KEY to your generated key
   ```

3. **Update config.yaml**:
   - Update `master_key` in `config.yaml` to match your `.env` file
   - Add your API keys for providers (OpenAI, Anthropic, etc.) if needed

4. **Start LiteLLM**:
   ```bash
   docker-compose up -d
   ```

5. **Check status**:
   ```bash
   docker-compose logs -f
   ```

6. **Access the UI**:
   - Open: http://localhost:4000/ui
   - API Docs: http://localhost:4000/docs

## API Endpoints

- **Health Check**: `GET http://localhost:4000/health`
- **Create User**: `POST http://localhost:4000/user/new`
- **List Keys**: `GET http://localhost:4000/key/list`
- **User Info**: `GET http://localhost:4000/user/info?user_id=123`

## Using the Master Key

All admin operations require the master key in the header:
```bash
curl -X POST 'http://localhost:4000/user/new' \
  -H 'x-litellm-api-key: sk-your-master-key-here' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "123",
    "user_email": "user@example.com",
    "user_alias": "John Doe"
  }'
```

## Environment Variables

- `LITELLM_MASTER_KEY`: Master key for admin operations (must start with `sk-`)
- `DATABASE_URL`: Optional database for persistent user management
- `UI_PASSWORD`: Optional password for UI access
- `OPENAI_API_KEY`: Optional OpenAI API key for testing

## Stopping LiteLLM

```bash
docker-compose down
```

## Viewing Logs

```bash
docker-compose logs -f litellm
```

## Troubleshooting

1. **Port 4000 already in use**:
   - Change port in `docker-compose.yml`: `"4001:4000"`

2. **Master key not working**:
   - Ensure it starts with `sk-`
   - Check that `config.yaml` and `.env` have the same key

3. **Check container status**:
   ```bash
   docker-compose ps
   ```

## Next Steps

Once LiteLLM is running, you can:
1. Test the API with the master key
2. Create users via the API
3. Use this local instance for development
4. Update your agent marketplace to use `http://localhost:4000` instead of the Cloud Run URL
