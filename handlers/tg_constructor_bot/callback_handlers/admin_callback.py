from config.states import States
from create_bot import bot
from db.db import DB
from keyboards.keyboards import *
from telegram import ParseMode


async def admin_callback(call, chat_id, message_id):
    db = DB()
    states = States()
    
    
    if call.data == "popup_in_this_bot":
        data = db.get_storage(chat_id)
        data["popup_in_bot"] = call.data
        db.update_storage(chat_id, data)
        
        db.update_state(chat_id, states.find_user)

        return await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="<b>Введите ID или @username пользователя:</b>",
            parse_mode=ParseMode.HTML
        )
        
    if call.data == "popup_in_another_bot":
        data = db.get_storage(chat_id)
        data["popup_in_bot"] = call.data
        db.update_storage(chat_id, data)
        
        db.update_state(chat_id, states.find_bot)

        return await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="<b>Введите @usernamebot бота:</b>",
            parse_mode=ParseMode.HTML
        )
