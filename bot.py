import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import commands
from handlers.forecasts import tomorrow, now


async def main() -> None:
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    logging.basicConfig(level=logging.INFO)

    dp.include_router(commands.router)
    dp.include_routers(now.router, tomorrow.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
