const API_BASE = (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_BASE_URL) || '/api';


/**
 * Handles HTTP responses from FastAPI, parsing JSON or handling 204 No Content.
 */
export async function handleResponse(res) {
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
    throw new ApiError(errorMessage, res.status);
  }

  // HTTP 204 No Content
  if (res.status === 204) {
    return { detail: 'Success' };
  }

  return res.json();
}


export class ApiError extends Error {
  constructor(message, status) { super(message); this.name = "ApiError"; this.status = status; }
}

export function request(path, options = {}) {
  return fetch(`${API_BASE}${path}`, { ...options, headers: { Accept: "application/json", ...options.headers } }).then(handleResponse);
}
