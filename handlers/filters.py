import asyncpg

from datetime import datetime
from aiogram.filters import BaseFilter
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, func, and_

from aiogram.types import Message
from environs import Env

from create_bot import bot
from data_base.database import async_session
from data_base.model import UsersOrm


class AdminUser(BaseFilter):
    async def __call__(self, message: Message):
        try:
            async with async_session() as session:
                tg_ids = await session.execute(select(UsersOrm.tg_id)
                                               .where(and_(UsersOrm.admin_check == True,
                                                           UsersOrm.tg_id == message.from_user.id)))
                if tg_ids.scalar():
                    return True
                else:
                    return False

        except IntegrityError:
            # Обработка ошибки нарушения уникальности, если она возникнет
            return False  # Возвращаем None в случае ошибки