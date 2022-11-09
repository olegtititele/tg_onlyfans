import asyncio

from aiogram import Dispatcher, types
from create_bot import bot
from keyboards.keyboards import *
from telegram import ParseMode


async def message_handler(message: types.Message, chat_id):
    db = DB()
    current_bot = db.get_current_bot(chat_id)
    
    try:
        if message.content_type == "photo":
            file_id = message.photo[-1].file_id
            photo_file = await bot.get_file(file_id)
            photo_bytes = await bot.download_file(photo_file.file_path)
        
            db.add_photo(photo_bytes.read(), current_bot)
            
            await bot.send_message(
                chat_id=chat_id, 
                text=f"<b>✅ Фото успешно загружено.</b>",
                parse_mode=ParseMode.HTML
            )
            
        elif message.content_type == "video":
            file_id = message.video.file_id
            video_file = await bot.get_file(file_id)
            video_bytes = await bot.download_file(video_file.file_path)
            
            db.add_video(video_bytes.read(), current_bot)

            await bot.send_message(
                chat_id=chat_id, 
                text=f"<b>✅ Видео успешно загружено.</b>",
                parse_mode=ParseMode.HTML
            )
                
        else:
            pass
    except:
        if message.content_type == "photo":
            await bot.send_message(
                chat_id=chat_id, 
                text=f"<b>❌ Фото не загружено.</b>",
                parse_mode=ParseMode.HTML
            )
            
        elif message.content_type == "video":
            await bot.send_message(
                chat_id=chat_id, 
                text=f"<b>❌ Видео не загружено.</b>",
                parse_mode=ParseMode.HTML
            )
            
        else:
            pass
        
    await asyncio.sleep(1)
