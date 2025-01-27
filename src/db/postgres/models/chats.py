from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.postgres import Base


if TYPE_CHECKING:
    from src.db.postgres.models import Messages, Participants

from src.db.postgres.models.base_model import BasePostgresAlchemyModel


class Chats(Base, BasePostgresAlchemyModel):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(64), index=False)
    creator_id: Mapped[int] = mapped_column(BigInteger, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(), index=False, server_default=func.now()
    )

    messages: Mapped[list["Messages"]] = relationship()
    participants: Mapped[list["Participants"]] = relationship(
        back_populates="chats"
    )

    __table_args__ = (
        UniqueConstraint(
            "name",
            "creator_id",
            name="name_user_id_constraint",
        ),
    )
