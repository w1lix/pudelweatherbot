from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# основная информация текущей погоды
def to_main_now() -> InlineKeyboardMarkup:
    button = [
        [InlineKeyboardButton(text="◀ вернуться к сводке", callback_data='back_now')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=button)

    return keyboard


# детальная информация текущей погоды
def to_detail_now() -> InlineKeyboardMarkup:
    button = [
        [InlineKeyboardButton(text='😶‍🌫️ детальная информация', callback_data="detail_now")]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=button)

    return keyboard


# основная информация прогноза на завтра
def to_main_t() -> InlineKeyboardMarkup:
    button = [
        [InlineKeyboardButton(text="◀ вернуться к сводке", callback_data='back_t')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=button)

    return keyboard


# детальная информация прогноза на завтра
def to_detail_t() -> InlineKeyboardMarkup:
    button = [
        [InlineKeyboardButton(text='😶‍🌫️ детальная информация', callback_data="detail_t")]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=button)

    return keyboard
