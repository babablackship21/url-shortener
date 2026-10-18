# SvelteKit URL Shortener Frontend

A clean and sleek frontend built with **JavaScript** and **SvelteKit**, connected directly to the FastAPI backend.

## Features

1. **Shorten URL (`/`)**: Enter a long destination URL with optional custom alias. Calls `POST /api/url/`.
2. **Retrieve URL (`/`)**: Look up original destination by short code or full short URL. Calls `GET /api/url/{short_code}`.
3. **Admin Dashboard (`/admin`)**: View all created short links, track total clicks, search/filter, copy, test, and delete links. Calls `GET /api/url/` and `DELETE /api/url/{short_code}`.
4. **Empty State Handling**: Elegant empty state when the project just started and 0 URLs exist in PostgreSQL.
5. **Direct Link Resolver (`/[short_code]`)**: Shows a loading animation while resolving, redirects to original destination, or displays not-found state if the link does not exist.

## Getting Started

### 1. Install Dependencies
```bash
npm install
```

### 2. Run the Development Server
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

In development, Vite proxies requests from `/api/*` to the FastAPI backend running at `http://127.0.0.1:8000/api/*`.
