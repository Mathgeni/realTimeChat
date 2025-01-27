from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.db.postgres import Base
from src.db.postgres.models.base_model import BasePostgresAlchemyModel


class Messages(Base, BasePostgresAlchemyModel):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), index=True)
    sender_id: Mapped[int] = mapped_column(BigInteger(), index=True)
    content: Mapped[str] = mapped_column(Text(), index=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        index=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        index=False,
        server_default=func.now(),
    )
