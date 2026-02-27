/**
 * Example script to create a LiteLLM virtual key
 * Run with: node create-key-example.js
 */

const LITELLM_API_URL = 'https://swzissb82u.us-east-1.awsapprunner.com';
const MASTER_KEY = 'sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642';

async function createVirtualKey(userId = 'admin') {
  console.log(`Creating virtual key for user: ${userId}`);
  console.log('');

  try {
    const response = await fetch(`${LITELLM_API_URL}/key/generate`, {
      method: 'POST',
      headers: {
        'x-litellm-api-key': MASTER_KEY,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: userId,
        duration: null, // null = no expiration
        key_alias: 'API Key via Script',
        tpm_limit: 100000,
        rpm_limit: 100,
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to create key: ${errorText}`);
    }

    const data = await response.json();
    
    console.log('✅ Virtual Key Created Successfully!');
    console.log('');
    console.log('Key Details:');
    console.log(JSON.stringify(data, null, 2));
    console.log('');
    console.log('🔑 Your Virtual Key (save this!):');
    console.log(data.key);
    console.log('');
    console.log('⚠️  Note: This key is only shown once. Save it securely!');
    
    return data.key;
  } catch (error) {
    console.error('❌ Error creating virtual key:');
    console.error(error.message);
    process.exit(1);
  }
}

// Get user ID from command line or use default
const userId = process.argv[2] || 'admin';
createVirtualKey(userId);
