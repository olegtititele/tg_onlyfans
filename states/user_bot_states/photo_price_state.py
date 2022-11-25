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
    price = message.text.replace(',', '.')
    
    try:
        if float(price) > 0:
            db.update_user_bot_photo_price(current_bot, price)
            
            await bot.send_photo(
                chat_id=chat_id, 
                caption=f"<b>Цена за фото изменена на {price} ₽.</b>",
                photo=photo,
                parse_mode=ParseMode.HTML,
                reply_markup=kb.back_to_user_bot_info_kb()
            )
            db.update_state(chat_id, states.main_state)
        else:
            await bot.send_photo(
                chat_id=chat_id, 
                caption=f"<b>Цена должна быть больше 0. Попробуйте еще раз.</b>",
                photo=photo,
                parse_mode=ParseMode.HTML,
                reply_markup=kb.back_to_user_bot_info_kb()
            )
    except:
        await bot.send_photo(
            chat_id=chat_id, 
            caption=f"<b>Цена должна быть числом. Попробуйте еще раз.</b>",
            photo=photo,
            parse_mode=ParseMode.HTML,
            reply_markup=kb.back_to_user_bot_info_kb()
        )
