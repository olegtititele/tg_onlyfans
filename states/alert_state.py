from aiogram import Dispatcher, types
from config.states import States
from create_bot import bot
from keyboards.keyboards import *
from telegram import ParseMode


async def message_handler(message: types.Message, chat_id):
    db = DB()
    states = States()
    
    users = db.get_all_users()
    success, error, total = 0, 0, 0

    try:
        file_id = message.photo[-1].file_id
        caption = message.caption
        for i in users:
            total+=1
            try:
                await bot.send_photo(i[0], file_id, caption=caption)
                success+=1
            except:
                error+=1
        
        await bot.send_message(message.chat.id, f'<b>Всего рассылок:</b> <code>{total}</code>\n\n<b>✓ Успешно:</b> <code>{success}</code>\n<b>× Неудачно:</b> <code>{error}</code>', parse_mode=ParseMode.HTML)
    except:
        text = message.text
        for i in users:
            total+=1
            try:
                await bot.send_message(i[0], text)
                success+=1
            except:
                error+=1
        await bot.send_message(message.chat.id, f'<b>Всего рассылок:</b> <code>{total}</code>\n\n<b>✓ Успешно:</b> <code>{success}</code>\n<b>× Неудачно:</b> <code>{error}</code>', parse_mode=ParseMode.HTML)
        
        db.update_state(chat_id, states.main_state)
