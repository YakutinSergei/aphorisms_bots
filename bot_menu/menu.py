from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
'''генератор клавиатур'''


async def create_inline_kb(width: int,
                           pref: str,
                           *args: str,
                           **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=button,
                callback_data=pref + button))

    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=pref + button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


'''Клавиатура просмотра афоризмов'''

async def viewing_aphorisms_kb(id_aphorisms: str,
                               items: int,
                               len_ap:int) -> InlineKeyboardMarkup:
    inline_markup: InlineKeyboardBuilder = InlineKeyboardBuilder()

    buttons: list[InlineKeyboardButton] = [InlineKeyboardButton(
        text='⏪',
        callback_data=f'viewing_{items}_back'
    ), InlineKeyboardButton(
        text=f'{items+1}/{len_ap}',
        callback_data=f'viewing_123'
    ), InlineKeyboardButton(
        text='⏩',
        callback_data=f'viewing_{items}_forward'
    )
    ]
    inline_markup.row(*buttons, width=3)

    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = [InlineKeyboardButton(
        text='❌Удалить',
        callback_data=f'delite_{id_aphorisms}_{items}'
    )
    ]
    inline_markup.row(*buttons, width=1)
    return inline_markup.as_markup()