import os

import config.config as cf
from aiogram import types
from aiogram.types import InputFile
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
            
            data = db.get_storage(chat_id)
            data["photo"] = photo
            db.update_storage(chat_id, data)
            
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
            
            
            data = db.get_storage(chat_id)
            data["photo"] = photo
            db.update_storage(chat_id, data)
            
            await bot.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=media,
                reply_markup=kb.show_images_kb(cf.current_material + 1, len(images))
            )
            
        return
            
    if call.data == "delete_image":
        current_bot = db.get_current_bot(chat_id)
        data = db.get_storage(chat_id)
        filename = data["photo"]
        db.delete_photo(filename)
        os.remove(f"materials/photos/{filename}.jpg")
        
        images = db.get_bot_photos(current_bot)
        
        if len(images) > 0:
            if cf.current_material + 1 > 1:
                cf.current_material -= 1
                
                photo = images[cf.current_material][0]
                media = types.InputMediaPhoto(media=InputFile(f"materials/photos/{photo}.jpg"))
                
                
                data = db.get_storage(chat_id)
                data["photo"] = photo
                db.update_storage(chat_id, data)
                
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
                
                
                data = db.get_storage(chat_id)
                data["photo"] = photo
                db.update_storage(chat_id, data)
                
                await bot.edit_message_media(
                    chat_id=chat_id,
                    message_id=message_id,
                    media=media,
                    reply_markup=kb.show_images_kb(cf.current_material + 1, len(images))
                )
        else:
            created_date = db.get_user_bot_created_time(current_bot)
            images = len(db.get_bot_photos(current_bot))
            photo_price = db.get_user_bot_photo_price(current_bot)
            videos = len(db.get_bot_videos(current_bot))
            video_price = db.get_user_bot_video_price(current_bot)
            
            media = types.InputMediaPhoto(media=InputFile("background.jpg"))
                
            await bot.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=media,
            )
            
            await bot.edit_message_caption(
                chat_id=chat_id,
                message_id=message_id,
                caption=f"<b><u>Информация о боте</u></b>\n\n<b>🤖 Username:</b> @{current_bot}\n\n<b>⌚️ Дата создания бота:</b> <code>{created_date}</code>\n\n<b>🖼 Фото:</b> <code>{images}</code>\n<b>💲 Стоимость фото:</b> <code>{photo_price} ₽</code>\n\n<b>🖼 Видео:</b> <code>{videos}</code>\n<b>💲 Стоимость видео:</b> <code>{video_price} ₽</code>",
                parse_mode=ParseMode.HTML,
                reply_markup=kb.bot_info_kb()
            )
            
        return
