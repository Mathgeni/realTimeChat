from sqlalchemy import delete
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.db.base_repository import BaseRepository
from src.db.postgres.models import Participants


class ParticipantsRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, participants_model: Participants) -> int:
        self.session.add(participants_model)
        await self.session.commit()
        return participants_model.id

    async def delete(self, id: int) -> None:
        query = delete(Participants).where(Participants.id == id)
        await self.session.execute(query)
        await self.session.commit()
