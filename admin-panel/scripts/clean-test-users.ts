import * as dotenv from 'dotenv';
import * as path from 'path';
dotenv.config({ path: path.join(__dirname, '../.env.local') });

const LITELLM_API_URL = process.env.LITELLM_API_URL;
const LITELLM_API_KEY = process.env.LITELLM_API_KEY;

async function deleteTestUsers() {
  if (!LITELLM_API_URL || !LITELLM_API_KEY) {
    console.error('Missing LiteLLM environment variables');
    return;
  }

  console.log('--- Cleaning Test Users from LiteLLM ---');
  
  try {
    // 1. Fetch all users
    const res = await fetch(`${LITELLM_API_URL}/user/list`, {
      headers: { 'x-litellm-api-key': LITELLM_API_KEY }
    });
    
    if (!res.ok) throw new Error('Failed to fetch user list');
    const data = await res.json();
    const users = data.users || data.data || [];
    
    console.log(`Searching through ${users.length} users...`);

    // 2. Identify test users
    const testUserIds = users
      .filter((u: any) => {
        const email = (u.user_email || '').toLowerCase();
        const id = (u.user_id || '').toString();
        
        return email.includes('test') || 
               email.includes('@example.com') || 
               email === '' ||
               (id.length > 0 && !isNaN(Number(id)) && Number(id) <= 20); // Low IDs often indicate early tests, but we'll be careful
      })
      .map((u: any) => u.user_id || u.id);

    if (testUserIds.length === 0) {
      console.log('No test users found.');
      return;
    }

    console.log(`Identified ${testUserIds.length} test users for removal.`);

    // 3. Delete in bulk
    const delRes = await fetch(`${LITELLM_API_URL}/user/delete`, {
      method: 'POST',
      headers: {
        'x-litellm-api-key': LITELLM_API_KEY,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ user_ids: testUserIds })
    });

    if (delRes.ok) {
      console.log('✅ Successfully removed test users.');
    } else {
      const err = await delRes.text();
      console.error('❌ Failed to delete users:', err);
    }
    
  } catch (error) {
    console.error('Error:', error);
  }
}

deleteTestUsers();
