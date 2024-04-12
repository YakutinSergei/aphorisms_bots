import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine

from Config_Data.config import settings


#Асинхроно
engine_asinc = create_async_engine(
    url=settings.DATADASE_URL_asyncpg,
    echo=False  # Что бы сыпались все запросы в консоль
)

async_session = async_sessionmaker(engine_asinc)


class Base(DeclarativeBase):
    pass