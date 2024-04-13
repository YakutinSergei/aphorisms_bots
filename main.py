import asyncio
import logging
from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.types import BotCommand
from pytz import timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from create_bot import bot, dp
from environs import Env

from data_base.orm import create_tables
from handlers import admin_handlers, start_handlers
from handlers.apsh import mailing

env = Env()
env.read_env()

# Инициализируем логгер
logger = logging.getLogger(__name__)


async def set_main_menu(bot: Bot):

    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/menu', description='Меню')]

    await bot.set_my_commands(main_menu_commands)

async def main():

    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    '''Подключаем базу данных'''
    await create_tables() # Создание таблиц

    # Регистриуем роутеры в диспетчере
    dp.include_router(start_handlers.router)
    dp.include_router(admin_handlers.router)

    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    start_date = datetime.now().replace(hour=20, minute=0, second=0, microsecond=0) + timedelta(days=1)
    scheduler.add_job(mailing, 'interval', hours=6, start_date=start_date)
    scheduler.start()
   
    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup.register(set_main_menu)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

