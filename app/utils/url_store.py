"""Atomic URL writes for PostgreSQL and the SQLite test database."""
from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert as postgres_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.orm import Session

from models.url import URLItem
from schemas.url import URLResponse


def insert_url_if_available(db: Session, short_code: str, original_url: str) -> bool:
    """Insert without committing; return False only for a short-code conflict.

    The unique constraint resolves concurrent inserts inside the database.
    Other constraint or database failures propagate to the API error handlers.
    """
    insert = sqlite_insert if db.get_bind().dialect.name == "sqlite" else postgres_insert
    statement = (
        insert(URLItem)
        .values(short_code=short_code, original_url=original_url, clicks=0)
        .on_conflict_do_nothing(index_elements=[URLItem.short_code])
        .returning(URLItem.id)
    )
    return db.execute(statement).scalar_one_or_none() is not None


def increment_clicks(db: Session, short_code: str) -> URLResponse | None:
    """Atomically increment and snapshot a URL, leaving commit to the caller.

    UPDATE uses the database's current count even when requests overlap.
    RETURNING avoids a second lookup or stale ORM identity-map values.
    """
    statement = (
        update(URLItem)
        .where(URLItem.short_code == short_code.strip())
        .values(clicks=URLItem.clicks + 1)
        .returning(*URLItem.__table__.columns)
        .execution_options(synchronize_session=False)
    )
    row = db.execute(statement).mappings().one_or_none()
    return URLResponse.model_validate(dict(row)) if row is not None else None
