from aiogram import types
from config.states import States
from create_bot import bot
from keyboards.keyboards import *
from telegram import ParseMode
from handlers.tg_user_bot import methods as user_bot

async def message_handler(message: types.Message, chat_id):
    db = DB()
    states = States()
    current_bot = db.get_current_bot(chat_id)
    bot_token = db.get_bot_token(current_bot)
    users = db.get_users_from_bot(current_bot)
    success, error, total = 0, 0, 0

    try:
        file_id = message.photo[-1].file_id
        file = await bot.get_file(file_id)
        file_bytes = (await bot.download_file(file.file_path)).read()
        
        caption = message.caption
        if caption is None:
            caption = ""
            
        for i in users:
            total+=1
            try:
                await user_bot.send_photo(
                    token=bot_token,
                    chat_id=str(i[0]),
                    photo=file_bytes,
                    caption=caption
                )
                success+=1
            except:
                error+=1
        
        await bot.send_message(chat_id, f'<b>Всего рассылок:</b> <code>{total}</code>\n\n<b>✓ Успешно:</b> <code>{success}</code>\n<b>× Неудачно:</b> <code>{error}</code>', parse_mode=ParseMode.HTML)
    except:
        text = message.text
        for i in users:
            total+=1
            try:
                await user_bot.send_message(
                    token=bot_token,
                    chat_id=str(i[0]),
                    text=text
                )
                success+=1
            except:
                error+=1
        await bot.send_message(chat_id, f'<b>Всего рассылок:</b> <code>{total}</code>\n\n<b>✓ Успешно:</b> <code>{success}</code>\n<b>× Неудачно:</b> <code>{error}</code>', parse_mode=ParseMode.HTML)
        
        db.update_state(chat_id, states.main_state)
