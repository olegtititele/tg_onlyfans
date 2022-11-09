from aiogram import Bot, Dispatcher

import config.config as cf

bot = Bot(token=cf.TOKEN)
dp = Dispatcher(bot)
