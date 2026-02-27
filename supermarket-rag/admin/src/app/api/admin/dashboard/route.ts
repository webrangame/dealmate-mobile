import { NextRequest, NextResponse } from 'next/server';
import { query } from '@/lib/db';

export async function GET(request: NextRequest) {
    try {
        const productsCountSql = 'SELECT COUNT(*) FROM rag.data_supermarket_docs';
        const logsTodaySql = "SELECT COUNT(*) FROM rag.chat_logs WHERE timestamp > CURRENT_DATE";
        const disabledCountSql = 'SELECT COUNT(*) FROM rag.data_supermarket_docs WHERE is_enabled = FALSE';

        const [productsRes, logsRes, disabledRes] = await Promise.all([
            query(productsCountSql),
            query(logsTodaySql),
            query(disabledCountSql)
        ]);

        return NextResponse.json({
            totalProducts: parseInt(productsRes.rows[0].count),
            logsToday: parseInt(logsRes.rows[0].count),
            disabledProducts: parseInt(disabledRes.rows[0].count),
            status: 'Optimal'
        });
    } catch (error: any) {
        console.error('API Error:', error);
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}
