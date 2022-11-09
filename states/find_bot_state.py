from aiogram import Dispatcher, types
from config.states import States
from create_bot import bot
from keyboards.keyboards import *
from telegram import ParseMode


async def message_handler(message: types.Message, chat_id):
    db = DB()
    kb = Keyboards()
    states = States()
    searched_bot = message.text
        
    try:
        if "@" in searched_bot:
            searched_bot = searched_bot.split("@")[1]

        db.get_user_bot(searched_bot)
        data = db.get_storage(chat_id)
        data["popup_bot"] = searched_bot
        db.update_storage(chat_id, data)
        
        db.update_state(chat_id, states.find_user)
        
        await bot.send_message(
            chat_id=chat_id,
            text="<b>Введите ID или @username пользователя:</b>",
            parse_mode=ParseMode.HTML
        )
    except:
        text = f"<b>Бот @{searched_bot} не найден. Попробуйте еще раз.</b>"
        await bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=ParseMode.HTML
        )