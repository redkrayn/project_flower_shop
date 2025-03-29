import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'TeamProject2_Flower.settings'
import django
django.setup()
import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from Handlers.handlers import user_private_router
from Common.bot_cmds_list import private
from dotenv import load_dotenv


async def main():
    load_dotenv()
    dp = Dispatcher()
    dp.include_routers(user_private_router)
    bot_token = os.getenv('BOT_TG_TOKEN')
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=bot_token)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('EXIT')
