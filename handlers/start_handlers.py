from aiogram import Router, F
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from data_base.orm import add_users_bd

router: Router = Router()


class FSMcategory_add(StatesGroup):
    category = State()


@router.message(CommandStart())
async def process_start_command(message: Message):
    tg_id = int(message.from_user.id) if message.chat.type == 'private' else int(message.chat.id)
    await add_users_bd(tg_id=tg_id)