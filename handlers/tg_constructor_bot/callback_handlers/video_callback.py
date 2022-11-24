import os
from io import BytesIO

import config.config as cf
from aiogram import types
from aiogram.types import InputFile
from create_bot import bot
from db.db import DB
from keyboards.keyboards import *
from telegram import ParseMode


async def video_callback(call, chat_id, message_id):
    db = DB()
    kb = Keyboards()
    
    if call.data == "next_video":
        current_bot = db.get_current_bot(chat_id)
        videos = db.get_bot_videos(current_bot)
        
        if cf.current_material + 1 < len(videos):
            cf.current_material += 1
            
            video = videos[cf.current_material][0]
            media = types.InputMediaVideo(media=InputFile(f"materials/videos/{video}.mp4"))
            
            data = db.get_storage(chat_id)
            data["video"] = video
            db.update_storage(chat_id, data)
            
            await bot.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=media,
                reply_markup=kb.show_videos_kb(cf.current_material + 1, len(videos))
            )
            
        return
            
    if call.data == "previous_video":
        current_bot = db.get_current_bot(chat_id)
        videos = db.get_bot_videos(current_bot)
        
        if cf.current_material + 1 > 1:
            cf.current_material -= 1
            
            video = videos[cf.current_material][0]
            media = types.InputMediaVideo(media=InputFile(f"materials/videos/{video}.mp4"))
            
            data = db.get_storage(chat_id)
            data["video"] = video
            db.update_storage(chat_id, data)
            
            await bot.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=media,
                reply_markup=kb.show_videos_kb(cf.current_material + 1, len(videos))
            )
            
        return
            
    if call.data == "delete_video":
        current_bot = db.get_current_bot(chat_id)
        data = db.get_storage(chat_id)
        filename = data["video"]
        db.delete_video(filename)
        os.remove(f"materials/videos/{filename}.mp4")
        
        videos = db.get_bot_videos(current_bot)
        
        if len(videos) > 0:
            if cf.current_material + 1 > 1:
                cf.current_material -= 1
                
                video = videos[cf.current_material][0]
                media = types.InputMediaVideo(media=InputFile(f"materials/videos/{video}.mp4"))
                
                data = db.get_storage(chat_id)
                data["video"] = video
                db.update_storage(chat_id, data)
                
                await bot.edit_message_media(
                    chat_id=chat_id,
                    message_id=message_id,
                    media=media,
                    reply_markup=kb.show_videos_kb(cf.current_material + 1, len(videos))
                )
            else:
                cf.current_material = 0
                
                video = videos[cf.current_material][0]
                media = types.InputMediaVideo(media=InputFile(f"materials/videos/{video}.mp4"))
                
                data = db.get_storage(chat_id)
                data["video"] = video
                db.update_storage(chat_id, data)
                
                await bot.edit_message_media(
                    chat_id=chat_id,
                    message_id=message_id,
                    media=media,
                    reply_markup=kb.show_videos_kb(cf.current_material + 1, len(videos))
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
