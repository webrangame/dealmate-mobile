import { NextRequest, NextResponse } from 'next/server';
import { verifyToken } from '@/lib/jwt';
import { getTokensFromCookies } from '@/lib/auth-cookies';
import { updateAd, deleteAd } from '@/lib/ads-service';

export async function PUT(
    request: NextRequest,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const { id: idParam } = await params;
        const { accessToken } = getTokensFromCookies(request);
        if (!accessToken || !verifyToken(accessToken)) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        const id = parseInt(idParam);
        const body = await request.json();

        const ad = await updateAd(id, body);
        return NextResponse.json({ success: true, ad });
    } catch (error: any) {
        console.error(`Error in ads PUT:`, error);
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}

export async function DELETE(
    request: NextRequest,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const { id: idParam } = await params;
        const { accessToken } = getTokensFromCookies(request);
        if (!accessToken || !verifyToken(accessToken)) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        const id = parseInt(idParam);
        const result = await deleteAd(id);
        return NextResponse.json(result);
    } catch (error: any) {
        console.error(`Error in ads DELETE:`, error);
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}
