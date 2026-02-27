import { NextRequest, NextResponse } from 'next/server';
import { query } from '@/lib/db';
import { verifyToken } from '@/lib/jwt';
import { getTokensFromCookies } from '@/lib/auth-cookies';

export async function GET(request: NextRequest) {
  try {
    const { accessToken } = getTokensFromCookies(request);
    if (!accessToken || !verifyToken(accessToken)) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const result = await query(`
      SELECT 
        id, 
        email, 
        name, 
        created_at, 
        is_active 
      FROM users 
      ORDER BY created_at DESC
    `);

    console.log(`Successfully fetched ${result.rows.length} users`);

    return NextResponse.json({
      users: result.rows.map((user: any) => ({
        id: user.id,
        name: user.name || 'Anonymous User',
        email: user.email,
        joined: user.created_at,
        status: user.is_active ? 'active' : 'inactive'
      }))
    });
  } catch (error: any) {
    console.error('CRITICAL: Error fetching marketplace users:', error.message);
    return NextResponse.json({ 
      error: 'Internal server error',
      details: error.message 
    }, { status: 500 });
  }
}
