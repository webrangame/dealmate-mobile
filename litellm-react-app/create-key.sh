#!/bin/bash

# Script to create a LiteLLM virtual key
# Usage: ./create-key.sh [user_id]

MASTER_KEY="sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642"
USER_ID="${1:-admin}"
API_URL="https://swzissb82u.us-east-1.awsapprunner.com"

echo "🔑 Creating LiteLLM Virtual Key"
echo "================================"
echo "User ID: $USER_ID"
echo ""

RESPONSE=$(curl -s -X POST "$API_URL/key/generate" \
  -H "x-litellm-api-key: $MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"user_id\": \"$USER_ID\",
    \"duration\": null,
    \"key_alias\": \"Key created via script\",
    \"tpm_limit\": 100000,
    \"rpm_limit\": 100
  }")

# Check if jq is available
if command -v jq &> /dev/null; then
  echo "Response:"
  echo "$RESPONSE" | jq '.'
  KEY=$(echo "$RESPONSE" | jq -r '.key')
else
  echo "Response:"
  echo "$RESPONSE"
  KEY=$(echo "$RESPONSE" | grep -o '"key":"[^"]*"' | cut -d'"' -f4)
fi

if [ "$KEY" != "null" ] && [ -n "$KEY" ] && [ "$KEY" != "" ]; then
  echo ""
  echo "✅ Virtual Key Created Successfully!"
  echo ""
  echo "🔑 Your Virtual Key (save this!):"
  echo "$KEY"
  echo ""
  echo "⚠️  Note: This key is only shown once. Save it securely!"
else
  echo ""
  echo "❌ Failed to create key"
  echo "Response: $RESPONSE"
  exit 1
fi
