import { NextRequest, NextResponse } from 'next/server';
import { verifyToken } from '@/lib/jwt';
import { getTokensFromCookies } from '@/lib/auth-cookies';
import { toggleAgentVisibility } from '@/lib/agents-service';

export async function PUT(request: NextRequest) {
    try {
        const { accessToken } = getTokensFromCookies(request);
        if (!accessToken || !verifyToken(accessToken)) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        const { slug, isVisible } = await request.json();

        if (!slug) {
            return NextResponse.json({ error: 'Slug is required' }, { status: 400 });
        }

        const result = await toggleAgentVisibility(slug, isVisible);

        return NextResponse.json(result);
    } catch (error: any) {
        console.error('Error in agent visibility toggle:', error);
        return NextResponse.json({
            error: 'Internal server error',
            details: error.message
        }, { status: 500 });
    }
}
