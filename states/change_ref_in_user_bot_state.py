from aiogram import Dispatcher, types
from config.states import States
from create_bot import bot
from keyboards.keyboards import *
from telegram import ParseMode


async def message_handler(message: types.Message, chat_id):
    db = DB()
    states = States()
    
    percentage = message.text
    
    if percentage.isdigit():
        if int(percentage) > 0 and int(percentage) < 100:
            db.update_referal_bonus_in_user_bot(int(percentage))
            
            await bot.send_message(
                chat_id=chat_id, 
                text=f"<b>Процент реферала изменен на {percentage}%.</b>",
                parse_mode=ParseMode.HTML
            )
            
            db.update_state(chat_id, states.main_state)
        else:
            await bot.send_message(
                chat_id=chat_id, 
                text=f"<b>Процент реферала должен быть больше 0 и меньше 100. Попробуйте еще раз.</b>",
                parse_mode=ParseMode.HTML
            )
    else:
        await bot.send_message(
            chat_id=chat_id, 
            text=f"<b>Процент реферала должен быть числом. Попробуйте еще раз.</b>",
            parse_mode=ParseMode.HTML
        )