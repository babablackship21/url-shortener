# Frontend service

SvelteKit and JavaScript provide URL creation, destination lookup, and link management. In production, the SvelteKit Node adapter serves the application behind Caddy on EC2. See the [root README](../README.md) for the system architecture.

## Features

- **Shorten URL (`/`):** Create a short link with an optional custom alias using `POST /api/url/`.
- **Retrieve URL (`/`):** Inspect a destination by short code or full short URL using `GET /api/url/{short_code}`.
- **Admin dashboard (`/admin`):** List links, view clicks, filter, copy, test, seed, and delete. Search and totals cover the currently fetched page.
- **Empty state:** Displays a message when no links are available.
- **Link resolver (`/[short_code]`):** Looks up a destination and redirects the browser, or displays a not-found state.

## Modules

| Path | Responsibility |
| --- | --- |
| `src/routes/` | Home, admin, and short-code resolver pages |
| `src/routes/+layout.svelte` | Shared layout |
| `src/lib/Navbar.svelte` | Navigation |
| `src/lib/api.js` | API requests, response errors, and short-link helpers |
| `src/app.css` | Global styles |

## Production routing

Caddy is the public entry point. It forwards pages and assets to `web:3000` and `/api/*` requests to `app:8000`, removing the `/api` prefix.

For example, when the public origin is `https://example.com`:

```text
Browser: https://example.com/          -> Caddy -> web:3000
Browser: https://example.com/api/url/  -> Caddy -> app:8000/url/
```

The browser uses `/api` relative to the public origin, so frontend and API requests share the same origin. The frontend container's port is accessible over the Docker network and is not published to the host in production. 

## Environment variables

The production Dockerfile and Compose configuration supply these values:

| Variable | When used | Purpose and source |
| --- | --- | --- |
| `VITE_API_BASE_URL` | Image build |  `Dockerfile.prod` sets it to `/api`. |

## Production build and deployment

From the repository root, the production image can be built with:

```bash
docker build -f web/Dockerfile.prod -t url-shortener-web ./web
```

The Dockerfile installs dependencies with `npm ci`, runs `npm run build`, removes development dependencies, and starts the generated Node server with `node build`.

To validate production compilation from `web/` using Node.js 22:

```bash
npm ci
npm run build
```
