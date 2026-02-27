import json

# Load current config
with open("current_config.json", "r") as f:
    config = json.load(f)

# Extract SourceConfiguration
source_config = config["Service"]["SourceConfiguration"]

# Update AWS Credentials in RuntimeEnvironmentVariables
env_vars = source_config["ImageRepository"]["ImageConfiguration"]["RuntimeEnvironmentVariables"]
env_vars["AWS_ACCESS_KEY_ID"] = "AKIAYPJPI6FZ7WKH7WH2"
env_vars["AWS_SECRET_ACCESS_KEY"] = "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"
env_vars["AWS_REGION"] = "us-east-1"  # Ensure usage of us-east-1 (user hinted at region issues before? or simply standard)

# Ensure database URL is correctly preserved (it was proper in the full view I saw earlier)

# Save to update_service.json
with open("update_service.json", "w") as f:
    json.dump(source_config, f, indent=2)

print("Created update_service.json with updated credentials.")
