from datetime import datetime

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import BOT_TOKEN
from handlers.commands import Form
from keyboards.inline import to_detail_now, to_main_now
from keyboards.reply import reply_keyboard_main
from tools.create_response_owm import get_data_now, get_data_first
from tools.rework_dict import rework_now

router = Router()
bot = Bot(token=BOT_TOKEN)

days = ["понедельник", "вторник", "среда",
        "четверг", "пятница", "суббота", "воскресенье", "понедельник"]


# текущая погода
@router.message(Form.request_city_now, F.content_type.in_({'text', 'location'}))
async def tomorrow(m: Message, state: FSMContext) -> None:
    try:
        weekday = datetime.today().weekday()

        await bot.send_chat_action(m.chat.id, 'typing')

        # проверка, является ли сообщение локацией
        if not m.location:
            data = await get_data_now(await get_data_first(m.text))
            re_data = rework_now(data)
        else:
            data = await get_data_now(  # получение json погоды на сегодня
                [m.location.latitude, m.location.longitude])
            re_data = rework_now(data)  # переделывание словаря

        await m.answer_sticker(
            r"CAACAgIAAxkBAAEFxwRjGK96VU-SA-5NEkRlbKWVxzIDrgAC3AkAApek8EpUZ7lMIqYlaSkE",
            reply_markup=reply_keyboard_main())

        await m.reply(
            f"⭐️ {days[weekday]}, текущая погода <b>| {re_data['temp']}°:</b>\n\n"
            f"🏙 <b>температура:</b> {re_data['temp']}°\n"
            f"🌇 <b>ощущается как:</b> {re_data['feels_like']}°\n\n"
            f"🌺 <b>рассвет: </b>{re_data['sunrise'].strftime('%H:%M')}\n"
            f"🌸 <b>закат: </b>{re_data['sunset'].strftime('%H:%M')}\n"
            f"🌼 <b>световой день: </b>{re_data['ldr'][0]} ч {re_data['ldr'][1]} мин\n\n"
            f"<b><u>{re_data['descr']}</u></b>", reply_markup=to_detail_now())

        await state.clear()

        # добавление переменных в state для inline кнопок
        await state.update_data(city=m.text, re_data=re_data, wd=weekday)

    except KeyError:
        await m.answer_sticker(
            r'CAACAgIAAxkBAAEFzWNjHhsV_39aP-iBk7ghBQ7B4zpZ5AACgxAAAmuA8UvdlI_YEKj09ykE')
        await m.reply("😐 <b>ошибка!</b> введено некорректное название.\n↪️ <b>повторите попытку</b>")


# подробная информация
@router.callback_query(F.data == 'detail_now')
async def show_detail_info(c: CallbackQuery, state: FSMContext) -> None:
    await c.answer()

    try:
        # получение данных state из уже из выполненной функции
        state_data = await state.get_data()
        re_data = state_data['re_data']

        await c.message.edit_text(
            f"<b>🌟 текущая погода</b> <b>| {re_data['temp']}°:</b>\n\n"
            f"☁️ <b>облачность: </b>{re_data['clouds']}%\n"
            f"💧 <b>влажность: </b>{re_data['humidity']}%\n"
            f"💨 <b>скорость ветра: </b>{re_data['wind_speed']} м/c\n"
            f"🧭 <b>ветер: </b>{re_data['wind_direction']}\n"
            f"🌱 <b>точка росы: </b>{re_data['dew_point']}°\n"
            f"🌡 <b>давление: </b>{re_data['pressure']} мм рт. ст.\n"
            f"☀️ <b>УФ-индекс: </b>{re_data['uvi']}, {re_data['uvt']}\n\n"
            f"<b><u>{re_data['descr']}</u></b>", reply_markup=to_main_now())

    except KeyError:
        await c.message.edit_text("🫡 <b>нельзя изменять предыдущее сообщение "
                                  "с новым прогнозом!</b>")


# вернуться к сводке
@router.callback_query(F.data == "back_now")
async def show_main_info(c: CallbackQuery, state: FSMContext) -> None:
    await c.answer()

    try:
        # получение данных state из уже из выполненной функции
        state_data = await state.get_data()
        re_data = state_data['re_data']

        await c.message.edit_text(
            f"⭐️ <b>текущая погода</b> <b>| {re_data['temp']}°:</b>\n\n"
            f"🏙 <b>температура:</b> {re_data['temp']}°\n"
            f"🌇 <b>ощущается как:</b> {re_data['feels_like']}°\n\n"
            f"🌺 <b>рассвет: </b>{re_data['sunrise'].strftime('%H:%M')}\n"
            f"🌸 <b>закат: </b>{re_data['sunset'].strftime('%H:%M')}\n"
            f"🌼 <b>световой день: </b>{re_data['ldr'][0]} ч {re_data['ldr'][1]} мин\n\n"
            f"<b><u>{re_data['descr']}</u></b>", reply_markup=to_detail_now())

    except KeyError:
        await c.message.edit_text("🫡 <b>нельзя изменять предыдущее сообщение "
                                  "с новым прогнозом!</b>")
