from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload

from src.db.base_repository import BaseRepository
from src.db.postgres.models import Chats


class ChatsRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, chat_model: Chats) -> int:
        self.session.add(chat_model)
        await self.session.commit()
        return chat_model.id

    async def get_by_id(self, chat_id: int) -> Chats | None:
        query = (
            select(Chats)
            .filter(Chats.id == chat_id)
            .options(joinedload(Chats.participants))
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def update(self, id: int, **kwargs) -> None:
        query = update(Chats).where(Chats.id == id).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def delete(self, id: int) -> None:
        query = delete(Chats).where(Chats.id == id)
        await self.session.execute(query)
        await self.session.commit()

    async def list_by_creator_id(
        self,
        creator_id: int,
        limit: int,
        offset: int,
    ) -> list[Chats]:
        query = (
            select(Chats)
            .filter(Chats.creator_id == creator_id)
            .limit(limit)
            .offset(offset)
        )
        models = await self.session.execute(query)
        return models.scalars().all()
