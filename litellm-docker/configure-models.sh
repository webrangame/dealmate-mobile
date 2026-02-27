#!/bin/bash

MASTER_KEY="sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642"
GOOGLE_API_KEY="AIzaSyB363hm_J0BoJ_EZ8Da_cg0-EBjItKLsA8"
BASE_URL="http://localhost:4000"

echo "🔧 Configuring LiteLLM models with Google API key..."
echo ""

# Configure gemini-1.5-pro
echo "📦 Configuring gemini-1.5-pro..."
curl -s -X POST "${BASE_URL}/model/new" \
  -H "x-litellm-api-key: ${MASTER_KEY}" \
  -H 'Content-Type: application/json' \
  -d "{
    \"model_name\": \"gemini-1.5-pro\",
    \"litellm_params\": {
      \"model\": \"gemini/gemini-1.5-pro\",
      \"api_key\": \"${GOOGLE_API_KEY}\"
    }
  }" | python3 -m json.tool 2>/dev/null || echo "Response received"
echo ""

# Configure gemini-1.5-flash
echo "📦 Configuring gemini-1.5-flash..."
curl -s -X POST "${BASE_URL}/model/new" \
  -H "x-litellm-api-key: ${MASTER_KEY}" \
  -H 'Content-Type: application/json' \
  -d "{
    \"model_name\": \"gemini-1.5-flash\",
    \"litellm_params\": {
      \"model\": \"gemini/gemini-1.5-flash\",
      \"api_key\": \"${GOOGLE_API_KEY}\"
    }
  }" | python3 -m json.tool 2>/dev/null || echo "Response received"
echo ""

echo "✅ Configuration complete!"
echo "🌐 Refresh UI: http://localhost:4000/ui"
