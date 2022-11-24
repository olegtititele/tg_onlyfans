import asyncio
import binascii
import os
from datetime import datetime

from aiogram import Dispatcher, types
from create_bot import bot
from keyboards.keyboards import *
from telegram import ParseMode


async def message_handler(message: types.Message, chat_id):
    db = DB()
    kb = Keyboards()
    current_bot = db.get_current_bot(chat_id)
    
    try:
        if message.content_type == "photo":
            file_id = message.photo[-1].file_id
            filename = generate_random_id(db.get_all_filenames(message.content_type))
                
            file = await bot.get_file(file_id)
            file_bytes = (await bot.download_file(file.file_path)).read()
            file_option = open(f'materials/photos/{filename}.jpg', 'wb')
            file_option.write(file_bytes)
        
            db.add_material(filename, message.content_type, current_bot)
            
            await bot.send_message(
                chat_id=chat_id, 
                text=f"<b>✅ Фото успешно загружено.</b>",
                parse_mode=ParseMode.HTML
            )
        
            await bot.send_photo(
                chat_id=cf.unverified_material_chat_id,
                photo=file_id,
                caption=f'<b>Пользователь:</b> @{db.get_username(chat_id)}\n<b>Бот:</b> @{current_bot}\n<b>Дата:</b> {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}',
                reply_markup=kb.delete_photo_kb(filename),
                parse_mode=ParseMode.HTML
            )                        
            
        elif message.content_type == "video":
            file_id = message.video.file_id
            filename = generate_random_id(db.get_all_filenames(message.content_type))
                
            file = await bot.get_file(file_id)
            file_bytes = (await bot.download_file(file.file_path)).read()
            file_option = open(f'materials/videos/{filename}.mp4', 'wb')
            file_option.write(file_bytes)
        
            db.add_material(filename, message.content_type, current_bot)

            await bot.send_message(
                chat_id=chat_id, 
                text=f"<b>✅ Видео успешно загружено.</b>",
                parse_mode=ParseMode.HTML
            )
            
            
            await bot.send_video(
                chat_id=cf.unverified_material_chat_id,
                video=file_id,
                caption=f'<b>Пользователь:</b> @{db.get_username(chat_id)}\n<b>Бот:</b> @{current_bot}\n<b>Дата:</b> {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}',
                reply_markup=kb.delete_video_kb(filename),
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



def generate_random_id(material_list):
    while True:
        id = binascii.b2a_hex(os.urandom(25)).decode()
        
        if id not in material_list:
            return id
