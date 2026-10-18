from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from db import get_db
from utils.url_store import increment_clicks

router = APIRouter(tags=["Redirect"])


@router.get(
    "/{short_code}",
    response_class=RedirectResponse,
    status_code=status.HTTP_302_FOUND,
    summary="Redirect short URL to original destination",
)
def redirect_short_url(
    short_code: str,
    db: Session = Depends(get_db),
):
    """
    Looks up the short code, increments click count, and issues a 302 redirect.
    """
    item = increment_clicks(db, short_code)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found or expired.",
        )

    db.commit()

    return RedirectResponse(
        url=item.original_url,
        status_code=status.HTTP_302_FOUND,
    )
