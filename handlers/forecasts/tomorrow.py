from datetime import datetime
from pprint import pprint

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import BOT_TOKEN
from handlers.commands import Form
from keyboards.inline import to_detail_t, to_main_t
from keyboards.reply import reply_keyboard_main
from tools.create_response_owm import get_data_first, get_data_tomorrow
from tools.rework_dict import rework_forecast

days = ["понедельник", "вторник", "среда",
        "четверг", "пятница", "суббота", "воскресенье", "понедельник"]

router = Router()
bot = Bot(token=BOT_TOKEN)


@router.message(Form.request_city_tomorrow, F.content_type.in_({'text', 'location'}))
async def tomorrow(m: Message, state: FSMContext) -> None:
    weekday = datetime.today().weekday() + 1

    await bot.send_chat_action(m.chat.id, 'typing')
    # проверка, является ли сообщение локацией
    if not m.location:
        data_first = await get_data_first(m.text)
        data = await get_data_tomorrow(data_first[0])
        re_data = rework_forecast(data, data_first[1])
    else:
        data_first = await get_data_first(m.text)
        data = await get_data_tomorrow(  # получение json погоды на завтра
            [m.location.latitude, m.location.longitude])
        re_data = rework_forecast(data, data_first[1])  # переделывание словаря

    await m.answer_sticker(
        r"CAACAgIAAxkBAAEFxwRjGK96VU-SA-5NEkRlbKWVxzIDrgAC3AkAApek8EpUZ7lMIqYlaSkE",
        reply_markup=reply_keyboard_main())

    await m.reply(
        f"⭐️ <b>{days[weekday]}</b>, прогноз <b>| {re_data['temp_min']}/{re_data['temp_max']}</b>°:\n\n"
        f"🌄 <b>утром: </b>{re_data['morn']}°  <b>|</b>  ощущ: {re_data['flmorn']}°\n"
        f"🌁 <b>днем: </b>{re_data['day']}°  <b>|</b>  ощущ: {re_data['flday']}°\n"
        f"🌇 <b>вечером: </b>{re_data['eve']}°  <b>|</b>  ощущ: {re_data['fleve']}°\n"
        f"🌃 <b>ночью: </b>{re_data['night']}°  <b>|</b>  ощущ: {re_data['flnight']}°\n\n"
        f"🌺 <b>рассвет: </b>{re_data['sunrise'].strftime('%H:%M')}\n"
        f"🌸 <b>закат: </b>{re_data['sunset'].strftime('%H:%M')}\n"
        f"🌼 <b>световой день: </b>{re_data['ldr'][0]} ч {re_data['ldr'][1]} мин\n\n"
        f"<b><u>{re_data['descr']}</u></b>", reply_markup=to_detail_t())

    await state.clear()

    # добавление переменных в state для inline кнопок
    await state.update_data(city=m.text, re_data=re_data, wd=weekday)


# инлайн кнопка с подробной информацией
@router.callback_query(F.data == 'detail_t')
async def show_detail_info(c: CallbackQuery, state: FSMContext) -> None:
    await c.answer()

    try:
        # получение данных state из уже из выполненной функции
        state_data = await state.get_data()
        re_data = state_data['re_data']

        await c.message.edit_text(
            f"🌟 <b>{days[state_data['wd']]}</b>, прогноз <b>| {re_data['temp_min']}/{re_data['temp_max']}</b>°:\n\n"
            f"☁️ <b>облачность: </b>{re_data['clouds']}%\n"
            f"💧 <b>влажность: </b>{re_data['humidity']}%\n"
            f"💨 <b>скорость ветра: </b>{re_data['wind_speed']} м/c\n"
            f"🧭 <b>ветер: </b>{re_data['wind_direction']}\n"
            f"🌱 <b>точка росы: </b>{re_data['dew_point']}°\n"
            f"🌡 <b>давление: </b>{re_data['pressure']} мм рт. ст.\n"
            f"☀️ <b>УФ-индекс: </b>{re_data['uvi']}, {re_data['uvt']}\n"
            f"🌧 <b>вероятность осадков: </b>{re_data['pop']}%\n\n"
            f"<b><u>{re_data['descr']}</u></b>", reply_markup=to_main_t())

    except KeyError:
        await c.message.edit_text(" <b>нельзя изменять предыдущее сообщение "
                                  "с новым прогнозом! 🫡</b>")


# вернуться к сводке
@router.callback_query(F.data == "back_t")
async def show_main_info(c: CallbackQuery, state: FSMContext) -> None:
    await c.answer()

    try:
        # получение данных state из уже из выполненной функции
        state_data = await state.get_data()
        re_data = state_data['re_data']

        await c.message.edit_text(
            f"⭐️ <b>{days[state_data['wd']]}</b>, прогноз <b>| {re_data['temp_min']}/{re_data['temp_max']}</b>°:\n\n"
            f"🌄 <b>утром: </b>{re_data['morn']}°  <b>|</b>  ощущ: {re_data['flmorn']}°\n"
            f"🌁 <b>днем: </b>{re_data['day']}°  <b>|</b>  ощущ: {re_data['flday']}°\n"
            f"🌇 <b>вечером: </b>{re_data['eve']}°  <b>|</b>  ощущ: {re_data['fleve']}°\n"
            f"🌃 <b>ночью: </b>{re_data['night']}°  <b>|</b>  ощущ: {re_data['flnight']}°\n\n"
            f"🌺 <b>рассвет: </b>{re_data['sunrise'].strftime('%H:%M')}\n"
            f"🌸 <b>закат: </b>{re_data['sunset'].strftime('%H:%M')}\n"
            f"🌼 <b>световой день: </b>{re_data['ldr'][0]} ч {re_data['ldr'][1]} мин\n\n"
            f"<b><u>{re_data['descr']}</u></b>", reply_markup=to_detail_t())

    except KeyError:
        await c.message.edit_text(" <b>нельзя изменять предыдущее сообщение "
                                  "с новым прогнозом! 🫡</b>")
