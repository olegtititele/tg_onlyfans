from io import BytesIO

import config.config as cf
from aiogram import types
from config.states import States
from create_bot import bot
from db.db import DB
from keyboards.keyboards import *
from telegram import ParseMode


async def userbot_settings_callback(call, chat_id, message_id):
    db = DB()
    kb = Keyboards()
    states = States()
    
    if call.data == "show_all_images":
        current_bot = db.get_current_bot(chat_id)
        images = db.get_user_bot_photos(current_bot)
        
        if len(images) < 1:
            return await bot.answer_callback_query(
                callback_query_id=call.id,
                text="В боте нет ни одного фото!",
                show_alert=False
            )
            
        cf.current_material = 0
        
        photo = db.get_photo(images[cf.current_material][0])
        media = types.InputMediaPhoto(BytesIO(photo))
        
        data = db.get_storage(chat_id)
        data["photo"] = images[cf.current_material][0]
        db.update_storage(chat_id, data)
        
        await bot.edit_message_media(
            chat_id=chat_id,
            message_id=message_id,
            media=media,
            reply_markup=kb.show_images_kb(cf.current_material + 1, len(images))
        )
        
        return
        
    if call.data == "show_all_videos":
        current_bot = db.get_current_bot(chat_id)
        videos = db.get_user_bot_videos(current_bot)
        
        if len(videos) < 1:
            return await bot.answer_callback_query(
                callback_query_id=call.id,
                text="В боте нет ни одного видео!",
                show_alert=False
            )
        
        cf.current_material = 0
        video = db.get_video(videos[cf.current_material][0])
        media = types.InputMediaVideo(BytesIO(video))
        
        data = db.get_storage(chat_id)
        data["video"] = videos[cf.current_material][0]
        db.update_storage(chat_id, data)
        
        await bot.edit_message_media(
            chat_id=chat_id,
            message_id=message_id,
            media=media,
            reply_markup=kb.show_videos_kb(cf.current_material + 1, len(videos))
        )
        
        return
    
    if call.data == "edit_photo_price":
        db.update_state(chat_id, states.photo_price_state)

        return await bot.edit_message_caption(
            chat_id=chat_id,
            message_id=message_id,
            caption="<b>⤵️ Введите цену за фото:</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=kb.back_to_user_bot_info_kb()
        )
        
        
    if call.data == "edit_video_price":
        db.update_state(chat_id, states.video_price_state)

        return await bot.edit_message_caption(
            chat_id=chat_id,
            message_id=message_id,
            caption="<b>⤵️ Введите цену за видео:</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=kb.back_to_user_bot_info_kb()
        )
        
        
    if call.data == "upload_material":
        db.update_state(chat_id, states.upload_material)

        return await bot.edit_message_caption(
            chat_id=chat_id,
            message_id=message_id,
            caption="<b>⤵️ Отправьте боту материал для загрузки в бота:</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=kb.back_to_user_bot_info_kb()
        )
        
        
    if call.data == "delete_bot":
        current_bot = db.get_current_bot(chat_id)
        
        db.delete_user_bot(current_bot)
        
        for photo in db.get_user_bot_photos(current_bot):
            db.delete_photo(photo[0])
            
        for video in db.get_user_bot_videos(current_bot):
            db.delete_video(video[0])
            
        await bot.answer_callback_query(
            callback_query_id=call.id,
            text=f"Бот @{current_bot} удален. Все фото и видео этого бота удалены.",
            show_alert=True
        )
        
        cf.page = 1
        
        await bot.edit_message_caption(
            chat_id=chat_id,
            message_id=message_id,
            caption=f"<b><u>Мои боты</u></b>\n\n<b>🤖 Всего ботов:</b> <code>{len(db.get_user_bots(chat_id))}</code>",
            parse_mode=ParseMode.HTML,
            reply_markup=kb.user_bots_kb(chat_id, cf.page)[0]
        )
        
        return
    
