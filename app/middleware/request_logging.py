import json
import logging
from time import perf_counter
from uuid import uuid4

logger = logging.getLogger("app.requests")
BODY_LOG_LIMIT = 4096


def capture_body(buffer, message):
    """Keep a bounded copy while forwarding the original body unchanged."""
    remaining = max(0, BODY_LOG_LIMIT + 1 - len(buffer))
    buffer.extend(message.get("body", b"")[:remaining])


def format_body(body):
    if not body:
        return None
    if len(body) > BODY_LOG_LIMIT:
        return "[body exceeds logging limit]"

    def redact(value):
        if isinstance(value, dict):
            return {
                key: "[REDACTED]" if any(
                    word in key.lower() for word in ("password", "secret", "token", "api_key", "authorization")
                ) else redact(item)
                for key, item in value.items()
            }
        if isinstance(value, list):
            return [redact(item) for item in value]
        return value

    try:
        return redact(json.loads(body))
    except (ValueError, UnicodeError, RecursionError):
        return "[non-JSON or malformed body omitted]"


class RequestLoggingMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = uuid4().hex
        scope.setdefault("state", {})["request_id"] = request_id
        method = scope["method"]
        path = scope["path"]
        started = perf_counter()
        status_code = None
        failed = False
        request_body = bytearray()
        error_body = bytearray()
        logger.info("request id=%s method=%s path=%r", request_id, method, path)

        async def log_receive():
            message = await receive()
            if message["type"] == "http.request":
                capture_body(request_body, message)
            return message

        async def log_send(message):
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
                message = dict(message)
                message["headers"] = [
                    (key, value) for key, value in message.get("headers", [])
                    if key.lower() != b"x-request-id"
                ] + [(b"x-request-id", request_id.encode("ascii"))]
            elif message["type"] == "http.response.body" and status_code is not None and status_code >= 400:
                capture_body(error_body, message)
            await send(message)

        try:
            await self.app(scope, log_receive, log_send)
        except Exception as exc:
            failed = True
            logger.error(
                "error id=%s method=%s path=%r type=%s message=%r",
                request_id, method, path, type(exc).__name__,
                str(exc)[:BODY_LOG_LIMIT],
            )
            raise
        finally:
            logger.info("request_body id=%s body=%r", request_id, format_body(request_body))
            status = status_code if status_code is not None else 500
            level = logging.ERROR if failed or status >= 500 else (
                logging.WARNING if status >= 400 else logging.INFO
            )
            logger.log(
                level,
                "response id=%s method=%s path=%r status=%s duration_ms=%.2f failed=%s error=%r",
                request_id, method, path, status,
                (perf_counter() - started) * 1000, failed, format_body(error_body),
            )
