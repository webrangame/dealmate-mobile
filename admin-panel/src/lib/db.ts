import { Pool } from 'pg';

let pool: Pool | null = null;

function getPool(): Pool {
  if (!pool) {
    const connectionString = process.env.DATABASE_URL;
    
    if (!connectionString) {
      throw new Error('DATABASE_URL environment variable is not set');
    }

    const needsSSL = connectionString.includes('sslmode=require') || process.env.DB_SSL === 'true';
    
    // Clean connection string
    let cleanURL = connectionString.replace(/[?&]sslmode=[^&]*/, '');
    cleanURL = cleanURL.replace(/\?\?+/g, '?').replace(/&&+/g, '&').replace(/\?$/, '');
    
    pool = new Pool({
      connectionString: cleanURL,
      ssl: needsSSL ? { rejectUnauthorized: false } : false,
      max: 10,
      idleTimeoutMillis: 30000,
    });

    pool.on('error', (err) => {
      console.error('Unexpected error on idle database client', err);
    });
  }

  return pool;
}

export async function query(text: string, params?: any[]) {
  const client = getPool();
  return client.query(text, params);
}

export async function getClient() {
  return getPool().connect();
}

export default getPool;
