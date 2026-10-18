from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class URLCreateRequest(BaseModel):
    original_url: HttpUrl
    custom_code: str | None = Field(
        default=None,
        min_length=3,
        max_length=16,
        pattern=r"^[a-zA-Z0-9_-]+$",
        description="Optional custom short code (3-16 alphanumeric characters, hyphens or underscores).",
    )

class URLResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    short_code: str
    original_url: str
    clicks: int
    created_at: datetime | None = None


class URLCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    original_url: str
    short_url: str