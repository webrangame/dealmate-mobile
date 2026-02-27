#!/bin/bash
# Daily Catalog Update - Cron Job Setup Script
# Run this once to set up automatic daily catalog updates

BACKEND_DIR="/home/ranga/code/pragith/whatssapp-chat/supermarket-rag/backend"
LOG_FILE="$BACKEND_DIR/catalog_update.log"

# Cron job to run every day at 8:00 AM
CRON_SCHEDULE="0 8 * * * cd $BACKEND_DIR && /usr/bin/python3 auto_update_catalogs.py >> $LOG_FILE 2>&1"

echo "Setting up daily catalog update automation..."
echo ""
echo "This will add a cron job to run auto_update_catalogs.py every day at 8:00 AM"
echo "Log file: $LOG_FILE"
echo ""
echo "Cron schedule: $CRON_SCHEDULE"
echo ""

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "auto_update_catalogs.py"; then
    echo "⚠️  Cron job already exists. Removing old entry..."
    crontab -l 2>/dev/null | grep -v "auto_update_catalogs.py" | crontab -
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_SCHEDULE") | crontab -

echo "✅ Cron job added successfully!"
echo ""
echo "To verify:"
echo "  crontab -l"
echo ""
echo "To view logs:"
echo "  tail -f $LOG_FILE"
echo ""
echo "To remove:"
echo "  crontab -e  # Then delete the line with 'auto_update_catalogs.py'"
echo ""
echo "Next run: Tomorrow at 8:00 AM (or manually run: python3 auto_update_catalogs.py)"
