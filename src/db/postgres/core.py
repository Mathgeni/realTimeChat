import json
from datetime import date, datetime

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import AsyncAdaptedQueuePool

from src.configs import db_settings


Base = declarative_base()


def json_dumps_default(val):
    if isinstance(val, datetime) or isinstance(val, date):
        return val.isoformat()
    raise TypeError()


def json_serializer(d):
    return json.dumps(d, default=json_dumps_default)


engine: AsyncEngine = create_async_engine(
    db_settings.POSTGRES_URL,
    poolclass=AsyncAdaptedQueuePool,
    echo=False,
    json_serializer=json_serializer,
    pool_size=100,
    max_overflow=100,
)

Session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine, expire_on_commit=False, autocommit=False, autoflush=False
)
