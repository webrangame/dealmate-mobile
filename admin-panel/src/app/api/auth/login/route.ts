import { NextRequest, NextResponse } from 'next/server';
import { query } from '@/lib/db';
import * as bcrypt from 'bcryptjs';
import { generateTokens } from '@/lib/jwt';
import { setAuthCookies } from '@/lib/auth-cookies';

export async function POST(request: NextRequest) {
  try {
    const { email, password } = await request.json();

    if (!email || !password) {
      return NextResponse.json({ error: 'Email and password are required' }, { status: 400 });
    }

    // Check in admin_users table
    const result = await query('SELECT * FROM admin_users WHERE email = $1 AND is_active = true', [email]);
    const admin = result.rows[0];

    if (!admin || !await bcrypt.compare(password, admin.password_hash)) {
      return NextResponse.json({ error: 'Invalid credentials' }, { status: 401 });
    }

    const tokens = generateTokens({
      userId: admin.id,
      email: admin.email,
      name: admin.name
    });

    const response = NextResponse.json({
      message: 'Login successful',
      user: {
        id: admin.id,
        email: admin.email,
        name: admin.name
      }
    });

    setAuthCookies(response, tokens);
    return response;
  } catch (error: any) {
    console.error('Login error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
