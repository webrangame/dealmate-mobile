import { NextResponse } from 'next/server';
import { query } from '@/lib/db';
import { S3Client, ListObjectsV2Command } from '@aws-sdk/client-s3';
import { verifyToken } from '@/lib/jwt';
import { getTokensFromCookies } from '@/lib/auth-cookies';

export async function GET(request: Request) {
  try {
    const { accessToken } = getTokensFromCookies(request as any);
    if (!accessToken || !verifyToken(accessToken)) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const health: any = {
      database: { status: 'unknown', details: null },
      s3: { status: 'unknown', details: null },
      litellm: { status: 'unknown', details: null },
      environment: {
        node_env: process.env.NODE_ENV,
        app_url: process.env.NEXT_PUBLIC_APP_URL || 'Not Set',
      }
    };

    // 1. Check Database
    try {
      const dbStart = Date.now();
      await query('SELECT 1');
      health.database.status = 'healthy';
      health.database.latency = `${Date.now() - dbStart}ms`;
    } catch (err: any) {
      health.database.status = 'unhealthy';
      health.database.details = err.message;
    }

    // 2. Check S3
    try {
      const s3Client = new S3Client({
        region: process.env.AWS_REGION || 'us-east-1',
        credentials: {
          accessKeyId: process.env.AWS_ACCESS_KEY_ID || '',
          secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY || '',
        },
      });
      const s3Start = Date.now();
      await s3Client.send(new ListObjectsV2Command({
        Bucket: process.env.AWS_S3_BUCKET_NAME,
        MaxKeys: 1
      }));
      health.s3.status = 'healthy';
      health.s3.latency = `${Date.now() - s3Start}ms`;
    } catch (err: any) {
      health.s3.status = 'unhealthy';
      health.s3.details = err.message;
    }

    // 3. Check LiteLLM
    try {
      const litellmStart = Date.now();
      const res = await fetch(`${process.env.LITELLM_API_URL}/user/list?page_size=1`, {
        headers: {
          'x-litellm-api-key': process.env.LITELLM_API_KEY || ''
        }
      });
      if (res.ok) {
        health.litellm.status = 'healthy';
        health.litellm.latency = `${Date.now() - litellmStart}ms`;
      } else {
        health.litellm.status = 'unhealthy';
        health.litellm.details = `Status: ${res.status}`;
      }
    } catch (err: any) {
      health.litellm.status = 'unhealthy';
      health.litellm.details = err.message;
    }

    return NextResponse.json(health);
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
