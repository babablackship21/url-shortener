from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.orm import Session

from db import get_db
from models.url import URLItem
from schemas.url import URLCreateResponse
from utils.mock_links import MOCK_LINKS
from config import BASE_URL
from utils.url_store import insert_url_if_available

router = APIRouter(prefix="/seed", tags=["Seed"])


@router.post(
    "/",
    response_model=list[URLCreateResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Seed database with predefined mock links",
)
def seed_mock_links(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Seeds mock links into PostgreSQL in an atomic transaction, skipping any that already exist.
    """
    created_responses: list[URLCreateResponse] = []
    for link in MOCK_LINKS:
        code = link["short_code"]
        if insert_url_if_available(db, code, link["original_url"]):
            created_responses.append(URLCreateResponse(
                original_url=link["original_url"],
                short_url=f"{BASE_URL}/{code}",
            ))
    db.commit()
    return created_responses


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete all predefined mock links",
)
def delete_all_mock_links(
    db: Session = Depends(get_db),
):
    """
    Deletes all mock links in a single atomic bulk DELETE query.
    """
    mock_codes = [link["short_code"] for link in MOCK_LINKS]

    # Single atomic bulk delete
    db.query(URLItem).filter(URLItem.short_code.in_(mock_codes)).delete(
        synchronize_session=False
    )
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)