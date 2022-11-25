import asyncio

from aiogram import Dispatcher, types
from aiogram.types import InputFile
from config.states import States
from create_bot import bot
from keyboards.keyboards import *
from telegram import ParseMode

import handlers.tg_user_bot.userbot as userbot
from handlers.tg_user_bot.methods import get_me


async def message_handler(message: types.Message, chat_id):
    db = DB()
    kb = Keyboards()
    states = States()
    photo = InputFile("background.jpg")
    token = message.text
    
    try:
        bots = db.get_user_bots(chat_id)
        bot_username = (await get_me(token))['result']['username']
        if (await bot.get_me()).username == bot_username:
            return await bot.send_photo(
                chat_id=chat_id, 
                caption=f"<b>Нельзя использовать токен бота конструктора! Введите корректный токен бота!</b>",
                photo=photo,
                parse_mode=ParseMode.HTML,
                reply_markup=kb.back_to_user_bots_list_kb()
            )
        if bot_username not in bots:
            asyncio.create_task(userbot.run(token))
            db.add_new_bot(bot_username, token, chat_id, message.from_user.username)
            db.create_bot_table(bot_username)
            
            await bot.send_photo(
                chat_id=chat_id, 
                caption=f"<b>✔️ Успешно! Бот @{bot_username} запущен.</b>",
                photo=photo,
                parse_mode=ParseMode.HTML,
                reply_markup=kb.back_to_user_bots_list_kb()
            )
            
            db.update_state(chat_id, states.main_state)
        else:
            await bot.send_photo(
                chat_id=chat_id, 
                caption=f"<b>Бот @{bot_username} уже добавлен.</b>",
                photo=photo,
                parse_mode=ParseMode.HTML,
                reply_markup=kb.back_to_user_bots_list_kb()
            )
    except Exception as e:
        print(e)
        await bot.send_photo(
            chat_id=chat_id, 
            caption=f"<b>Введите корректный токен бота!</b>",
            photo=photo,
            parse_mode=ParseMode.HTML,
            reply_markup=kb.back_to_user_bots_list_kb()
        )