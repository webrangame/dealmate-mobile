#!/bin/bash

# Create LiteLLM database on existing RDS instance
set -e

echo "🗄️  Creating LiteLLM Database"
echo "=============================="
echo ""

# Database connection details
DB_HOST="agent-marketplace-db.cmt466aga8u0.us-east-1.rds.amazonaws.com"
DB_PORT="5432"
DB_USER="postgres"
DB_PASSWORD="it371Ananda"
DB_NAME="litellm_db"

echo "📝 Database Details:"
echo "   Host: $DB_HOST"
echo "   Port: $DB_PORT"
echo "   User: $DB_USER"
echo "   Database: $DB_NAME"
echo ""

# Check if psql is available
if ! command -v psql &> /dev/null; then
    echo "⚠️  psql not found. Installing PostgreSQL client..."
    echo "   Please install: sudo apt-get install postgresql-client"
    echo ""
    echo "📝 Or create database manually:"
    echo "   Connect to your RDS instance and run:"
    echo "   CREATE DATABASE litellm_db;"
    exit 1
fi

echo "🔌 Connecting to database..."
echo ""

# Create database
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d postgres << EOF
-- Create database if it doesn't exist
SELECT 'CREATE DATABASE $DB_NAME'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME')\gexec
EOF

if [ $? -eq 0 ]; then
    echo "✅ Database '$DB_NAME' created successfully!"
    echo ""
    echo "📝 Connection String:"
    echo "   postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME?sslmode=require"
    echo ""
else
    echo "⚠️  Database might already exist or connection failed"
    echo "   Please check manually"
fi
