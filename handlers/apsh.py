import random
from datetime import datetime, timedelta

from create_bot import bot
from data_base.database import async_session, engine_asinc, Base
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError

from data_base.model import UsersOrm, AphorismsORM



'''Добавление цепей'''
async def mailing():
    try:
        async with async_session() as session:
            # Получаем все записи из таблицы aphorisms
            aphorisms = await session.execute(select(AphorismsORM.name, AphorismsORM.autor).order_by(func.random()))
            aphorisms = aphorisms.first()
            print(aphorisms)

            tg_ids = await session.execute(select(UsersOrm.tg_id))
            print(tg_ids.all())

            if aphorisms:
                tg_ids = await session.execute(select(UsersOrm.tg_id))
                tg_ids = tg_ids.all()
                for i in range(len(tg_ids)):
                    try:
                        await bot.send_message(chat_id=tg_ids[i][0],
                                               text=f'{aphorisms[0]}\n\n'
                                                    f'<b><i>{aphorisms[1]}</i></b>')
                    except Exception as _ex:
                        print('[INFO] Error ', _ex)

            else:
                tg_ids = await session.execute(select(UsersOrm.tg_id).filter(UsersOrm.admin_check == True))
                tg_ids = tg_ids.all()
                for i in range(len(tg_ids)):
                    try:
                        await bot.send_message(chat_id=tg_ids[i][0],
                                               text='База данных пустая')
                    except Exception as _ex:
                        print('[INFO] Error ', _ex)

    except IntegrityError:
        print('[INFO] Error ', IntegrityError)