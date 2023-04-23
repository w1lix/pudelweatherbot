from aiogram import Router, html, F
from aiogram.filters import Text, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from keyboards.reply import reply_keyboard_main, reply_keyboard_send_location

router = Router()


class Form(StatesGroup):
    request_city_now = State()
    request_city_tomorrow = State()


# старт :D
@router.message(Command('start'))
async def cmd_start(m: Message, state: FSMContext) -> None:
    await state.clear()

    await m.answer(f"👻 привет, {html.bold(html.quote(m.from_user.first_name))}!"
                   f" 👻 \n🌤️ я <b>погодный</b> бот от <b>@takilow</b>\n\n"
                   f"я могу узнать <b>погоду</b> на <b>завтра</b>, <b>сегодня</b>\n"
                   f"<b>и даже на 8 дней!</b> 😎\n\n"
                   f"✨ <b>используй кнопки ниже чтобы управлять мной</b>\n\n"
                   f"<b>также для удобства ты можешь отправить мне свою геопозицию, "
                   f"чтобы тебе не пришлось постоянно вводить свой город 🤔</b>\n\n"
                   f"💗 <b>приятного использования</b>", reply_markup=reply_keyboard_main())


# установка state для хендлера now
@router.message(F.text == "🏙 текущая погода")
async def request_the_city_now(m: Message, state: FSMContext) -> None:
    await state.clear()

    await m.reply("<b>🗺 отправьте геопозицию</b> или \n"
                  "<b>🦋 введите город</b>: ", reply_markup=reply_keyboard_send_location())

    await state.set_state(Form.request_city_now)


# установка state для хендлера tomorrow
@router.message(F.text == '🌆 погода на завтра')
async def request_the_city_tomorrow(m: Message, state: FSMContext) -> None:
    await state.clear()

    await m.reply("<b>🗺 отправьте геопозицию</b> или \n"
                  "<b>🦋 введите город</b>: ", reply_markup=reply_keyboard_send_location())

    await state.set_state(Form.request_city_tomorrow)


@router.message(Text('🌌 погода на 8 дней'))
async def cmd_start(m: Message, state: FSMContext):
    await state.clear()
    await m.answer("в разработке :( ")


@router.message(Command('negr'))
async def negr(m: Message) -> None:
    await m.answer("negr", reply_markup=None)
