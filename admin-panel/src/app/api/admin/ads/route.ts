import { NextRequest, NextResponse } from 'next/server';
import { verifyToken } from '@/lib/jwt';
import { getTokensFromCookies } from '@/lib/auth-cookies';
import { getAllAds, uploadAd } from '@/lib/ads-service';

export async function GET(request: NextRequest) {
    try {
        const { accessToken } = getTokensFromCookies(request);
        if (!accessToken || !verifyToken(accessToken)) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        const ads = await getAllAds();
        return NextResponse.json({ ads });
    } catch (error: any) {
        console.error('Error in ads GET:', error);
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}

export async function POST(request: NextRequest) {
    try {
        const { accessToken } = getTokensFromCookies(request);
        if (!accessToken || !verifyToken(accessToken)) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        const formData = await request.formData();
        const file = formData.get('file') as File;
        const agentSlug = formData.get('agentSlug') as string;
        const adType = (formData.get('adType') || 'Hero') as any;
        const targetUrl = formData.get('targetUrl') as string;
        const isPaid = formData.get('isPaid') === 'true';
        const isEnabled = formData.get('isEnabled') === 'true';

        if (!file || !agentSlug) {
            return NextResponse.json({ error: 'Missing required fields' }, { status: 400 });
        }

        const buffer = Buffer.from(await file.arrayBuffer());
        const ad = await uploadAd(buffer, file.name, {
            agent_slug: agentSlug,
            ad_type: adType,
            target_url: targetUrl,
            is_paid: isPaid,
            is_enabled: isEnabled
        });

        return NextResponse.json({ success: true, ad });
    } catch (error: any) {
        console.error('Error in ads POST:', error);
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}
