import { NextRequest, NextResponse } from 'next/server';
import { query } from '@/lib/db';

export async function PATCH(
    request: NextRequest,
    context: { params: Promise<{ id: string }> }
) {
    try {
        const { id } = await context.params;
        const body = await request.json();
        const { text, is_enabled } = body;

        let sql = 'UPDATE rag.data_supermarket_docs SET updated_at = CURRENT_TIMESTAMP';
        const queryParams = [];
        let paramCount = 1;

        if (text !== undefined) {
            sql += `, text = $${paramCount++}`;
            queryParams.push(text);
        }

        if (is_enabled !== undefined) {
            sql += `, is_enabled = $${paramCount++}`;
            queryParams.push(is_enabled);
        }

        sql += ` WHERE id = $${paramCount++} RETURNING id`;
        queryParams.push(id);

        const result = await query(sql, queryParams);

        if (result.rowCount === 0) {
            return NextResponse.json({ error: 'Product not found' }, { status: 404 });
        }

        return NextResponse.json({ success: true, id: result.rows[0].id });
    } catch (error: any) {
        console.error('API Error:', error);
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}
