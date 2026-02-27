process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
import { query } from '../src/lib/db';
import * as dotenv from 'dotenv';
import { join } from 'path';

// Load environment variables
dotenv.config({ path: join(process.cwd(), '.env.local') });

async function createAdsTable() {
    try {
        console.log('🚀 Creating ads table...');

        await query(`
      CREATE TABLE IF NOT EXISTS ads (
        id SERIAL PRIMARY KEY,
        agent_slug VARCHAR(255) NOT NULL,
        image_url TEXT NOT NULL,
        target_url TEXT NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
      );
    `);

        await query(`
      CREATE INDEX IF NOT EXISTS idx_ads_agent_slug ON ads(agent_slug);
    `);

        console.log('✅ Ads table created successfully!');
    } catch (err) {
        console.error('❌ Failed to create ads table:', err);
    } finally {
        process.exit(0);
    }
}

createAdsTable();
