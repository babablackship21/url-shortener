from datetime import datetime, timezone
from sqlalchemy import BigInteger, Column, DateTime, String, Text
from db import Base


class URLItem(Base):
    __tablename__ = "urls"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    short_code = Column(String(16), unique=True, index=True, nullable=False)
    original_url = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    clicks = Column(BigInteger, default=0, nullable=False)

