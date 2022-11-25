import os
from io import BytesIO

import config.config as cf
from aiogram import types
from aiogram.types import InputFile
from config.bot_texts import *
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
            media = types.InputMediaPhoto(media=InputFile("background.jpg"))
                
            await bot.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=media,
            )
            
            await bot.edit_message_caption(
                chat_id=chat_id,
                message_id=message_id,
                caption=bot_info_text(current_bot),
                parse_mode=ParseMode.HTML,
                reply_markup=kb.bot_info_kb(chat_id)
            )
            
        return
