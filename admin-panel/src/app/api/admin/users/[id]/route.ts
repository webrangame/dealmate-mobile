import { NextRequest, NextResponse } from 'next/server';
import { query } from '@/lib/db';
import { verifyToken } from '@/lib/jwt';
import { getTokensFromCookies } from '@/lib/auth-cookies';
import { getUserLiteLLMStats } from '@/lib/litellm';

export async function GET(
  request: NextRequest, 
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const { accessToken } = getTokensFromCookies(request);
    if (!accessToken || !verifyToken(accessToken)) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // 1. Fetch basic user info
    const userResult = await query(`
      SELECT id, email, name, created_at, is_active 
      FROM users WHERE id = $1
    `, [id]);
    
    const user = userResult.rows[0];
    if (!user) {
      return NextResponse.json({ error: 'User not found' }, { status: 404 });
    }

    // 2. Fetch purchased agents
    const purchasesResult = await query(`
      SELECT agent_id, agent_name, purchased_at 
      FROM user_purchases WHERE user_id = $1 ORDER BY purchased_at DESC
    `, [id]);

    // 3. Fetch LiteLLM stats - Try by ID first, then by email
    let litellmStats = await getUserLiteLLMStats(id);
    if (!litellmStats && user.email) {
      litellmStats = await getUserLiteLLMStats(user.email);
    }

    return NextResponse.json({
      user: {
        id: user.id,
        name: user.name || 'Anonymous',
        email: user.email,
        joined: user.created_at,
        status: user.is_active ? 'active' : 'inactive',
      },
      purchases: purchasesResult.rows.map((p: any) => ({
        id: p.agent_id,
        name: p.agent_name,
        purchasedAt: p.purchased_at
      })),
      tokenInfo: litellmStats ? {
        spend: `$${(litellmStats.user_info?.spend || litellmStats.total_spend || 0).toFixed(2)}`,
        rawSpend: litellmStats.user_info?.spend || litellmStats.total_spend || 0,
        totalTokens: litellmStats.user_info?.total_tokens || litellmStats.total_events || 0,
        budget: litellmStats.user_info?.max_budget || litellmStats.max_budget || 0,
      } : null
    });
  } catch (error: any) {
    console.error('Error fetching user detail:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

// Update user status (Revoke/Activate)
export async function PATCH(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const { accessToken } = getTokensFromCookies(request);
    if (!accessToken || !verifyToken(accessToken)) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const { status } = await request.json();
    const isActive = status === 'active';

    const result = await query(
      'UPDATE users SET is_active = $1 WHERE id = $2 RETURNING id',
      [isActive, id]
    );

    if (result.rowCount === 0) {
      return NextResponse.json({ error: 'User not found' }, { status: 404 });
    }

    return NextResponse.json({ success: true, status });
  } catch (error: any) {
    console.error('Error updating user status:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
