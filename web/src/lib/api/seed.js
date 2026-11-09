import { request } from './client.js';

export const MOCK_SHORT_CODES = Object.freeze(['google', 'github', 'youtube', 'openai']);

/**
 * 5. Seed database with mock links (POST /api/seed/)
 * @returns {Promise<Array<{ original_url: string, short_url: string }>>}
 */
export async function seedMockLinks() {
  const res = await request(`/seed/`, {
    method: 'POST',
    headers: {
      'Accept': 'application/json'
    }
  });

  return res;
}

/**
 * 6. Delete all mock links from database (DELETE /api/seed/)
 * @returns {Promise<{ detail?: string }>}
 */
export async function deleteMockLinks() {
  const res = await request(`/seed/`, {
    method: 'DELETE',
    headers: {
      'Accept': 'application/json'
    }
  });

  return res;
}

