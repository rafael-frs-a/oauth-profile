import sqlalchemy as sa
from datetime import datetime
from sqlmodel import SQLModel, Field
from src.db import config


class TimestampModel(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column=sa.Column(sa.DateTime, onupdate=datetime.utcnow)
    )


def get_key() -> str:
    return config.DB_ENCRYPTION_KEY
