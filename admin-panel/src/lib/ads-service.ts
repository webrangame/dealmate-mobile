import { query } from './db';
import { getS3Client } from './s3';
import { PutObjectCommand, DeleteObjectCommand } from '@aws-sdk/client-s3';
import path from 'path';

const BUCKET_NAME = process.env.AWS_S3_BUCKET_NAME || 'agent-marketplace-agents';

export type AdType = 'Hero' | 'Square' | 'Billboard';

export interface AdData {
    id?: number;
    agent_slug: string;
    image_url: string;
    target_url?: string;
    is_paid: boolean;
    is_enabled: boolean;
    ad_type: AdType;
}

export async function getAllAds() {
    try {
        const result = await query(`
      SELECT a.*, ag.name as agent_name 
      FROM ads a
      LEFT JOIN agents ag ON a.agent_slug = ag.slug
      ORDER BY a.created_at DESC
    `);
        return result.rows;
    } catch (error) {
        console.error('Error fetching ads from DB:', error);
        throw error;
    }
}

export async function uploadAd(fileBuffer: Buffer, fileName: string, data: Omit<AdData, 'image_url'>) {
    try {
        const s3Client = getS3Client();
        const fileExt = path.extname(fileName);
        const s3Key = `ads/${Date.now()}_${Math.random().toString(36).substring(7)}${fileExt}`;

        // 1. Upload to S3
        await s3Client.send(new PutObjectCommand({
            Bucket: BUCKET_NAME,
            Key: s3Key,
            Body: fileBuffer,
            ContentType: getContentType(fileName),
        }));

        // Construct URL
        const imageUrl = `https://${BUCKET_NAME}.s3.${process.env.AWS_REGION || 'us-east-1'}.amazonaws.com/${s3Key}`;

        // 2. Insert into DB
        const result = await query(`
      INSERT INTO ads (agent_slug, image_url, target_url, is_paid, is_enabled, ad_type)
      VALUES ($1, $2, $3, $4, $5, $6)
      RETURNING *
    `, [data.agent_slug, imageUrl, data.target_url, data.is_paid, data.is_enabled, data.ad_type]);

        return result.rows[0];
    } catch (error) {
        console.error('Error uploading ad:', error);
        throw error;
    }
}

export async function updateAd(id: number, data: Partial<AdData>) {
    try {
        const fields = [];
        const values = [];
        let i = 1;

        for (const [key, value] of Object.entries(data)) {
            if (key === 'id') continue;
            fields.push(`${key} = $${i}`);
            values.push(value);
            i++;
        }

        values.push(id);
        const result = await query(`
      UPDATE ads 
      SET ${fields.join(', ')}, updated_at = NOW() 
      WHERE id = $${i}
      RETURNING *
    `, values);

        return result.rows[0];
    } catch (error) {
        console.error(`Error updating ad ${id}:`, error);
        throw error;
    }
}

export async function deleteAd(id: number) {
    try {
        const adResult = await query('SELECT image_url FROM ads WHERE id = $1', [id]);
        if (adResult.rows.length === 0) return { success: false, message: 'Ad not found' };

        const imageUrl = adResult.rows[0].image_url;
        const s3Client = getS3Client();

        const urlParts = imageUrl.split('.amazonaws.com/');
        if (urlParts.length > 1) {
            const s3Key = urlParts[1];
            await s3Client.send(new DeleteObjectCommand({
                Bucket: BUCKET_NAME,
                Key: s3Key,
            }));
        }

        await query('DELETE FROM ads WHERE id = $1', [id]);

        return { success: true };
    } catch (error) {
        console.error(`Error deleting ad ${id}:`, error);
        throw error;
    }
}

function getContentType(filename: string): string {
    const ext = path.extname(filename).toLowerCase();
    switch (ext) {
        case '.png': return 'image/png';
        case '.jpg':
        case '.jpeg': return 'image/jpeg';
        case '.gif': return 'image/gif';
        case '.webp': return 'image/webp';
        default: return 'application/octet-stream';
    }
}
