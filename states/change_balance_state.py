from aiogram import Dispatcher, types
from config.states import States
from create_bot import bot
from keyboards.keyboards import *
from telegram import ParseMode

async def message_handler(message: types.Message, chat_id):
    db = DB()
    states = States()
    popup_sum = message.text.replace(',', '.')
        
    try:
        if float(popup_sum) > 0:
            data = db.get_storage(chat_id)
            popup_user_id = data["popup_user_id"]
            
                        
            if data["popup_in_bot"] == "popup_in_this_bot":
                old_balance = db.get_balance(popup_user_id)
                new_balance = old_balance + float(popup_sum)
                db.update_balance(popup_user_id, new_balance)
                
                await bot.send_message(
                    chat_id=popup_user_id, 
                    text=f"<b>Ваш пополнен на {popup_sum} ₽. Теперь ваш баланс составляет {new_balance} ₽.</b>",
                    parse_mode=ParseMode.HTML
                )
                
            else:
                old_balance = db.get_balance_from_user_bot(data["popup_bot"], popup_user_id)
                new_balance = old_balance + float(popup_sum)
                db.update_balance_from_user_bot(data["popup_bot"], popup_user_id, new_balance)            
            
            
            await bot.send_message(
                chat_id=chat_id, 
                text=f"<b>Баланс пользователя @{db.get_username(popup_user_id)} пополнен на {popup_sum} ₽. Теперь баланс пользователя составляет {new_balance} ₽.</b>",
                parse_mode=ParseMode.HTML
            )
            
            db.update_state(chat_id, states.main_state)
        else:
            await bot.send_message(
                chat_id=chat_id, 
                text=f"<b>Сумма пополнения должна быть больше 0. Попробуйте еще раз.</b>",
                parse_mode=ParseMode.HTML
            )
    except:
        await bot.send_message(
            chat_id=chat_id,
            text=f"<b>Сумма пополнения должна быть числом. Попробуйте еще раз.</b>",
            parse_mode=ParseMode.HTML
        )
