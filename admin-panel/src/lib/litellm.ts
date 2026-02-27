export async function getUserLiteLLMStats(identifier: string | number) {
  const LITELLM_API_URL = process.env.LITELLM_API_URL;
  const LITELLM_API_KEY = process.env.LITELLM_API_KEY;

  if (!LITELLM_API_URL || !LITELLM_API_KEY) {
    return null;
  }

  try {
    const res = await fetch(`${LITELLM_API_URL}/user/info?user_id=${encodeURIComponent(identifier.toString())}`, {
      headers: {
        'x-litellm-api-key': LITELLM_API_KEY
      }
    });

    if (!res.ok) {
      if (res.status === 404) return null;
      throw new Error(`LiteLLM stats fetch failed: ${res.status}`);
    }

    return await res.json();
  } catch (error) {
    console.error('Error fetching LiteLLM stats:', error);
    return null;
  }
}

export async function getAllUsersLiteLLMStats() {
  const LITELLM_API_URL = process.env.LITELLM_API_URL;
  const LITELLM_API_KEY = process.env.LITELLM_API_KEY;

  if (!LITELLM_API_URL || !LITELLM_API_KEY) {
    return [];
  }

  try {
    const res = await fetch(`${LITELLM_API_URL}/user/list`, {
      headers: {
        'x-litellm-api-key': LITELLM_API_KEY
      }
    });

    if (!res.ok) {
      throw new Error(`LiteLLM users fetch failed: ${res.status}`);
    }

    const data = await res.json();
    return data.users || data.data || [];
  } catch (error) {
    console.error('Error fetching all LiteLLM users:', error);
    return [];
  }
}
