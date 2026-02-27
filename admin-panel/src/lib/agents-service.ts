import { query } from './db';
import { getAllAgents as getAllAgentsFromS3, getS3Client } from './s3';
import AdmZip from 'adm-zip';
import { PutObjectCommand } from '@aws-sdk/client-s3';
import path from 'path';

export async function getAllAgentsFromDB(showHidden = true) {
    try {
        // 1. Fetch usage counts from DB
        const usageResult = await query(`
      SELECT agent_id, COUNT(*) as count 
      FROM user_purchases 
      GROUP BY agent_id
    `);
        const usageMap = new Map();
        usageResult.rows.forEach((row: any) => {
            usageMap.set(row.agent_id, parseInt(row.count));
        });

        // 2. Fetch agents from DB
        const whereClause = showHidden ? '' : 'WHERE is_visible = true';
        const result = await query(`
      SELECT * FROM agents 
      ${whereClause}
      ORDER BY name ASC
    `);

        return result.rows.map((row: any) => {
            const metadata = row.metadata || {};
            return {
                id: row.slug,
                slug: row.slug,
                name: row.name,
                description: row.description || metadata.description || '',
                category: metadata.category || 'general',
                version: metadata.version || '1.0.0',
                author: metadata.author?.name || metadata.author || 'Unknown',
                price: metadata.pricing?.price || metadata.price || 0,
                pricingModel: metadata.pricing?.model || metadata.pricingModel || 'free',
                usageCount: usageMap.get(row.slug) || 0,
                isVisible: row.is_visible
            };
        });
    } catch (error) {
        console.error('Error fetching agents from DB:', error);
        throw error;
    }
}

export async function toggleAgentVisibility(slug: string, isVisible: boolean) {
    try {
        await query(
            'UPDATE agents SET is_visible = $1, updated_at = NOW() WHERE slug = $2',
            [isVisible, slug]
        );
        return { success: true };
    } catch (error) {
        console.error('Error toggling agent visibility:', error);
        throw error;
    }
}

export async function uploadAgentZip(fileBuffer: Buffer, originalName: string) {
    const BUCKET_NAME = process.env.AWS_S3_BUCKET_NAME || 'agent-marketplace-agents';
    try {
        console.log(`[Upload ZIP] Starting upload for: ${originalName}`);
        const zip = new AdmZip(fileBuffer);
        const zipEntries = zip.getEntries();

        // 1. Find metadata.json
        let metadata: any = null;
        let agentSlug = originalName.replace('.zip', '').toLowerCase().replace(/[^a-z0-9-]/g, '-');

        for (const entry of zipEntries) {
            if (entry.entryName.endsWith('metadata.json')) {
                const metadataText = entry.getData().toString('utf8');
                metadata = JSON.parse(metadataText);
                if (metadata.id) agentSlug = metadata.id;
                break;
            }
        }

        if (!metadata) {
            throw new Error('metadata.json not found in ZIP file');
        }

        // 2. Upload to S3
        const s3Client = getS3Client();
        for (const entry of zipEntries) {
            if (entry.isDirectory) continue;

            const s3Key = `${agentSlug}/${entry.entryName}`;
            await s3Client.send(new PutObjectCommand({
                Bucket: BUCKET_NAME,
                Key: s3Key,
                Body: entry.getData(),
                ContentType: getContentType(entry.entryName)
            }));
        }

        // 3. Upsert into database
        await query(`
      INSERT INTO agents (slug, name, description, metadata, is_visible, updated_at)
      VALUES ($1, $2, $3, $4, true, NOW())
      ON CONFLICT (slug) DO UPDATE SET
        name = EXCLUDED.name,
        description = EXCLUDED.description,
        metadata = EXCLUDED.metadata,
        updated_at = NOW()
    `, [
            agentSlug,
            metadata.name || agentSlug,
            metadata.description || '',
            JSON.stringify(metadata)
        ]);

        return { success: true, slug: agentSlug };
    } catch (error) {
        console.error('[Upload ZIP] Error:', error);
        throw error;
    }
}

function getContentType(filename: string): string {
    const ext = path.extname(filename).toLowerCase();
    switch (ext) {
        case '.json': return 'application/json';
        case '.js': return 'application/javascript';
        case '.txt': return 'text/plain';
        case '.md': return 'text/markdown';
        case '.png': return 'image/png';
        case '.jpg':
        case '.jpeg': return 'image/jpeg';
        default: return 'application/octet-stream';
    }
}

export async function syncAgentsFromS3() {
    try {
        console.log('Starting S3 to DB sync...');
        const agentsFromS3 = await getAllAgentsFromS3();
        console.log(`Fetched ${agentsFromS3.length} agents from S3`);

        for (const agent of agentsFromS3) {
            // Upsert into agents table
            await query(`
        INSERT INTO agents (slug, name, description, metadata, is_visible, updated_at)
        VALUES ($1, $2, $3, $4, true, NOW())
        ON CONFLICT (slug) DO UPDATE SET
          name = EXCLUDED.name,
          description = EXCLUDED.description,
          metadata = EXCLUDED.metadata,
          updated_at = NOW()
      `, [
                agent.id,
                agent.name,
                agent.description,
                JSON.stringify({
                    category: agent.category,
                    version: agent.version,
                    author: agent.author,
                    pricing: {
                        price: agent.price,
                        model: agent.pricingModel
                    }
                })
            ]);
        }

        return { success: true, count: agentsFromS3.length };
    } catch (error) {
        console.error('Error syncing agents from S3:', error);
        throw error;
    }
}
