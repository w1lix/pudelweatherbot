from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


# основная клавиатура
def reply_keyboard_main() -> ReplyKeyboardMarkup:
    buttons = [

        [KeyboardButton(text='🏙 текущая погода')],
        [KeyboardButton(text='🌆 погода на завтра')],
        [KeyboardButton(text='🌌 погода на 8 дней')]

    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    return keyboard


# клавиатура вместе с отправкой геопозиции
def reply_keyboard_send_location() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text='🎈 отправить геопозицию', request_location=True)],

        [KeyboardButton(text='🏙 текущая погода'),
         KeyboardButton(text='🌆 погода на завтра'),
         KeyboardButton(text='🌌 погода на 8 дней')]

    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    return keyboard
