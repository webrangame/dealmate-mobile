import { NextRequest, NextResponse } from 'next/server';
import { verifyToken } from '@/lib/jwt';
import { getTokensFromCookies } from '@/lib/auth-cookies';
import { syncAgentsFromS3 } from '@/lib/agents-service';

export async function POST(request: NextRequest) {
    try {
        const { accessToken } = getTokensFromCookies(request);
        if (!accessToken || !verifyToken(accessToken)) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        const result = await syncAgentsFromS3();

        return NextResponse.json(result);
    } catch (error: any) {
        console.error('Error syncing agents:', error);
        return NextResponse.json({
            error: 'Internal server error',
            details: error.message
        }, { status: 500 });
    }
}
