from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from db import get_db

router = APIRouter(tags=["Health"])


@router.get("/")
def read_root(db: Session = Depends(get_db)):
    """Check database connectivity; return HTTP 503 when the probe fails."""
    try:
        db.execute(text("SELECT 1"))
        return {
            "message": "Welcome to the URL Shortener API",
            "database": "connected",
        }
    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        )