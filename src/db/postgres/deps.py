from typing import Callable, TypeVar

from src.db.base_repository import BaseRepository
from src.db.postgres import Session


BaseRepositoryType = TypeVar("BaseRepositoryType", bound=BaseRepository)


def get_postgres_repository(
    repository: BaseRepositoryType,
) -> Callable[[], BaseRepositoryType]:
    async def wrapper() -> BaseRepositoryType:
        async with Session() as session:
            return repository(session)

    return wrapper
