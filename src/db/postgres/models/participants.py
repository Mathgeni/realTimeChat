from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.postgres import Base


if TYPE_CHECKING:
    from src.db.postgres.models import Chats

from src.db.postgres.models.base_model import BasePostgresAlchemyModel


class Participants(Base, BasePostgresAlchemyModel):
    __tablename__ = "participants"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(64), index=False)
    user_id: Mapped[int] = mapped_column(BigInteger(), index=False)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), index=True)

    chats: Mapped[list["Chats"]] = relationship(back_populates="participants")

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "chat_id",
            name="chat_id_user_id_constraint",
        ),
    )
