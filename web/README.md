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
| `src/lib/components/links/` | Independent create and retrieve forms, including request state and results |
| `src/lib/components/admin/` | Overview, toolbar, and searchable links table |
| `src/lib/components/` | Shared KPI card, copy button, feedback, spinner, and backend status |
| `src/lib/api/` | HTTP client, status-aware errors, and focused endpoint modules |
| `src/lib/utils/` | URL parsing/normalization, date formatting, filtering, and statistics |
| `src/app.css` | Tailwind import, theme tokens, animations, and base styles |

The admin route owns the fetched links and mutations. It passes data and callbacks to its components; the table owns its search query. Each home form owns its inputs, loading state, errors, and results, so switching tabs cannot mix feedback between workflows. Both forms remain mounted to preserve their inputs and results.

Shared components own their styles and interaction state. `CopyButton` manages clipboard feedback and timer cleanup. `KpiCard` accepts `label`, `value`, `description`, `muted`, an icon snippet, and an icon `tone` (`emerald`, `amber`, or `purple`). Components use Tailwind CSS v4 utilities. `src/app.css` defines the shared colors (`brand`, `ink`, `muted`, `line`, `page`, and `surface`), fonts, card radius/shadow, and animation tokens. Tailwind Preflight supplies the reset. The Vite plugin in `vite.config.js` generates the stylesheet; no separate Tailwind configuration file is required.

Use complete utility strings in conditional classes and variant maps (as in `KpiCard`) so Tailwind can detect every state. Use `sm:` for the 640px layouts and `min-[600px]:` for the form result rows. Spinner dimensions remain inline because they accept a runtime pixel size.

API modules handle transport and response parsing. `ApiError.status` lets callers distinguish a missing link from a service failure. URL and statistics helpers remain independent of components.

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
