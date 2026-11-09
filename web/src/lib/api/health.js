import { request } from './client.js';

/**
 * 7. Check API & DB health
 * @returns {Promise<{ message: string, database: string }>}
 */
export async function checkHealth() {
  const res = await request(`/`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json'
    }
  });

  return res;
}

