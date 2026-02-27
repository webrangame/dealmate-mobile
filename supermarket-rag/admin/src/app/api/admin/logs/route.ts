import { NextRequest, NextResponse } from 'next/server';
import { query } from '@/lib/db';

export async function GET(request: NextRequest) {
    try {
        const { searchParams } = new URL(request.url);
        const limit = parseInt(searchParams.get('limit') || '50');
        const offset = parseInt(searchParams.get('offset') || '0');

        const sql = `
      SELECT id, timestamp, user_id, query as user_query, response as ai_response, ip_address, metadata
      FROM rag.chat_logs
      ORDER BY timestamp DESC
      LIMIT $1 OFFSET $2
    `;

        const countSql = 'SELECT COUNT(*) FROM rag.chat_logs';

        const [logsResult, countResult] = await Promise.all([
            query(sql, [limit, offset]),
            query(countSql)
        ]);

        return NextResponse.json({
            logs: logsResult.rows,
            total: parseInt(countResult.rows[0].count),
            limit,
            offset
        });
    } catch (error: any) {
        console.error('API Error:', error);
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}
