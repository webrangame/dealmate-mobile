import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function setAuthCookies(response: NextResponse, tokens: { accessToken: string; refreshToken: string }) {
  const isProd = process.env.NODE_ENV === 'production';
  
  const commonOptions = {
    httpOnly: true,
    secure: isProd,
    sameSite: 'lax' as const,
    path: '/',
  };

  response.cookies.set('adminAccessToken', tokens.accessToken, {
    ...commonOptions,
    maxAge: 60 * 60, // 1 hour
  });

  response.cookies.set('adminRefreshToken', tokens.refreshToken, {
    ...commonOptions,
    maxAge: 60 * 60 * 24 * 7, // 7 days
  });
}

export function clearAuthCookies(response: NextResponse) {
  response.cookies.set('adminAccessToken', '', { maxAge: 0, path: '/' });
  response.cookies.set('adminRefreshToken', '', { maxAge: 0, path: '/' });
}

export function getTokensFromCookies(request: NextRequest) {
  const accessToken = request.cookies.get('adminAccessToken')?.value || null;
  const refreshToken = request.cookies.get('adminRefreshToken')?.value || null;
  
  return { accessToken, refreshToken };
}
