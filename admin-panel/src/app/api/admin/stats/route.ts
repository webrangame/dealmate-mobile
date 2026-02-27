import { NextRequest, NextResponse } from 'next/server';
import { query } from '@/lib/db';
import { verifyToken } from '@/lib/jwt';
import { getTokensFromCookies } from '@/lib/auth-cookies';
import { getActiveAgentsCount } from '@/lib/s3';
import { getAllUsersLiteLLMStats } from '@/lib/litellm';

export async function GET(request: NextRequest) {
  try {
    const { accessToken } = getTokensFromCookies(request);
    if (!accessToken || !verifyToken(accessToken)) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // 1. Total Users
    const usersCount = await query('SELECT COUNT(*) FROM users');
    
    // 2. Total Purchases
    const purchasesCount = await query('SELECT COUNT(*) FROM user_purchases');

    // 3. Active Agents from S3
    const agentsCount = await getActiveAgentsCount();

    // 4. Registration trends (last 14 days)
    const registrationData = await query(`
      SELECT 
        TO_CHAR(created_at, 'YYYY-MM-DD') as date,
        COUNT(*) as count
      FROM users 
      WHERE created_at >= CURRENT_DATE - INTERVAL '14 days'
      GROUP BY date
      ORDER BY date
    `);

    // 5. Purchase trends (last 14 days)
    const purchaseData = await query(`
      SELECT 
        TO_CHAR(purchased_at, 'YYYY-MM-DD') as date,
        COUNT(*) as count
      FROM user_purchases 
      WHERE purchased_at >= CURRENT_DATE - INTERVAL '14 days'
      GROUP BY date
      ORDER BY date
    `);

    // 6. Recent Activity (last 10 user signups)
    const recentUsers = await query(`
      SELECT 'USER' as type, name as text, created_at as time 
      FROM users ORDER BY created_at DESC LIMIT 10
    `);

    // 7. Token Usage & Top Consumers form LiteLLM
    let tokenUsage = '0';
    let tokenConsumptionData: any[] = [];
    
    try {
      const litellmUsers = await getAllUsersLiteLLMStats();
      if (litellmUsers && Array.isArray(litellmUsers)) {
        // Calculate total tokens
        const totalTokens = litellmUsers.reduce((acc, user) => acc + (user.total_tokens || 0), 0);
        
        // Format token usage
        if (totalTokens >= 1000000) {
          tokenUsage = `${(totalTokens / 1000000).toFixed(1)}M`;
        } else if (totalTokens >= 1000) {
          tokenUsage = `${(totalTokens / 1000).toFixed(1)}K`;
        } else {
          tokenUsage = totalTokens.toString();
        }

        // Get Top 5 Consumers by Spend
        tokenConsumptionData = litellmUsers
          .sort((a, b) => (b.spend || 0) - (a.spend || 0))
          .slice(0, 5)
          .map(user => ({
            name: user.user_alias || user.user_email || user.user_id,
            spend: user.spend || 0,
            tokens: user.total_tokens || 0
          }));
      }
    } catch (err) {
      console.error('Failed to fetch LiteLLM stats within dashboard:', err);
    }

    return NextResponse.json({
      stats: {
        totalUsers: usersCount.rows[0].count,
        totalPurchases: purchasesCount.rows[0].count,
        activeAgents: agentsCount,
        tokenUsage: tokenUsage, 
      },
      registrationData: registrationData.rows,
      purchaseData: purchaseData.rows,
      tokenConsumptionData: tokenConsumptionData,
      recentEvents: recentUsers.rows.map((row: any) => ({
        type: row.type,
        text: `New user: ${row.text || 'Anonymous'}`,
        time: row.time
      }))
    });
  } catch (error: any) {
    console.error('Error fetching dashboard stats:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
