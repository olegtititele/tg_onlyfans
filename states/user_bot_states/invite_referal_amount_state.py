from aiogram import types
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
    sum = message.text.replace(',', '.')
    
    try:
        sum = float(sum)
        if sum >= 1 and sum <= 1000:
            db.update_bot_invited_ref_sum(current_bot, sum)
            
            await bot.send_photo(
                chat_id=chat_id, 
                caption=f"<b>Cумма реферала за приглашенного человека изменена на {sum} ₽.</b>",
                photo=photo,
                parse_mode=ParseMode.HTML,
                reply_markup=kb.back_to_user_bot_info_kb()
            )
            db.update_state(chat_id, states.main_state)
        else:
            await bot.send_photo(
                chat_id=chat_id, 
                caption=f"<b>Cумма реферала за приглашенного человека должна быть больше 1 и меньше 1000. Попробуйте еще раз.</b>",
                photo=photo,
                parse_mode=ParseMode.HTML,
                reply_markup=kb.back_to_user_bot_info_kb()
            )
    except:
        await bot.send_photo(
            chat_id=chat_id, 
            caption=f"<b>Cумма реферала за приглашенного человека должна быть числом. Попробуйте еще раз.</b>",
            photo=photo,
            parse_mode=ParseMode.HTML,
            reply_markup=kb.back_to_user_bot_info_kb()
        )