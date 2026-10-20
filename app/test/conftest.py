"""
Shared pytest fixtures for the URL shortener test suite.

Uses an in-memory SQLite database so tests never touch PostgreSQL.

db.py handles SQLite-compatible engine kwargs automatically; here we also
patch SQLAlchemy's BigInteger → Integer mapping so SQLite auto-increments
PKs correctly (SQLite only auto-generates rowids for INTEGER-affinity cols).
"""
import os
import sys

# Ensure the app package root is on sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Use a throw-away SQLite DB for every test run
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["GOOGLE_SAFE_BROWSING_API_URL"] = "https://safety.example.test"
os.environ["GOOGLE_SAFE_BROWSING_API_KEY"] = "test-key"

# Patch BigInteger → Integer BEFORE any app model is imported, so the table
# DDL uses INTEGER (SQLite's native autoincrement affinity) rather than BIGINT.
import sqlalchemy.types as _sa_types
from sqlalchemy import Integer as _Integer
_sa_types.BigInteger = _Integer  # type: ignore[attr-defined]
import sqlalchemy as _sa
_sa.BigInteger = _Integer  # type: ignore[attr-defined]

import pytest
from fastapi.testclient import TestClient

from db import Base, SessionLocal, engine, get_db
from main import app


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def reset_db():
    """Re-create all tables before each test and drop them afterwards."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    """Yield a raw SQLAlchemy session backed by the test DB."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session):
    """
    FastAPI TestClient with the real DB dependency overridden to use the
    in-memory SQLite session.
    """

    def override_get_db():
        """Reuse the session owned by the test fixture."""
        try:
            yield db_session
        finally:
            pass  # cleanup handled by db_session fixture

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app, raise_server_exceptions=True) as c:
            try:
                yield c
            finally:
                db_session.close()
    finally:
        app.dependency_overrides.clear()



@pytest.fixture(autouse=True)
def mock_safety_service(monkeypatch):
    """Keep router tests deterministic and prevent calls to the real service."""
    monkeypatch.setattr("routers.urls.check_url_safety", lambda url: True)
