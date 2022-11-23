from aiogram import Dispatcher, types
from aiogram.types import InputFile
from config.states import States
from create_bot import bot
from keyboards.keyboards import *
from telegram import ParseMode
import random

async def message_handler(message: types.Message, chat_id):
    db = DB()
    kb = Keyboards()
    states = States()

    withdrawal_amount = message.text.replace(',', '.')
    try:
        if float(withdrawal_amount) > 20 and float(withdrawal_amount) <= db.get_balance(chat_id):
            if db.get_subscription_time(chat_id) > 0:
                commission_percentage = 3
            else:  
                commission_percentage = db.get_commission_percentage()
                
            new_withdrawal_amount = float(withdrawal_amount) - (float(withdrawal_amount) * (float(commission_percentage)/100))
            data = db.get_storage(chat_id)
            wallet_type = data["wallet_type"]
            card_number = data["card_number"]
            
            withdrawal_id = generate_withdrawal_id()
            db.add_new_withdrawal_request(withdrawal_id, chat_id, float(new_withdrawal_amount), wallet_type, card_number)
            
            await bot.send_message(
                chat_id=chat_id, 
                text=f"<b>✅ Вывод успешно зарегистрирован\n\n💸 Вам придут {round(new_withdrawal_amount, 2)} ₽. Комиссия {round(float(withdrawal_amount) * (float(commission_percentage)/100), 2)} ₽.</b>",
                parse_mode=ParseMode.HTML
            )
            
            await bot.send_message(
                chat_id=cf.logs_chat_id, 
                text=f"<b><u>💳 Новая заявка на вывод</u></b>\n\n<b>Пользователь:</b> @{db.get_username(chat_id)}\n<b>Кошелек:</b> <code>{wallet_type}</code>\n<b>Номер кошелька:</b> <code>{card_number}</code>\n<b>Сумма:</b> <code>{round(new_withdrawal_amount, 2)} ₽</code>",
                parse_mode=ParseMode.HTML,
                reply_markup=kb.confrim_withdrawal_kb(withdrawal_id)
            )
            
            invited_by_id = db.get_invited_by(chat_id)
            if not invited_by_id is None:
                old_balance = db.get_balance(invited_by_id)
                referal_bonus = float(withdrawal_amount) * (float(commission_percentage)/100) * float(db.get_referal_bonus() / 100)
                new_balance = old_balance + referal_bonus
                db.update_balance(invited_by_id, new_balance)
                
                await bot.send_message(
                    chat_id=invited_by_id, 
                    text=f"<b>🎁 Вы получили {referal_bonus} ₽ c реферала.</b>",
                    parse_mode=ParseMode.HTML
                )
                
            old_balance = db.get_balance(chat_id)
            new_balance = old_balance - float(withdrawal_amount)
            
            db.update_balance(chat_id, new_balance)
            db.update_state(chat_id, states.main_state)
        else:
            await bot.send_message(
                chat_id=chat_id, 
                text=f"<b>Сумма вывода должна быть больше 20 и меньше {round(withdrawal_amount)}. Введите еще раз.</b>",
                parse_mode=ParseMode.HTML
            )
    except:
        await bot.send_message(
            chat_id=chat_id, 
            text=f"<b>Сумма вывода должна быть числом. Введите еще раз.</b>",
            parse_mode=ParseMode.HTML
        )


def generate_withdrawal_id():
    db = DB()
    while True:
        withdrawal_id = random.randint(1000000, 9999999)
        if withdrawal_id in [w_id[0] for w_id in db.get_withdrawal_requests()]:
            generate_withdrawal_id()
        
        return withdrawal_id