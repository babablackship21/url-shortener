# Backend service

FastAPI handles URL creation, destination inspection, redirects, link management, and database health checks. SQLAlchemy manages PostgreSQL access; Pydantic validates request and response data.

## Structure

| Path | Purpose |
| --- | --- |
| `main.py` | Application setup, lifespan, routers, and database error handlers |
| `routers/` | Health, URL, redirect, and seed endpoints |
| `schemas/url.py` | Request validation and response models |
| `models/url.py` | SQLAlchemy URL table |
| `utils/url_store.py` | Conflict-safe inserts and atomic click increments |
| `utils/safe_search.py` | Google Safe Browsing integration |
| `utils/link_policy.py` | Shared `PROTECTED_SHORT_CODES` policy |
| `config.py`, `db.py` | Configuration, engine, and database sessions |
| `test/` | Pytest tests for short-code generation |

## Endpoints

Through Caddy, endpoints use the `/api` prefix shown below. Direct requests to `http://localhost:8000` omit that prefix—for example, `http://localhost/api/url/` through Caddy corresponds to `http://localhost:8000/url/` directly.

| Method | Public path | Behavior |
| --- | --- | --- |
| GET | `/api/` | Database connectivity check; 200 when connected, 503 when unavailable |
| POST | `/api/url/` | Create a short URL; 201 with `original_url` and `short_url` |
| GET | `/api/url/?limit=50&offset=0` | List newest links first; limit 1–100, offset zero or greater |
| GET | `/api/url/{short_code}` | Return details and increment clicks; 404 if absent |
| DELETE | `/api/url/{short_code}` | Delete a link; 200 on success, 403 for protected codes, 404 if absent |
| GET | `/api/{short_code}` | Increment clicks and return a 302 redirect; 404 if absent |
| POST | `/api/seed/` | Insert predefined mock links, skipping existing codes; 201 |
| DELETE | `/api/seed/` | Delete predefined mock links except protected codes; 204 |
| GET | `/api/docs` | Swagger UI |
| GET | `/api/redoc` | ReDoc documentation |

Example creation body for `POST /api/url/` through Caddy:

```json
{
  "original_url": "https://example.com/article",
  "custom_code": "article"
}
```

Example response (`201 Created`), with `API_BASE_URL=http://localhost/api`:

```json
{
  "original_url": "https://example.com/article",
  "short_url": "http://localhost/api/article"
}
```

`custom_code` is optional and accepts 4–16 letters, numbers, hyphens, or underscores. Unsafe destinations and taken custom codes return 400; validation failures return 422. Safety-service failures return 503 rather than permitting unchecked destinations.

List and detail responses include `id`, `short_code`, `original_url`, `clicks`, `created_at`, and `can_delete`. The shared protection policy includes `code` and applies to direct deletion and seed cleanup. Click counts include inspection requests as well as redirects, so they are not unique-visitor counts.

## Configuration

| Setting | Purpose |
| --- | --- |
| `DATABASE_URL` | Optional full database URL; overrides individual database settings |
| `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` | Required when `DATABASE_URL` is absent |
| `POSTGRES_HOST`, `POSTGRES_PORT` | Default to `localhost:5432` for host execution. Docker Compose uses `postgres:5432` over its internal network. |
| `GOOGLE_SAFE_BROWSING_API_URL`, `GOOGLE_SAFE_BROWSING_API_KEY` | Required safety-service endpoint and credentials |
| `API_BASE_URL` | Public prefix used to construct returned short URLs, including scheme and path; for example, `https://example.com/api`. |
| `ENV` | Application environment for logging; defaults to `prod` |

Settings can be supplied through environment variables or an `.env` file. 

## Run and test

For the full container stack, follow the [root README](../README.md). To run directly on the host, configure the settings above and run from `app/`:

```bash
python -m pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

From the repository root:

```bash
cd app
python -m pytest test -q
```

