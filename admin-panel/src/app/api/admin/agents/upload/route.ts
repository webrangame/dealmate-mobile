import { NextRequest, NextResponse } from 'next/server';
import { verifyToken } from '@/lib/jwt';
import { getTokensFromCookies } from '@/lib/auth-cookies';
import { uploadAgentZip } from '@/lib/agents-service';

export async function POST(request: NextRequest) {
    try {
        const { accessToken } = getTokensFromCookies(request);
        if (!accessToken || !verifyToken(accessToken)) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        const formData = await request.formData();
        const file = formData.get('file') as File;

        if (!file) {
            return NextResponse.json({ error: 'No file uploaded' }, { status: 400 });
        }

        if (!file.name.endsWith('.zip')) {
            return NextResponse.json({ error: 'Only ZIP files are allowed' }, { status: 400 });
        }

        const buffer = Buffer.from(await file.arrayBuffer());
        const result = await uploadAgentZip(buffer, file.name);

        return NextResponse.json(result);
    } catch (error: any) {
        console.error('Error in agent upload:', error);
        return NextResponse.json({
            error: 'Internal server error',
            details: error.message
        }, { status: 500 });
    }
}
