from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from aiogram.types import Message, CallbackQuery

from bot_menu.menu import create_inline_kb, viewing_aphorisms_kb
from create_bot import bot
from data_base.orm import add_aphorisms_bd, add_admin_bd, del_admin_bd, get_all_aphorisms, deleting_aphorisms_kb
from handlers.filters import AdminUser

router: Router = Router()
router.message.filter(AdminUser())
router.callback_query.filter(AdminUser())

class FSMaphorisms(StatesGroup):
    aphorisms = State()
    autor = State()
    admin = State()
    admin_del = State()


@router.message(F.text == '/menu')
async def menu_admin(message: Message):
    await message.answer(text='🔽Выберите действие🔽',
                         reply_markup=await create_inline_kb(2,
                                                       'admin_menu',
                                                       'Добавить администратора',
                                                       'Удалить администратора',
                                                       'Добавить афоризм',
                                                       'Просмотр афоризмов'
                                                       ))


'''Добавляем афоризм'''

@router.callback_query(F.data.endswith('Добавить афоризм'))
async def add_aphorisms(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Отправьте афоризм боту')
    await state.set_state(FSMaphorisms.aphorisms)
    await callback.answer()


'''Добавление афоризма'''
@router.message(StateFilter(FSMaphorisms.aphorisms))
async def enter_aphorisms(message: Message, state: FSMContext):
    if message.text:
        await message.answer(text='Отправьте автора афоризма боту')
        await state.update_data(aphorisms=message.text)
        await state.set_state(FSMaphorisms.autor)
    else:
        await message.answer(text='Вы отправили не текст. Попробуйте еще раз')

'''Добавление автора афоризма'''
@router.message(StateFilter(FSMaphorisms.autor))
async def enter_aphorisms_autor(message: Message, state: FSMContext):
    if message.text:
        aphorisms = await state.get_data()
        await add_aphorisms_bd(name=aphorisms['aphorisms'], autor=message.text)
        await state.clear()
    else:
        await message.answer(text='Вы отправили не текст. Попробуйте еще раз')


'''Добавление администратора'''


@router.callback_query(F.data.endswith('Добавить администратора'))
async def add_admin(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMaphorisms.admin)
    await callback.message.answer(text='Пришли ID-телеграм пользователя или перешлите боту его сообщение')
    await callback.answer()


'''Включение в базу данных'''
@router.message(StateFilter(FSMaphorisms.admin))
async def enter_admin(message: Message, state: FSMContext):
    if message.text.isdigit():
        id = int(message.text)
        add = await add_admin_bd(tg_id=id)
        if add:
            await message.answer(text='Администратора добавлен')
        else:
            await message.answer(text='Пользователь в базе не найден')

    elif message.forward_date:
        id = int(message.forward_from.id)
        add = await add_admin_bd(tg_id=id)
        if add:
            await message.answer(text='Администратора добавлен')
        else:
            await message.answer(text='Пользователь в базе не найден')
        await state.clear()
    else:
        await message.answer(text='Пришли ID-телеграм пользователя или перешлите боту его сообщение')



'''удаление администратора'''


@router.callback_query(F.data.endswith('Добавить администратора'))
async def add_admin(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMaphorisms.admin_del)
    await callback.message.answer(text='Пришли ID-телеграм пользователя или перешлите боту его сообщение')
    await callback.answer()


'''Включение в базу данных'''
@router.message(StateFilter(FSMaphorisms.admin))
async def enter_admin(message: Message, state: FSMContext):
    if message.text.isdigit():
        id = int(message.text)
        add = await del_admin_bd(tg_id=id)
        if add:
            await message.answer(text='Администратора добавлен')
        else:
            await message.answer(text='Пользователь в базе не найден')

    elif message.forward_date:
        id = int(message.forward_from.id)
        add = await del_admin_bd(tg_id=id)
        if add:
            await message.answer(text='Администратора добавлен')
        else:
            await message.answer(text='Пользователь в базе не найден')
        await state.clear()
    else:
        await message.answer(text='Пришли ID-телеграм пользователя или перешлите боту его сообщение')


'''Просмотр афоризмов'''


@router.callback_query(F.data.endswith('Просмотр афоризмов'))
async def viewing_aphorisms(callback: CallbackQuery, state: FSMContext):
    all_aphorisms = await get_all_aphorisms()
    if all_aphorisms:
        id_aphorisms = all_aphorisms[0][0]
        name = all_aphorisms[0][1]
        autor = all_aphorisms[0][2]
        await callback.message.answer(text=f'{name}\n\n'
                                                    f'<b><i>{autor}</i></b>',
                                      reply_markup= await viewing_aphorisms_kb(id_aphorisms=id_aphorisms,
                                                                               items=0,
                                                                               len_ap=len(all_aphorisms)))
    else:
        await callback.message.answer(text='В базе нет афоризмов')
    await callback.answer()


'''Нажатия кнопок на просмотре афоризмов'''
@router.callback_query(F.data.startswith('viewing_'))
async def enter_button_viewing(callback: CallbackQuery):
    action = callback.data.split('_')[-1]
    all_aphorisms = await get_all_aphorisms()
    items = int(callback.data.split('_')[1])
    if all_aphorisms:
        if action == 'back':
            if items > 0:
                id_aphorisms = all_aphorisms[items-1][0]
                name = all_aphorisms[items-1][1]
                autor = all_aphorisms[items-1][2]
                await bot.edit_message_text(chat_id=callback.from_user.id,
                                            message_id=callback.message.message_id,
                                            text=f'{name}\n\n'
                                                   f'<b><i>{autor}</i></b>',
                                            reply_markup=await viewing_aphorisms_kb(id_aphorisms=id_aphorisms,
                                                                                    items=items-1,
                                                                                    len_ap=len(all_aphorisms)))
        elif action == 'forward':
            if items < len(all_aphorisms)-1:
                id_aphorisms = all_aphorisms[items+1][0]
                name = all_aphorisms[items+1][1]
                autor = all_aphorisms[items+1][2]
                await bot.edit_message_text(chat_id=callback.from_user.id,
                                            message_id=callback.message.message_id,
                                            text=f'{name}\n\n'
                                                 f'<b><i>{autor}</i></b>',
                                            reply_markup=await viewing_aphorisms_kb(id_aphorisms=id_aphorisms,
                                                                                    items=items + 1,
                                                                                    len_ap=len(all_aphorisms)))
    else:
        await callback.message.answer(text='В базе нет афоризмов')
    await callback.answer()

'''Удаление афоризмов'''
@router.callback_query(F.data.startswith('delite_'))
async def delete_aphorisms(callback: CallbackQuery):
    id_aphorisms = callback.data.split('_')[1]
    check_del = await deleting_aphorisms_kb(id_aphorism=int(id_aphorisms))

    if check_del:
        all_aphorisms = await get_all_aphorisms()
        items = int(callback.data.split('_')[-1])
        if items >= len(all_aphorisms):
            items -= 1
        id_aphorisms = all_aphorisms[0][0]
        name = all_aphorisms[items][1]
        autor = all_aphorisms[items][2]
        await bot.edit_message_text(chat_id=callback.from_user.id,
                                    message_id=callback.message.message_id,
                                    text=f'{name}\n\n'
                                         f'<b><i>{autor}</i></b>',
                                    reply_markup=await viewing_aphorisms_kb(id_aphorisms=id_aphorisms,
                                                                            items=items,
                                                                            len_ap=len(all_aphorisms)))
    else:
        await callback.message.answer(text='Афоризм уже удален')