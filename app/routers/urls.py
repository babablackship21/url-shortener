from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from db import get_db
from models.url import URLItem
from schemas.url import URLCreateRequest, URLCreateResponse, URLResponse
from utils.short_code import generate_short_code
from utils.safe_search import check_url_safety
from config import BASE_URL
from utils.url_store import increment_clicks, insert_url_if_available

router = APIRouter(prefix="/url", tags=["URLs"])


# 1. Create a shortened URL
@router.post(
    "/",
    response_model=URLCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new short URL",
)
def create_short_url(
    request: Request,
    payload: URLCreateRequest,
    db: Session = Depends(get_db),
):
    # Check URL safety before creating a short URL
    """Check destination safety and create a unique code; reject unsafe or taken codes."""
    if not check_url_safety(str(payload.original_url)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The provided URL is not safe.",
        )

    original_url = str(payload.original_url)
    for _ in range(1 if payload.custom_code else 5):
        short_code = payload.custom_code or generate_short_code()
        if insert_url_if_available(db, short_code, original_url):
            db.commit()
            return URLCreateResponse(
                original_url=original_url,
                short_url=f"{BASE_URL}/{short_code}",
            )
        if payload.custom_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Short code '{short_code}' is already taken.",
            )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Could not generate a unique short code. Please try again.",
    )


# 2. List all short URLs (Admin)
@router.get(
    "/",
    response_model=list[URLResponse],
    summary="List a page of shortened URLs",
)
def list_short_urls(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    """Return at most 100 URLs, newest first, skipping the requested offset."""
    return (
        db.query(URLItem).order_by(URLItem.id.desc())
        .offset(offset).limit(limit).all()
    )


# 3. Retrieve a URL by its short code (API inspect/lookup)
@router.get(
    "/{short_code}",
    response_model=URLResponse,
    summary="Retrieve URL details by short code",
)
def get_original_url(
    short_code: str,
    db: Session = Depends(get_db),
):
    """Return URL details and count the lookup; raise HTTP 404 for missing codes."""
    item = increment_clicks(db, short_code)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found or expired.",
        )

    db.commit()

    return item


# 4. Delete a shortened URL
@router.delete(
    "/{short_code}",
    summary="Delete a shortened URL",
)
def delete_short_url(
    short_code: str,
    db: Session = Depends(get_db),
):
    """Delete a URL and confirm its code; raise HTTP 404 when absent."""
    item = (
        db.query(URLItem)
        .filter(URLItem.short_code == short_code.strip())
        .first()
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Short URL '{short_code}' not found.",
        )

    db.delete(item)
    db.commit()

    return {
        "message": f"Short URL '{short_code}' successfully deleted."
    }
