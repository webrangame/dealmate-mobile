import { NextRequest, NextResponse } from 'next/server';
import { verifyToken } from '@/lib/jwt';
import { getTokensFromCookies } from '@/lib/auth-cookies';
import { getAllUsersLiteLLMStats } from '@/lib/litellm';

export async function GET(request: NextRequest) {
  try {
    const { accessToken } = getTokensFromCookies(request);
    if (!accessToken || !verifyToken(accessToken)) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const usage = await getAllUsersLiteLLMStats();

    return NextResponse.json({ usage });
  } catch (error: any) {
    console.error('Error fetching token stats:', error);
    return NextResponse.json({ 
      error: 'Internal server error',
      details: error.message 
    }, { status: 500 });
  }
}
