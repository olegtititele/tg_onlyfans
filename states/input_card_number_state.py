from aiogram import Dispatcher, types
from config.states import States
from create_bot import bot
from keyboards.keyboards import *
from telegram import ParseMode


async def message_handler(message: types.Message, chat_id):
    db = DB()
    states = States()
    card_number = message.text
    
    data = db.get_storage(chat_id)
    data["card_number"] = card_number
    db.update_storage(chat_id, data)

    db.update_state(chat_id, states.input_withdrawal_amount)
    
    await bot.send_message(
        chat_id=chat_id, 
        text=f"<b>💸 Введите сумму вывода до {db.get_balance(chat_id)} ₽.</b>",
        parse_mode=ParseMode.HTML
    )