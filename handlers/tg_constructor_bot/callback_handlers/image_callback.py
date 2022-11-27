import os

import config.config as cf
from aiogram import types
from aiogram.types import InputFile
from config.bot_texts import *
from create_bot import bot
from db.db import DB
from keyboards.keyboards import *
from telegram import ParseMode


async def image_callback(call, chat_id, message_id):
    db = DB()
    kb = Keyboards()
        
    if call.data == "next_image":
        current_bot = db.get_current_bot(chat_id)
        images = db.get_bot_photos(current_bot)
        
        if cf.current_material + 1 < len(images):
            cf.current_material += 1
            
            photo = images[cf.current_material][0]
            media = types.InputMediaPhoto(media=InputFile(f"materials/photos/{photo}.jpg"))
            
            db.update_current_material(chat_id, photo)
            
            await bot.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=media,
                reply_markup=kb.show_images_kb(cf.current_material + 1, len(images))
            )
        
        return
            
    if call.data == "previous_image":
        current_bot = db.get_current_bot(chat_id)
        images = db.get_bot_photos(current_bot)
        
        if cf.current_material + 1 > 1:
            cf.current_material -= 1
            
            photo = images[cf.current_material][0]
            media = types.InputMediaPhoto(media=InputFile(f"materials/photos/{photo}.jpg"))
            
            db.update_current_material(chat_id, photo)
            
            await bot.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=media,
                reply_markup=kb.show_images_kb(cf.current_material + 1, len(images))
            )
            
        return
            
    if call.data == "delete_image":
        current_bot = db.get_current_bot(chat_id)
        filename = db.get_current_material(chat_id)
        db.delete_photo(filename)
        os.remove(f"materials/photos/{filename}.jpg")
        
        images = db.get_bot_photos(current_bot)
        
        if len(images) > 0:
            if cf.current_material + 1 > 1:
                cf.current_material -= 1
                
                photo = images[cf.current_material][0]
                media = types.InputMediaPhoto(media=InputFile(f"materials/photos/{photo}.jpg"))
                
                
                db.update_current_material(chat_id, photo)
                
                await bot.edit_message_media(
                    chat_id=chat_id,
                    message_id=message_id,
                    media=media,
                    reply_markup=kb.show_images_kb(cf.current_material + 1, len(images))
                )
            else:
                cf.current_material = 0
                
                photo = images[cf.current_material][0]
                media = types.InputMediaPhoto(media=InputFile(f"materials/photos/{photo}.jpg"))
                
                
                db.update_current_material(chat_id, photo)
                
                await bot.edit_message_media(
                    chat_id=chat_id,
                    message_id=message_id,
                    media=media,
                    reply_markup=kb.show_images_kb(cf.current_material + 1, len(images))
                )
        else:
            media = types.InputMediaPhoto(media=InputFile("background.jpg"))
                
            await bot.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=media,
            )
            
            await bot.edit_message_caption(
                chat_id=chat_id,
                message_id=message_id,
                caption=bot_info_text(chat_id, current_bot),
                parse_mode=ParseMode.HTML,
                reply_markup=kb.bot_info_kb(chat_id)
            )
            
        return
