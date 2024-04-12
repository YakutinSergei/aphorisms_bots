from aiogram import Router, F
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

router: Router = Router()


@router.message(F.text == '/menu')
async def menu_admin(message: Message):
    pass

