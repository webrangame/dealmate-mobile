// Script to create LiteLLM database
import { Pool } from 'pg';

const pool = new Pool({
  host: 'agent-marketplace-db.cmt466aga8u0.us-east-1.rds.amazonaws.com',
  port: 5432,
  user: 'postgres',
  password: 'it371Ananda',
  database: 'postgres',
  ssl: {
    rejectUnauthorized: false
  }
});

async function createDatabase() {
  try {
    const client = await pool.connect();
    
    // Check if database exists
    const checkResult = await client.query(
      "SELECT 1 FROM pg_database WHERE datname = 'litellm_db'"
    );
    
    if (checkResult.rows.length === 0) {
      // Create database
      await client.query('CREATE DATABASE litellm_db');
      console.log('✅ Database "litellm_db" created successfully!');
    } else {
      console.log('✅ Database "litellm_db" already exists!');
    }
    
    client.release();
    await pool.end();
  } catch (error: any) {
    console.error('❌ Error creating database:', error.message);
    process.exit(1);
  }
}

createDatabase();
