import { request } from './client.js';
import { extractSlug } from '../utils/urls.js';

/**
 * 1. Create a shortened URL
 * @param {string} originalUrl - The destination long URL
 * @param {string|null} [customCode] - Optional custom alias (4-16 chars)
 * @returns {Promise<{ original_url: string, short_url: string }>}
 */
export async function createShortUrl(originalUrl, customCode = null) {
  const payload = {
    original_url: originalUrl.trim()
  };

  if (customCode && customCode.trim()) {
    payload.custom_code = customCode.trim();
  }

  const res = await request(`/url/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });

  return res;
}

/**
 * 2. Retrieve a URL and increment click count
 * @param {string} shortCodeOrUrl - The short code or full shortened URL
 * @returns {Promise<{ id: number, short_code: string, original_url: string, clicks: number, created_at?: string }>}
 */
export async function getOriginalUrl(shortCodeOrUrl) {
  const cleanCode = extractSlug(shortCodeOrUrl);
  if (!cleanCode) {
    throw new Error('Please provide a valid short code.');
  }

  const res = await request(`/url/${encodeURIComponent(cleanCode)}`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json'
    }
  });


  return res;
}

/**
 * 3. List all shortened URLs for Admin (ordered newest first)
 * @returns {Promise<Array<{ id: number, short_code: string, original_url: string, clicks: number, created_at?: string }>>}
 */
export async function listUrls() {
  const res = await request(`/url/`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json'
    }
  });

  return res;
}

/**
 * 4. Delete a shortened URL
 * @param {string} shortCode - The short code to delete
 * @returns {Promise<{ message: string }>}
 */
export async function deleteUrl(shortCode) {
  const cleanCode = extractSlug(shortCode);
  const res = await request(`/url/${encodeURIComponent(cleanCode)}`, {
    method: 'DELETE',
    headers: {
      'Accept': 'application/json'
    }
  });

  return res;
}

