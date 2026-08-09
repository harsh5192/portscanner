from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Base class for SQLAlchemy ORM models."""
    pass

class TimestampMixin:
    """Mixin for adding created_at timestamp."""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
