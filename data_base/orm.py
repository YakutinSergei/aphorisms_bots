from difflib import SequenceMatcher

from data_base.database import async_session, engine_asinc, Base
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from data_base.model import UsersOrm, AphorismsORM


async def create_tables():
    # Начинаем асинхронную транзакцию с базой данных
    async with engine_asinc.begin() as conn:
        existing_tables = await conn.run_sync(Base.metadata.reflect)
        # Проверяем, есть ли информация о существующих таблицах
        if existing_tables is not None:
            for table_name, table in Base.metadata.tables.items():
                # Проверяем, есть ли текущая таблица в списке существующих таблиц
                if table_name not in existing_tables:
                    await conn.run_sync(table.create)
        else:
            # Если информация о существующих таблицах отсутствует,
            # создаем все таблицы из метаданных
            await conn.run_sync(Base.metadata.create_all)


async def add_users_bd(tg_id: int):
    try:
        async with async_session() as session:
            user = await session.execute(
                select(UsersOrm).filter(UsersOrm.tg_id == tg_id)
            )
            existing_user = user.scalar()

            if existing_user is None:
                # Если tg_id не найден, добавляем его в таблицу
                new_user = UsersOrm(tg_id=tg_id)
                session.add(new_user)
                await session.commit()
    except IntegrityError:
        # Обработка ошибки нарушения уникальности, если она возникнет
        return None  # Возвращаем None в случае ошибки

'''Добавление в базу данных афоризмов'''
async def add_aphorisms_bd(name: str, autor: str):
    try:
        async with async_session() as session:
            category_obj = AphorismsORM(name=name,
                                        autor=autor)

            session.add(category_obj)
            await session.commit()

    except IntegrityError:
        # Обработка ошибки нарушения уникальности, если она возникнет
        print(IntegrityError)


'''Добавление администратора'''


async def add_admin_bd(tg_id: int):
    try:
        async with async_session() as session:
            user = await session.execute(select(UsersOrm.tg_id).where(UsersOrm.tg_id == tg_id))
            user = user.scalar()
            if user:
                # Если пользователь найден, обновляем значение admin_check на True
                await session.execute(
                    update(UsersOrm).where(UsersOrm.tg_id == tg_id).values(admin_check=True)
                )
                await session.commit()  # Сохраняем изменения в базе данных
                return True
            else:
                # Если пользователь не найден, возвращаем False
                return False
    except IntegrityError:
        # Обработка ошибки нарушения уникальности, если она возникнет
        print(IntegrityError)

'''Удаление администратора'''

async def del_admin_bd(tg_id: int):
    try:
        async with async_session() as session:
            user = await session.execute(select(UsersOrm.tg_id).where(UsersOrm.tg_id == tg_id))
            user = user.scalar()
            if user:
                # Если пользователь найден, обновляем значение admin_check на True
                await session.execute(
                    update(UsersOrm).where(UsersOrm.tg_id == tg_id).values(admin_check=False)
                )
                await session.commit()  # Сохраняем изменения в базе данных
                return True
            else:
                # Если пользователь не найден, возвращаем False
                return False
    except IntegrityError:
        # Обработка ошибки нарушения уникальности, если она возникнет
        print(IntegrityError)


'''Вывести все афоризмы'''


async def get_all_aphorisms():
    try:
        async with async_session() as session:
            aphorisms = await session.execute(select(AphorismsORM.id, AphorismsORM.name, AphorismsORM.autor).
                                              order_by(AphorismsORM.id))
            user = aphorisms.all()
            return user
    except IntegrityError:
        # Обработка ошибки нарушения уникальности, если она возникнет
        print(IntegrityError)


'''Удаление афоризмов'''
async def deleting_aphorisms_kb(id_aphorism: int):
    try:
        async with async_session() as session:
            aphorism = await session.execute(select(AphorismsORM.id).where(AphorismsORM.id == id_aphorism))
            aphorism = aphorism.one()

            if aphorism:
                await session.execute(delete(AphorismsORM).where(AphorismsORM.id == id_aphorism))
                await session.commit()

                return True
            else:
                return False

    except IntegrityError:
        # Обработка ошибки нарушения уникальности, если она возникнет
        print(IntegrityError)