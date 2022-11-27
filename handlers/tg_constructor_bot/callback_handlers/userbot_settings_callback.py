import os

import config.config as cf
from aiogram import types
from aiogram.types import InputFile
from config.bot_texts import *
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
        images = db.get_bot_photos(current_bot)
        
        if len(images) < 1:
            return await bot.answer_callback_query(
                callback_query_id=call.id,
                text="В боте нет ни одного фото!",
                show_alert=False
            )
            
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
        
        return
        
    if call.data == "show_all_videos":
        current_bot = db.get_current_bot(chat_id)
        videos = db.get_bot_videos(current_bot)
        
        if len(videos) < 1:
            return await bot.answer_callback_query(
                callback_query_id=call.id,
                text="В боте нет ни одного видео!",
                show_alert=False
            )
        
        cf.current_material = 0
        video = videos[cf.current_material][0]
        media = types.InputMediaVideo(media=InputFile(f"materials/videos/{video}.mp4"))
        
        
        db.update_current_material(chat_id, video)
        
        await bot.edit_message_media(
            chat_id=chat_id,
            message_id=message_id,
            media=media,
            reply_markup=kb.show_videos_kb(cf.current_material + 1, len(videos))
        )
        
        return
    
    if call.data == "user_alert":
        db.update_state(chat_id, states.user_bot_alert)

        return await bot.edit_message_caption(
            chat_id=chat_id,
            message_id=message_id,
            caption="<b>Отправьте текст/фото с текстом для рассылки:</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=kb.back_to_user_bot_info_kb()
        )
        
    if call.data == "channel_subscription_id":
        db.update_state(chat_id, states.channel_subscription_id)
        link = f'<a href="https://telegra.ph/Kak-sdelat-obyazatelnuyu-podpisku-na-kanal-11-27">Инструкция</a>'
        
        return await bot.edit_message_caption(
            chat_id=chat_id,
            message_id=message_id,
            caption=f"<b>{link}\nЕсли вы хотите отключить эту функцию, нажмите на кнопку \"Отключить\".\n\n⤵️ Введите ID канала:</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=kb.subscription_channel_id_kb()
        )
    
    if call.data == "channel_subscription_link":
        db.update_state(chat_id, states.channel_subscription_link)
        
        return await bot.edit_message_caption(
            chat_id=chat_id,
            message_id=message_id,
            caption=f"<b>⤵️ Введите ссылку или @username канала/группы в который пользователю нужно будет присоединиться:</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=kb.back_to_user_bot_info_kb()
        )
    
    if call.data == "off_channel_id":
        current_bot = db.get_current_bot(chat_id)
        db.update_state(chat_id, states.main_state)
        db.update_bot_subscription_channel_id(current_bot, None)
        
        await bot.answer_callback_query(
            callback_query_id=call.id,
            text="Функция отключена!"
        )
        
        return await bot.edit_message_caption(
            chat_id=chat_id,
            message_id=message_id,
            caption=bot_info_text(chat_id, current_bot),
            parse_mode=ParseMode.HTML,
            reply_markup=kb.bot_info_kb(chat_id)
        )
        
    if call.data == "invite_referal_amount":
        db.update_state(chat_id, states.invite_referal_amount)

        return await bot.edit_message_caption(
            chat_id=chat_id,
            message_id=message_id,
            caption="<b>⤵️ Введите сумму реферала, которую будет получать пользователь за приглашенного человека:</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=kb.back_to_user_bot_info_kb()
        )
    
    if call.data == "start_balance_amount":
        db.update_state(chat_id, states.start_balance_amount)

        return await bot.edit_message_caption(
            chat_id=chat_id,
            message_id=message_id,
            caption="<b>⤵️ Введите сумму стартового баланса пользователя:</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=kb.back_to_user_bot_info_kb()
        )
    
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
        
        for photo in db.get_bot_photos(current_bot):
            db.delete_photo(photo[0])
            os.remove(f"materials/photos/{photo[0]}.jpg")
            
        for video in db.get_bot_videos(current_bot):
            db.delete_video(video[0])
            os.remove(f"materials/videos/{video[0]}.mp4")
            
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
    
