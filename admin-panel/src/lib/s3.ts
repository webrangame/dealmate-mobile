import { S3Client, ListObjectsV2Command, GetObjectCommand } from '@aws-sdk/client-s3';
import { query } from './db';

export function getS3Client() {
  const AWS_ACCESS_KEY_ID = process.env.AWS_ACCESS_KEY_ID;
  const AWS_SECRET_ACCESS_KEY = process.env.AWS_SECRET_ACCESS_KEY;
  const REGION = process.env.AWS_REGION || 'us-east-1';

  if (!AWS_ACCESS_KEY_ID || !AWS_SECRET_ACCESS_KEY) {
    throw new Error('AWS credentials are not configured.');
  }

  return new S3Client({
    region: REGION,
    credentials: {
      accessKeyId: AWS_ACCESS_KEY_ID,
      secretAccessKey: AWS_SECRET_ACCESS_KEY,
    },
  });
}

export async function getActiveAgentsCount() {
  try {
    const s3Client = getS3Client();
    const listCommand = new ListObjectsV2Command({
      Bucket: process.env.AWS_S3_BUCKET_NAME || 'agent-marketplace-agents',
    });

    const response = await s3Client.send(listCommand);

    // Extract unique folder names from object keys
    const folderSet = new Set<string>();
    response.Contents?.forEach((object) => {
      if (object.Key) {
        const parts = object.Key.split('/');
        if (parts.length > 1 && parts[0]) {
          folderSet.add(parts[0]);
        }
      }
    });

    return folderSet.size;
  } catch (error) {
    console.error('Error fetching agent count from S3:', error);
    return 0;
  }
}

export async function getAllAgents() {
  const BUCKET_NAME = process.env.AWS_S3_BUCKET_NAME || 'agent-marketplace-agents';
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

    // 2. Fetch from S3
    const s3Client = getS3Client();
    const listCommand = new ListObjectsV2Command({
      Bucket: BUCKET_NAME,
    });

    const response = await s3Client.send(listCommand);
    console.log(`[S3 Scan] Found ${response.Contents?.length || 0} objects in bucket`);

    const folderSet = new Set<string>();
    response.Contents?.forEach((object) => {
      if (object.Key) {
        const parts = object.Key.split('/');
        if (parts.length > 1 && parts[0]) {
          folderSet.add(parts[0]);
        }
      }
    });

    const folders = Array.from(folderSet);
    console.log(`[S3 Scan] Unique folders found:`, folders);
    const agents = [];

    for (const folder of folders) {
      try {
        const getObjectCommand = new GetObjectCommand({
          Bucket: BUCKET_NAME,
          Key: `${folder}/metadata.json`,
        });

        const metadataResponse = await s3Client.send(getObjectCommand);
        const metadataText = await metadataResponse.Body?.transformToString();

        if (metadataText) {
          const metadata = JSON.parse(metadataText);
          const agentId = metadata.id || folder;
          agents.push({
            id: agentId,
            name: metadata.name || folder,
            description: metadata.description || '',
            category: metadata.category || 'general',
            version: metadata.version || '1.0.0',
            author: metadata.author?.name || 'Unknown',
            price: metadata.pricing?.price || 0,
            pricingModel: metadata.pricing?.model || 'free',
            usageCount: usageMap.get(agentId) || 0
          });
        }
      } catch (err) {
        console.warn(`Could not fetch metadata for folder: ${folder}`);
        agents.push({
          id: folder,
          name: folder,
          description: 'Metadata missing',
          category: 'unknown',
          version: '0.0.0',
          author: 'Unknown',
          price: 0,
          pricingModel: 'unknown',
          usageCount: usageMap.get(folder) || 0
        });
      }
    }

    return agents;
  } catch (error) {
    console.error('Error fetching all agents from S3:', error);
    return [];
  }
}
