#!/bin/bash

# Enable strict error handling
set -e

echo "=== Supermarket RAG Local LLM Installer ==="
echo "This script will set up the local AI environment."

# 1. Check for Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed."
    echo "Please install Docker Desktop for your OS: https://www.docker.com/products/docker-desktop/"
    exit 1
fi

echo "✅ Docker found."

# 2. Build and Start Services
echo "🚀 Starting services (this may take a few minutes the first time)..."
docker-compose up -d --build

# 3. Wait for Ollama to be ready
echo "⏳ Waiting for Ollama to start..."
until docker-compose exec ollama curl -s http://localhost:11434 > /dev/null; do
    printf "."
    sleep 2
done
echo ""
echo "✅ Ollama is ready."

# 4. Pull the Model
MODEL="llama3.1:8b"
echo "⬇️ Pulling AI Model: $MODEL (Size: ~4.7GB)"
echo "This makes the AI work offline. Please wait..."

docker-compose exec ollama ollama pull $MODEL

echo ""
echo "📂 Ingesting Local Data (Coles.pdf)..."
docker-compose exec -T backend python3 ingest_local.py

echo ""
echo "✅ Setup Complete!"
echo "-----------------------------------"
echo "API URL:      http://localhost:8001"
echo "Frontend URL: http://localhost:3001"
echo "-----------------------------------"
echo "To stop later, run: ./stop.sh"
