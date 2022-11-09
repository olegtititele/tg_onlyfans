from io import BytesIO

import config.config as cf
from aiogram import Dispatcher, types
from aiogram.types import InputFile, InputMedia
from config.states import States
from create_bot import bot
from db.db import DB
from keyboards.keyboards import *
from telegram import ParseMode


async def callback_handler(call: types.CallbackQuery):
    db = DB()
    kb = Keyboards()
    states = States()
    
    chat_id = call.from_user.id
    message_id = call.message.message_id

    try:
        for user_bot in db.get_all_users_bots():
            if user_bot[0] in call.data:
                db.update_current_bot(chat_id, user_bot[0])
                created_date = db.get_user_bot_created_time(user_bot[0])
                images = len(db.get_user_bot_photos(user_bot[0]))
                photo_price = db.get_user_bot_photo_price(user_bot[0])
                videos = len(db.get_user_bot_videos(user_bot[0]))
                video_price = db.get_user_bot_video_price(user_bot[0])
                created_by_username = db.get_user_bot_created_by_username(user_bot[0])
                
                caption = f"<b><u>Информация о боте</u></b>\n\n<b>🤖 Username бота:</b> @{user_bot[0]}\n\n<b>👔 Админ:</b> @{created_by_username}\n\n<b>⌚️ Дата создания бота:</b> <code>{created_date}</code>\n\n<b>🖼 Фото:</b> <code>{images}</code>\n<b>💲 Стоимость фото:</b> <code>{photo_price} ₽</code>\n\n<b>🖼 Видео:</b> <code>{videos}</code>\n<b>💲 Стоимость видео:</b> <code>{video_price} ₽</code>"
                
                if "admin|" in call.data:
                    await bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=caption,
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.back_to_all_bots_list_kb()
                    )
                else:
                    await bot.edit_message_caption(
                        chat_id=chat_id,
                        message_id=message_id,
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.bot_info_kb()
                    )
                    
        for withdrawal_request in db.get_withdrawal_requests():
            if str(withdrawal_request[0]) == str(call.data):
                if withdrawal_request[4] == "incomplete":
                    status = "⚪️"
                else:
                    status = "🟢"
                    
                text = f"<b><u>Заявка на вывод №{withdrawal_request[0]}</u></b>\n\n<b>Статус:</b> {status}\n\n<b>Пользователь:</b> @{db.get_username(withdrawal_request[1])}\n<b>Сумма:</b> <code>{round(withdrawal_request[2], 2)} ₽</code>\n<b>Тип кошелька:</b> <code>{withdrawal_request[5]}</code>\n<b>Номер кошелька:</b> <code>{withdrawal_request[6]}</code>\n\n<b>Дата:</b> <code>{parse(withdrawal_request[3]).strftime('%d.%m.%Y %H:%M:%S')}</code>" 
                
                
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=kb.back_to_withdrawal_requests_list_kb()
                )
                    
        if call.data == "statistic":
            total_income = db.get_total_income(chat_id)
            monthly_income = db.get_monthly_income(chat_id)
            weekly_income = db.get_weekly_income(chat_id)
            daily_income = db.get_daily_income(chat_id)
            
            total_subscriptions = db.get_total_subscriptions(chat_id)
            monthly_subscriptions = db.get_monthly_subscriptions(chat_id)
            weekly_subscriptions = db.get_weekly_subscriptions(chat_id)
            daily_subscriptions = db.get_daily_subscriptions(chat_id)
            
            total_images = db.get_total_bots_images(chat_id)
            total_videos = db.get_total_bots_videos(chat_id)
            
            
            text = f"<b><u>Статистика по всем ботам</u></b>\n\n<b>Заработано всего:</b> <code>{total_income} ₽</code>\n<b>💵 За месяц:</b> <code>{monthly_income} ₽</code>\n<b>💵 За неделю:</b> <code>{weekly_income} ₽</code>\n<b>💵 За сутки:</b> <code>{daily_income} ₽</code>\n\n<b>Пользователей всего:</b> <code>{total_subscriptions}</code>\n<b>👤 За месяц:</b> <code>{monthly_subscriptions}</code>\n<b>👤 За неделю:</b> <code>{weekly_subscriptions}</code>\n<b>👤 За сутки:</b> <code>{daily_subscriptions}</code>\n\n<b>🖼 Фото:</b> <code>{total_images}</code>\n<b>🖼 Видео:</b> <code>{total_videos}</code>"
            
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                parse_mode=ParseMode.HTML,
                reply_markup=kb.back_to_profile_kb()
            )
        
        elif call.data == "withdrawal":
            if db.get_balance(chat_id) < 20:
                await bot.answer_callback_query(
                    callback_query_id=call.id,
                    text="Баланс для вывода должен быть больше 20 ₽."
                )
            else:
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=f"<b>🏦 Выберите кошелёк для вывода средств:</b>\n\n<b>💯 Процент комиссии составляет</b> <code>{db.get_commission_percentage()}%</code>",
                    parse_mode=ParseMode.HTML,
                    reply_markup=kb.withdrawal_kb()
                )
            
        elif call.data == "QIWI_withdrawal":
            data = db.get_storage(chat_id)
            data["wallet_type"] = "🥝 QIWI"
            db.update_storage(chat_id, data)
            db.update_state(chat_id, states.input_card_number)
            
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="<b>📞 Введите номер вашего кошелька:</b>",
                parse_mode=ParseMode.HTML
            )
            
        elif call.data == "YOOMONEY_withdrawal":
            data = db.get_storage(chat_id)
            data["wallet_type"] = "👛 YOOMONEY"
            db.update_storage(chat_id, data)
            db.update_state(chat_id, states.input_card_number)
            
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="<b>📞 Введите номер вашего кошелька:</b>",
                parse_mode=ParseMode.HTML
            )
        
        elif "confrim_withdrawal" in call.data:
            id = call.data.split("confrim_withdrawal-")[1]
            db.update_withdrawal_request_status(id)
            
            await bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=message_id,
                reply_markup=kb.confrimed_withdrawal_kb()
            )
            
            await bot.send_message(
                chat_id=db.get_withdrawal_request(id)[1],
                text="<b>✅ Вывод средств прошёл успешно.</b>",
                parse_mode=ParseMode.HTML
            )
            
            
        # image
        elif call.data == "show_all_images":
            current_bot = db.get_current_bot(chat_id)
            images = db.get_user_bot_photos(current_bot)
            
            if len(images) < 1:
                return await bot.answer_callback_query(
                    callback_query_id=call.id,
                    text="В боте нет ни одного фото!",
                    show_alert=False
                )
                
            cf.current_material = 0
            media = types.InputMediaPhoto(BytesIO(images[cf.current_material][0]))
            db.update_current_material(chat_id, images[cf.current_material][0])
            
            return await bot.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=media,
                reply_markup=kb.show_images_kb(cf.current_material + 1, len(images))
            )
            
        elif call.data == "next_image":
            current_bot = db.get_current_bot(chat_id)
            images = db.get_user_bot_photos(current_bot)
            
            if cf.current_material + 1 < len(images):
                cf.current_material += 1
                media = types.InputMediaPhoto(BytesIO(images[cf.current_material][0]))
                db.update_current_material(chat_id, images[cf.current_material][0])
                
                return await bot.edit_message_media(
                    chat_id=chat_id,
                    message_id=message_id,
                    media=media,
                    reply_markup=kb.show_images_kb(cf.current_material + 1, len(images))
                )
                
        elif call.data == "previous_image":
            current_bot = db.get_current_bot(chat_id)
            images = db.get_user_bot_photos(current_bot)
            
            if cf.current_material + 1 > 1:
                cf.current_material -= 1
                media = types.InputMediaPhoto(BytesIO(images[cf.current_material][0]))
                db.update_current_material(chat_id, images[cf.current_material][0])
                
                return await bot.edit_message_media(
                    chat_id=chat_id,
                    message_id=message_id,
                    media=media,
                    reply_markup=kb.show_images_kb(cf.current_material + 1, len(images))
                )
                
        elif call.data == "delete_image":
            current_bot = db.get_current_bot(chat_id)
            current_image = db.get_current_material(chat_id)
            db.delete_photo(current_bot, current_image)
            
            images = db.get_user_bot_photos(current_bot)
            
            if len(images) > 0:
                if cf.current_material + 1 > 1:
                    cf.current_material -= 1
                    media = types.InputMediaPhoto(BytesIO(images[cf.current_material][0]))
                    db.update_current_material(chat_id, images[cf.current_material][0])
                    
                    return await bot.edit_message_media(
                        chat_id=chat_id,
                        message_id=message_id,
                        media=media,
                        reply_markup=kb.show_images_kb(cf.current_material + 1, len(images))
                    )
                else:
                    cf.current_material = 0
                    
                    media = types.InputMediaPhoto(BytesIO(images[cf.current_material][0]))
                    db.update_current_material(chat_id, images[cf.current_material][0])
                    
                    return await bot.edit_message_media(
                        chat_id=chat_id,
                        message_id=message_id,
                        media=media,
                        reply_markup=kb.show_images_kb(cf.current_material + 1, len(images))
                    )
            else:
                created_date = db.get_user_bot_created_time(current_bot)
                images = len(db.get_user_bot_photos(current_bot))
                photo_price = db.get_user_bot_photo_price(current_bot)
                videos = len(db.get_user_bot_videos(current_bot))
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
            
        
        # video
        elif call.data == "show_all_videos":
            current_bot = db.get_current_bot(chat_id)
            videos = db.get_user_bot_videos(current_bot)
            
            if len(videos) < 1:
                return await bot.answer_callback_query(
                    callback_query_id=call.id,
                    text="В боте нет ни одного видео!",
                    show_alert=False
                )
                
            cf.current_material = 0
            media = types.InputMediaVideo(BytesIO(videos[cf.current_material][0]))
            db.update_current_material(chat_id, videos[cf.current_material][0])
                
            return await bot.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=media,
                reply_markup=kb.show_videos_kb(cf.current_material + 1, len(videos))
            )
            
        elif call.data == "next_video":
            current_bot = db.get_current_bot(chat_id)
            videos = db.get_user_bot_videos(current_bot)
            
            if cf.current_material + 1 < len(videos):
                cf.current_material += 1
                media = types.InputMediaVideo(BytesIO(videos[cf.current_material][0]))
                db.update_current_material(chat_id, videos[cf.current_material][0])
                
                return await bot.edit_message_media(
                    chat_id=chat_id,
                    message_id=message_id,
                    media=media,
                    reply_markup=kb.show_videos_kb(cf.current_material + 1, len(videos))
                )
                
        elif call.data == "previous_video":
            current_bot = db.get_current_bot(chat_id)
            videos = db.get_user_bot_videos(current_bot)
            
            if cf.current_material + 1 > 1:
                cf.current_material -= 1
                media = types.InputMediaVideo(BytesIO(videos[cf.current_material][0]))
                db.update_current_material(chat_id, videos[cf.current_material][0])
                
                return await bot.edit_message_media(
                    chat_id=chat_id,
                    message_id=message_id,
                    media=media,
                    reply_markup=kb.show_videos_kb(cf.current_material + 1, len(videos))
                )
                
        elif call.data == "delete_video":
            current_bot = db.get_current_bot(chat_id)
            current_video = db.get_current_material(chat_id)
            db.delete_video(current_bot, current_video)
            
            videos = db.get_user_bot_videos(current_bot)
            
            if len(videos) > 0:
                if cf.current_material + 1 > 1:
                    cf.current_material -= 1
                    media = types.InputMediaVideo(BytesIO(videos[cf.current_material][0]))
                    db.update_current_material(chat_id, videos[cf.current_material][0])
                    
                    return await bot.edit_message_media(
                        chat_id=chat_id,
                        message_id=message_id,
                        media=media,
                        reply_markup=kb.show_videos_kb(cf.current_material + 1, len(videos))
                    )
                else:
                    cf.current_material = 0
                    
                    media = types.InputMediaVideo(BytesIO(videos[cf.current_material][0]))
                    db.update_current_material(chat_id, videos[cf.current_material][0])
                    
                    return await bot.edit_message_media(
                        chat_id=chat_id,
                        message_id=message_id,
                        media=media,
                        reply_markup=kb.show_videos_kb(cf.current_material + 1, len(videos))
                    )
            else:
                created_date = db.get_user_bot_created_time(current_bot)
                images = len(db.get_user_bot_photos(current_bot))
                photo_price = db.get_user_bot_photo_price(current_bot)
                videos = len(db.get_user_bot_videos(current_bot))
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
            
            
        elif call.data == "add_new_bot":
            db.update_state(chat_id, states.new_bot_state)

            await bot.edit_message_caption(
                chat_id=chat_id,
                message_id=message_id,
                caption="<b>⤵️ Введите токен нового бота:</b>",
                parse_mode=ParseMode.HTML,
                reply_markup=kb.back_to_user_bots_list_kb()
            )
            
            
        elif call.data == "edit_photo_price":
            db.update_state(chat_id, states.photo_price_state)

            await bot.edit_message_caption(
                chat_id=chat_id,
                message_id=message_id,
                caption="<b>⤵️ Введите цену за фото:</b>",
                parse_mode=ParseMode.HTML,
                reply_markup=kb.back_to_user_bot_info_kb()
            )
            
        elif call.data == "edit_video_price":
            db.update_state(chat_id, states.video_price_state)

            await bot.edit_message_caption(
                chat_id=chat_id,
                message_id=message_id,
                caption="<b>⤵️ Введите цену за видео:</b>",
                parse_mode=ParseMode.HTML,
                reply_markup=kb.back_to_user_bot_info_kb()
            )
            
        elif call.data == "upload_material":
            db.update_state(chat_id, states.upload_material)

            await bot.edit_message_caption(
                chat_id=chat_id,
                message_id=message_id,
                caption="<b>⤵️ Отправьте боту материал для загрузки в бота:</b>",
                parse_mode=ParseMode.HTML,
                reply_markup=kb.back_to_user_bot_info_kb()
            )
            
        elif call.data == "delete_bot":
            current_bot = db.get_current_bot(chat_id)
            
            db.delete_user_bot(current_bot)
            
            for photo in db.get_user_bot_photos(current_bot):
                db.delete_photo(current_bot, photo[0])
                
            for video in db.get_user_bot_videos(current_bot):
                db.delete_video(current_bot, video[0])
                
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
            
            
            
        elif call.data == "popup_in_this_bot":
            data = db.get_storage(chat_id)
            data["popup_in_bot"] = call.data
            db.update_storage(chat_id, data)
            
            db.update_state(chat_id, states.find_user)

            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="<b>Введите ID или @username пользователя:</b>",
                parse_mode=ParseMode.HTML
            )
            
        elif call.data == "popup_in_another_bot":
            data = db.get_storage(chat_id)
            data["popup_in_bot"] = call.data
            db.update_storage(chat_id, data)
            
            db.update_state(chat_id, states.find_bot)

            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="<b>Введите @usernamebot бота:</b>",
                parse_mode=ParseMode.HTML
            )
            
        elif call.data == "previous_withdrawal_requests_list":  
            await previous_page(chat_id, message_id, kb.withdrawal_requests_kb(cf.page-1))
            
        elif call.data == "next_withdrawal_requests_list":
            await next_page(chat_id, message_id, kb.withdrawal_requests_kb(cf.page+1))
        
        elif call.data == "previous_bots_list":  
            await previous_page(chat_id, message_id, kb.all_bots_kb(cf.page-1))
            
        elif call.data == "next_bots_list":
            await next_page(chat_id, message_id, kb.all_bots_kb(cf.page+1))
            
        elif call.data == "previous_user_bots_list":  
            await previous_page(chat_id, message_id, kb.user_bots_kb(chat_id, cf.page-1))
            
        elif call.data == "next_user_bots_list":
            await next_page(chat_id, message_id, kb.user_bots_kb(chat_id, cf.page+1))
            
            
        elif call.data == "back_to_user_bots_list":
            cf.page = 1
            db.update_state(chat_id, states.main_state)
            
            await bot.edit_message_caption(
                chat_id=chat_id,
                message_id=message_id,
                caption=f"<b><u>Мои боты</u></b>\n\n<b>🤖 Всего ботов:</b> <code>{len(db.get_user_bots(chat_id))}</code>",
                parse_mode=ParseMode.HTML,
                reply_markup=kb.user_bots_kb(chat_id, cf.page)[0]
            )

        elif call.data == "back_to_user_bot_info":
            db.update_state(chat_id, states.main_state)
            
            current_bot = db.get_current_bot(chat_id)
            created_date = db.get_user_bot_created_time(current_bot)
            images = len(db.get_user_bot_photos(current_bot))
            photo_price = db.get_user_bot_photo_price(current_bot)
            videos = len(db.get_user_bot_videos(current_bot))
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
            
        elif call.data == "back_to_profile":

            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"<b><u>Профиль</u></b>\n\n<b>👤 Профиль:</b> @{call.from_user.username}\n\n<b>💳 Баланс:</b> <code>{db.get_balance(chat_id)} ₽</code>",
                parse_mode=ParseMode.HTML,
                reply_markup=kb.profile_kb()
            )
        
        elif call.data == "back_to_all_bots_list":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="<b><u>Список всех ботов</u></b>",
                parse_mode=ParseMode.HTML,
                reply_markup=kb.all_bots_kb(cf.page)[0]
            )
        
        elif call.data == "back_to_withdrawal_requests_list":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="<b><u>Заявки на вывод</u></b>",
                parse_mode=ParseMode.HTML,
                reply_markup=kb.withdrawal_requests_kb(cf.page)[0]
            )
    except:
        await bot.answer_callback_query(
            callback_query_id=call.id,
            text="Произошла неизвестная ошибка!",
            show_alert=True
        )
                
async def next_page(chat_id, message_id, kb_info: tuple):
    scroll_kb_info = kb_info

    scroll_kb = scroll_kb_info[0]
    pages = scroll_kb_info[1]

    if cf.page >= pages:
        return
    else:
        cf.page += 1

    await bot.edit_message_reply_markup(
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=scroll_kb
    )
    
async def previous_page(chat_id, message_id, kb_info: tuple):
    scroll_kb_info = kb_info

    scroll_kb = scroll_kb_info[0]
    pages = scroll_kb_info[1]

    if cf.page <= 1:
        return
    else:
        cf.page -= 1

    await bot.edit_message_reply_markup(
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=scroll_kb
    )
    
    
def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(callback_handler)
