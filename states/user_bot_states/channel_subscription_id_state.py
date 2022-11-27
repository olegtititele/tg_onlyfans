from aiogram import Dispatcher, types
from aiogram.types import InputFile
from config.states import States
from create_bot import bot
from keyboards.keyboards import *
from telegram import ParseMode


async def message_handler(message: types.Message, chat_id):
    db = DB()
    kb = Keyboards()
    states = States()
    
    photo = InputFile("background.jpg")
    current_bot = db.get_current_bot(chat_id)
    channel_id = message.text
    
    if channel_id[0] == "-":
        if channel_id[1::].isdigit():
            db.update_bot_subscription_channel_id(current_bot, channel_id)
            
            await bot.send_photo(
                chat_id=chat_id, 
                caption=f"<b>ID канала изменено на {channel_id}.</b>",
                photo=photo,
                parse_mode=ParseMode.HTML,
                reply_markup=kb.back_to_user_bot_info_kb()
            )
            
            db.update_state(chat_id, states.main_state)
        else:
            await bot.send_photo(
                chat_id=chat_id, 
                caption=f"<b>ID канала должно быть числом. Попробуйте еще раз.</b>",
                photo=photo,
                parse_mode=ParseMode.HTML,
                reply_markup=kb.back_to_user_bot_info_kb()
            )
    else:
        await bot.send_photo(
            chat_id=chat_id, 
            caption=f"<b>Цена должна начинаться с \"-\". Попробуйте еще раз.</b>",
            photo=photo,
            parse_mode=ParseMode.HTML,
            reply_markup=kb.back_to_user_bot_info_kb()
        )