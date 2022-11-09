from aiogram import Dispatcher, types
from config.states import States
from create_bot import bot
from keyboards.keyboards import *
from telegram import ParseMode

async def message_handler(message: types.Message, chat_id):
    db = DB()
    kb = Keyboards()
    states = States()
    searched_user = message.text
        
    try:
        if "@" in searched_user:
            searched_user = searched_user.split("@")[1]

        
        data = db.get_storage(chat_id)
        if data["popup_in_bot"] == "popup_in_this_bot":
            user = db.get_user(searched_user)
            
            user_id = user[0]
            username = user[1]
        else:
            user = db.get_user_from_user_bot(data["popup_bot"], searched_user)
            
            user_id = user[0]
            username = user[1]
        
        data = db.get_storage(chat_id)
        data["popup_user_id"] = user_id
        db.update_storage(chat_id, data)
        
        db.update_state(chat_id, states.change_balance)
        
        await bot.send_message(
            chat_id=chat_id,
            text=f"<b>Пользователь @{username}.\n\nВведите сумму зачисления:</b>",
            parse_mode=ParseMode.HTML
        )

    except:
        if searched_user.isdigit():
            text = f"<b>Пользователь c ID {searched_user} не найден. Попробуйте еще раз.</b>"
            await bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=ParseMode.HTML
            )
        else:
            text = f"<b>Пользователь {searched_user} не найден. Попробуйте еще раз.</b>"
            await bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=ParseMode.HTML
            )
