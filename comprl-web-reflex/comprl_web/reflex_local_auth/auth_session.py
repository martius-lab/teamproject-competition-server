import datetime

from sqlmodel import Column, DateTime, Field, func, String

import reflex as rx

from comprl.server.data.sql_backend import Base

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column


class LocalAuthSession(
    Base,
):
    """Correlate a session_id with an arbitrary user_id."""

    __tablename__ = "auth_sessions"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(index=True, nullable=False)
    session_id: Mapped[str] = mapped_column(
        sa.String(255), unique=True, index=True, nullable=False
    )
    expiration: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
