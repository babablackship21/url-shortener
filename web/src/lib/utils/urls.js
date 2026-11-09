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

export function normalizeUrl(input) {
  const value = input.trim();
  return value && !/^[a-zA-Z][a-zA-Z0-9+.-]*:\/\//.test(value) ? `https://${value}` : value;
}
