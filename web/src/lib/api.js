/**
 * Backend API Client for FastAPI URL Shortener
 * Uses relative `/api` by default (proxied via Vite in dev or Caddy in production),
 * or can be overridden via VITE_API_BASE_URL.
 */

const API_BASE = (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_BASE_URL) || '/api';

/**
 * List of predefined mock link short codes from backend utils/mock_links.py
 */
export const MOCK_SHORT_CODES = Object.freeze(['google', 'github', 'youtube', 'openai']);

/**
 * Handles HTTP responses from FastAPI, parsing JSON or handling 204 No Content.
 */
async function handleResponse(res) {
  if (!res.ok) {
    let errorMessage = `HTTP Error ${res.status}`;
    try {
      const data = await res.json();
      if (typeof data.detail === 'string') {
        errorMessage = data.detail;
      } else if (Array.isArray(data.detail) && data.detail[0]?.msg) {
        errorMessage = data.detail[0].msg;
      } else if (data.message) {
        errorMessage = data.message;
      }
    } catch {
      // Non-JSON response
    }
    throw new Error(errorMessage);
  }

  // HTTP 204 No Content
  if (res.status === 204) {
    return { detail: 'Success' };
  }

  return res.json();
}

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

  const res = await fetch(`${API_BASE}/url/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });

  return handleResponse(res);
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

  const res = await fetch(`${API_BASE}/url/${encodeURIComponent(cleanCode)}`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json'
    }
  });


  return handleResponse(res);
}

/**
 * 3. List all shortened URLs for Admin (ordered newest first)
 * @returns {Promise<Array<{ id: number, short_code: string, original_url: string, clicks: number, created_at?: string }>>}
 */
export async function listUrls() {
  const res = await fetch(`${API_BASE}/url/`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json'
    }
  });

  return handleResponse(res);
}

/**
 * 4. Delete a shortened URL
 * @param {string} shortCode - The short code to delete
 * @returns {Promise<{ message: string }>}
 */
export async function deleteUrl(shortCode) {
  const cleanCode = extractSlug(shortCode);
  const res = await fetch(`${API_BASE}/url/${encodeURIComponent(cleanCode)}`, {
    method: 'DELETE',
    headers: {
      'Accept': 'application/json'
    }
  });

  return handleResponse(res);
}

/**
 * 5. Seed database with mock links (POST /api/seed/)
 * @returns {Promise<Array<{ original_url: string, short_url: string }>>}
 */
export async function seedMockLinks() {
  const res = await fetch(`${API_BASE}/seed/`, {
    method: 'POST',
    headers: {
      'Accept': 'application/json'
    }
  });

  return handleResponse(res);
}

/**
 * 6. Delete all mock links from database (DELETE /api/seed/)
 * @returns {Promise<{ detail?: string }>}
 */
export async function deleteMockLinks() {
  const res = await fetch(`${API_BASE}/seed/`, {
    method: 'DELETE',
    headers: {
      'Accept': 'application/json'
    }
  });

  return handleResponse(res);
}

/**
 * 7. Check API & DB health
 * @returns {Promise<{ message: string, database: string }>}
 */
export async function checkHealth() {
  const res = await fetch(`${API_BASE}/`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json'
    }
  });

  return handleResponse(res);
}

/**
 * Centralized helper to construct full short URL for a code
 * @param {string} code - The short code
 * @returns {string} Full short link
 */
export function buildShortUrl(code) {
  if (!code) return '';
  if (typeof window !== 'undefined') {
    return `${window.location.origin}/api/${encodeURIComponent(code)}`;
  }
  return `/api/${encodeURIComponent(code)}`;
}

/**
 * Robust helper to extract a short code from a full URL, query param, or raw string.
 * Handles cases like:
 * - "http://localhost:8000/api/google" -> "google"
 * - "localhost:3000/?s=google" -> "google"
 * - "api/google" -> "google"
 * - "google" -> "google"
 * @param {string} input - Raw input from user
 * @returns {string} Extracted short code
 */
export function extractSlug(input) {
  if (!input) return '';
  let str = String(input).trim();

  // If query string format: ?s=xyz or ?code=xyz
  const queryMatch = str.match(/[?&](?:s|code)=([^&#]+)/i);
  if (queryMatch) {
    return decodeURIComponent(queryMatch[1]).trim();
  }

  // Prepend protocol if input looks like a domain/path (e.g. localhost:8000/api/code or example.com/code)
  if (!/^[a-zA-Z][a-zA-Z0-9+.-]*:\/\//.test(str)) {
    if (str.includes('/') && (str.startsWith('localhost') || str.includes('.'))) {
      str = `http://${str}`;
    }
  }

  try {
    const parsed = new URL(str);
    const q = parsed.searchParams.get('s') || parsed.searchParams.get('code');
    if (q) return q.trim();

    const segments = parsed.pathname.split('/').filter(Boolean);
    if (segments.length > 0) {
      return decodeURIComponent(segments[segments.length - 1]).trim();
    }
  } catch {
    // Treat as raw slug/path
  }

  // Clean raw string: strip protocol, leading 'api/', and slashes
  return str
    .replace(/^https?:\/\//i, '')
    .replace(/^\/?api\//i, '')
    .replace(/^\/+|\/+$/g, '')
    .trim();
}
