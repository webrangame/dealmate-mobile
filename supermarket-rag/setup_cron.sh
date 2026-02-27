#!/bin/bash

# Get the absolute path of the backend directory
BACKEND_DIR="/home/ranga/code/pragith/whatssapp-chat/supermarket-rag/backend"
VENV_PYTHON="$BACKEND_DIR/venv/bin/python"
SCRIPT_PATH="$BACKEND_DIR/auto_update_catalogs.py"
LOG_FILE="$BACKEND_DIR/cron_update.log"

# Check if python and script exist
if [ ! -f "$VENV_PYTHON" ]; then
    echo "Error: Virtual environment python not found at $VENV_PYTHON"
    exit 1
fi

if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: Update script not found at $SCRIPT_PATH"
    exit 1
fi

# Define the cron job (Every Sunday at 00:00)
CRON_JOB="0 0 * * 0 cd $BACKEND_DIR && $VENV_PYTHON $SCRIPT_PATH >> $LOG_FILE 2>&1"

# Add to crontab if not already exists
(crontab -l 2>/dev/null | grep -v "$SCRIPT_PATH"; echo "$CRON_JOB") | crontab -

echo "Cron job scheduled: $CRON_JOB"
echo "Logs will be written to $LOG_FILE"
