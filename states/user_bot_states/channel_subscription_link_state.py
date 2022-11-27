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
    channel_link = message.text
    
    if len(channel_link) <= 200:
        db.update_bot_subscription_channel_link(current_bot, channel_link)
            
        await bot.send_photo(
            chat_id=chat_id, 
            caption=f"<b>Ссылка на канал изменена на {channel_link}.</b>",
            photo=photo,
            parse_mode=ParseMode.HTML,
            reply_markup=kb.back_to_user_bot_info_kb()
        )
        
        db.update_state(chat_id, states.main_state)
    else:
        await bot.send_photo(
            chat_id=chat_id, 
            caption=f"<b>Введите корректную ссылку на канал.</b>",
            photo=photo,
            parse_mode=ParseMode.HTML,
            reply_markup=kb.back_to_user_bot_info_kb()
        )