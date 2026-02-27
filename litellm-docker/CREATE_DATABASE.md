# Create LiteLLM Database

## Quick Steps

### Option 1: Using psql (if installed)

```bash
PGPASSWORD=it371Ananda psql \
  -h agent-marketplace-db.cmt466aga8u0.us-east-1.rds.amazonaws.com \
  -p 5432 \
  -U postgres \
  -d postgres \
  -c "CREATE DATABASE litellm_db;"
```

### Option 2: Using AWS Console + Database Client

1. **Connect to your RDS instance** using:
   - DBeaver
   - pgAdmin
   - psql
   - Any PostgreSQL client

2. **Connection Details**:
   - Host: `agent-marketplace-db.cmt466aga8u0.us-east-1.rds.amazonaws.com`
   - Port: `5432`
   - Database: `postgres`
   - User: `postgres`
   - Password: `it371Ananda`

3. **Run SQL**:
   ```sql
   CREATE DATABASE litellm_db;
   ```

### Option 3: Using AWS RDS Data API (if enabled)

```bash
# First, get your DB cluster ARN
DB_CLUSTER_ARN=$(aws rds describe-db-instances \
  --db-instance-identifier agent-marketplace-db \
  --query 'DBInstances[0].DBClusterIdentifier' \
  --output text)

# Then execute SQL (requires RDS Data API to be enabled)
aws rds-data execute-statement \
  --resource-arn $DB_CLUSTER_ARN \
  --secret-arn <SECRET_ARN> \
  --database postgres \
  --sql "CREATE DATABASE litellm_db;"
```

## Verify Database Created

```bash
PGPASSWORD=it371Ananda psql \
  -h agent-marketplace-db.cmt466aga8u0.us-east-1.rds.amazonaws.com \
  -p 5432 \
  -U postgres \
  -d postgres \
  -c "\l" | grep litellm_db
```

## Database Connection String

After creation, use this connection string:

```
postgresql://postgres:it371Ananda@agent-marketplace-db.cmt466aga8u0.us-east-1.rds.amazonaws.com:5432/litellm_db?sslmode=require
```

This is already added to your `.env.local` file!
