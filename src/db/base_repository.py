from abc import ABCMeta
from typing import Any


class BaseRepository(metaclass=ABCMeta):
    def __init__(self, session: Any) -> None:
        self.session = session

    async def create(self, *args, **kwargs) -> int:
        raise NotImplementedError

    async def update(self, id: int, **kwargs) -> Any:
        raise NotImplementedError

    async def delete(self, id: int) -> None:
        raise NotImplementedError

    async def get_by_id(self, id: int) -> Any:
        raise NotImplementedError
