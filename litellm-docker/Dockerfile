# LiteLLM Dockerfile for AWS Deployment
FROM ghcr.io/berriai/litellm:main-stable



# Set working directory
WORKDIR /app

# Copy config file
COPY config.yaml /app/config.yaml

# Expose port
EXPOSE 4000

# Run LiteLLM with config
# The base image entrypoint is 'litellm', so we just pass arguments
# Format: litellm --config /app/config.yaml --port 4000 --host 0.0.0.0
ENTRYPOINT []
CMD ["litellm", "--config", "/app/config.yaml", "--port", "4000", "--host", "0.0.0.0"]
