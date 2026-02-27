import { NextRequest, NextResponse } from 'next/server';
import { query } from '@/lib/db';

export async function GET(request: NextRequest) {
    try {
        const { searchParams } = new URL(request.url);
        const shop = searchParams.get('shop');

        let sql = 'SELECT id, text, metadata_, is_enabled, updated_at FROM rag.data_supermarket_docs';
        const params = [];

        if (shop) {
            sql += " WHERE metadata_->>'shop_name' = $1";
            params.push(shop);
        }

        sql += ' ORDER BY updated_at DESC LIMIT 100';

        console.log('Fetching products with SQL:', sql);
        const result = await query(sql, params);
        return NextResponse.json(result.rows);
    } catch (error: any) {
        console.error('DATABASE API Error:', error);
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}

export async function POST(request: NextRequest) {
    try {
        const body = await request.json();
        const { text, shop_name, metadata = {} } = body;

        if (!text || !shop_name) {
            return NextResponse.json({ error: 'Text and Shop Name are required' }, { status: 400 });
        }

        // Placeholder for embedding until we find a 384-dim remote provider
        // In a real scenario, we would call an embedding service here.
        const dummyEmbedding = Array(384).fill(0);

        const fullMetadata = {
            ...metadata,
            shop_name,
            added_via: 'admin_panel',
            updated_at: new Date().toISOString()
        };

        const sql = `
      INSERT INTO rag.data_supermarket_docs (text, metadata_, embedding, is_enabled, updated_at)
      VALUES ($1, $2, $3, $4, CURRENT_TIMESTAMP)
      RETURNING id
    `;

        const result = await query(sql, [text, fullMetadata, JSON.stringify(dummyEmbedding), true]);

        return NextResponse.json({ success: true, id: result.rows[0].id });
    } catch (error: any) {
        console.error('API Error:', error);
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}
