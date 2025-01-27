from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.db.base_repository import BaseRepository
from src.db.postgres.models import Messages


class MessagesRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, message_model: Messages) -> Messages:
        self.session.add(message_model)
        await self.session.commit()
        return message_model

    async def get_by_id(self, message_id: int) -> Messages | None:
        query = select(Messages).filter(Messages.id == message_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def list_messages(
        self,
        chat_id: int,
        limit: int,
        offset: int,
    ) -> list[Messages]:
        query = (
            select(Messages)
            .filter(Messages.chat_id == chat_id)
            .limit(limit)
            .offset(offset)
            .order_by(Messages.id.desc())
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, id: int, **kwargs) -> None:
        query = update(Messages).where(Messages.id == id).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def delete(self, id: int) -> None:
        query = delete(Messages).where(Messages.id == id)
        await self.session.execute(query)
        await self.session.commit()
