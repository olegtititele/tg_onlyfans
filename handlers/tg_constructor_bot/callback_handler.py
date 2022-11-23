import asyncio
import uuid
from datetime import datetime, timedelta

from aiogram import Dispatcher, types
from config.states import States
from create_bot import bot
from db.db import DB
from keyboards.keyboards import *
from payments.QIWI import Qiwi
from payments.YOOMONEY import YooMoney
from telegram import ParseMode

from .bot_callback_data import *
from .callback_handlers.admin_callback import admin_callback
from .callback_handlers.back_buttons_callback import back_buttons_callback
from .callback_handlers.image_callback import image_callback
from .callback_handlers.scroll_buttons_callback import scroll_buttons_callback
from .callback_handlers.userbot_settings_callback import \
    userbot_settings_callback
from .callback_handlers.video_callback import video_callback


async def callback_handler(call: types.CallbackQuery):
    db = DB()
    kb = Keyboards()
    states = States()
    chat_id = call.from_user.id
    message_id = call.message.message_id
    
    try:
        if call.data in userbot_settings_callback_data:
            return await userbot_settings_callback(call, chat_id, message_id)
        elif call.data in image_buttons_callback_data:
            return await image_callback(call, chat_id, message_id)
        elif call.data in video_buttons_callback_data:
            return await video_callback(call, chat_id, message_id)
        elif call.data in scroll_buttons_callback_data:
            return await scroll_buttons_callback(call, chat_id, message_id)
        elif call.data in admin_callback_data:
            return await admin_callback(call, chat_id, message_id)
        elif call.data in back_buttons_callback_data:
            return await back_buttons_callback(call, chat_id, message_id)
        else:
            if "del_img-" in call.data:
                material_id = call.data.split("del_img-")[1]
                bot_username = db.get_photo_info(material_id)
                photo_user_id = db.get_user_bot_created_by_id(bot_username)
                db.delete_photo(material_id)
                
                try:
                    await bot.send_message(
                        chat_id=photo_user_id, 
                        text=f"<b>❌ Фото удалено. Нарушает правила проекта.</b>",
                        parse_mode=ParseMode.HTML
                    )
                except:
                    pass
                
                
                try:
                    await bot.delete_message(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id
                    )
                except:
                    pass
                
                return
            
            if "del_vid-" in call.data:
                material_id = call.data.split("del_vid-")[1]
                bot_username = db.get_video_info(material_id)
                video_user_id = db.get_user_bot_created_by_id(bot_username)
                db.delete_video(material_id)
                
                try:
                    await bot.send_message(
                        chat_id=video_user_id, 
                        text=f"<b>❌ Видео удалено. Нарушает правила проекта.</b>",
                        parse_mode=ParseMode.HTML
                    )
                except:
                    pass
                
                
                try:
                    await bot.delete_message(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id
                    )
                except:
                    pass
                
                return
                
            if call.data == "one_month_price":
                data = db.get_storage(chat_id)
                data["popup_sum"] = cf.price_for_one_month
                data["premium_duration"] = 1
                db.update_storage(chat_id, data)
                
                
                return await bot.edit_message_caption(
                    chat_id=chat_id,
                    message_id=message_id,
                    caption="<b><u>💎 1 месяц</u>\n\nВыберите способ оплаты:</b>",
                    parse_mode=ParseMode.HTML,
                    reply_markup=kb.payment_methods_kb()
                )
                
            if call.data == "three_month_price":
                data = db.get_storage(chat_id)
                data["popup_sum"] = cf.price_for_three_month
                data["premium_duration"] = 3
                db.update_storage(chat_id, data)
                
                
                return await bot.edit_message_caption(
                    chat_id=chat_id,
                    message_id=message_id,
                    caption="<b><u>💎 3 месяца</u>\n\nВыберите способ оплаты:</b>",
                    parse_mode=ParseMode.HTML,
                    reply_markup=kb.payment_methods_kb()
                )
                
            if call.data == "six_month_price":
                data = db.get_storage(chat_id)
                data["popup_sum"] = cf.price_for_six_month
                data["premium_duration"] = 6
                db.update_storage(chat_id, data)
                
                
                return await bot.edit_message_caption(
                    chat_id=chat_id,
                    message_id=message_id,
                    caption="<b><u>💎 6 месяцев</u>\n\nВыберите способ оплаты:</b>",
                    parse_mode=ParseMode.HTML,
                    reply_markup=kb.payment_methods_kb()
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
                
                return
            
            if call.data == "withdrawal":
                if db.get_balance(chat_id) < 20:
                    await bot.answer_callback_query(
                        callback_query_id=call.id,
                        text="Баланс для вывода должен быть больше 20 ₽."
                    )
                else:
                    if db.get_subscription_time(chat_id) > 0:
                        proc = 3
                    else:
                        proc = db.get_commission_percentage()
                    await bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=f"<b>🏦 Выберите кошелёк для вывода средств:</b>\n\n<b>💯 Процент комиссии составляет</b> <code>{proc}%</code>",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.withdrawal_kb()
                    )
                
                return
                
            if call.data == "QIWI_withdrawal":
                data = db.get_storage(chat_id)
                data["wallet_type"] = "🥝 QIWI"
                db.update_storage(chat_id, data)
                db.update_state(chat_id, states.input_card_number)
                
                return await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text="<b>📞 Введите номер вашего кошелька:</b>",
                    parse_mode=ParseMode.HTML
                )
                
            if call.data == "YOOMONEY_withdrawal":
                data = db.get_storage(chat_id)
                data["wallet_type"] = "👛 YOOMONEY"
                db.update_storage(chat_id, data)
                db.update_state(chat_id, states.input_card_number)
                
                return await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text="<b>📞 Введите номер вашего кошелька:</b>",
                    parse_mode=ParseMode.HTML
                )
            
            if call.data == "popup_qiwi":
                qiwi = Qiwi()
                bill_id = uuid.uuid4().hex
                data = db.get_storage(chat_id)
                popup_sum = data["popup_sum"]
                premium_duration = int(data["premium_duration"])
                
                await qiwi.make_bill(bill_id, popup_sum, f"@{(await bot.get_me()).username}")
                pay_url = await qiwi.get_pay_url(bill_id)
                
                asyncio.create_task(check_qiwi_popup(chat_id, bill_id, premium_duration))
                
                return await bot.edit_message_caption(
                    chat_id=chat_id,
                    message_id=message_id,
                    caption=f"<b>Оплатите счет в течении 30 минут. Средства на баланс зачислятся автоматически.</b>",
                    parse_mode=ParseMode.HTML,
                    reply_markup=kb.pay_kb(pay_url)
                )
            
            if call.data == "popup_yoomoney":
                yoomoney = YooMoney()
                bill_id = generate_random_label()
                data = db.get_storage(chat_id)
                popup_sum = data["popup_sum"]
                premium_duration = int(data["premium_duration"])

                pay_url = yoomoney.make_bill(bill_id, popup_sum, f"@{(await bot.get_me()).username}")
                
                asyncio.create_task(check_yoomoney_popup(chat_id, bill_id, float(popup_sum), premium_duration))
                
                return await bot.edit_message_caption(
                    chat_id=chat_id,
                    message_id=message_id,
                    caption=f"<b>Оплатите счет в течении 30 минут. Средства на баланс зачислятся автоматически.</b>",
                    parse_mode=ParseMode.HTML,
                    reply_markup=kb.pay_kb(pay_url)
                )
                
            if call.data == "popup_from_balance":
                balance = db.get_balance(chat_id)
                data = db.get_storage(chat_id)
                popup_sum = float(data["popup_sum"])
                premium_duration = int(data["premium_duration"])
                
                if balance < popup_sum:
                    return await bot.answer_callback_query(
                        callback_query_id=call.id,
                        text="На вашем балансе недостаточно средств!"
                    )
                
                new_balance = balance - popup_sum
                db.update_balance(chat_id, new_balance)
                db.update_subscription_time(chat_id, premium_duration)
                
                return await bot.edit_message_caption(
                    chat_id=chat_id,
                    message_id=message_id,
                    caption=f"<b>💎Премимум подписка успешно оплачена.</b>",
                    parse_mode=ParseMode.HTML
                )
                
            if "confrim_withdrawal-" in call.data:
                id = call.data.split("confrim_withdrawal-")[1]
                if db.get_withdrawal_request_status(id) == "incomplete":
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
                else:
                    await bot.edit_message_reply_markup(
                        chat_id=call.message.chat.id,
                        message_id=message_id,
                        reply_markup=kb.confrimed_withdrawal_kb()
                    )
                
                return
            
            if "c_w_adm-" in call.data:
                id = call.data.split("c_w_adm-")[1]
                withdrawal_request = db.get_withdrawal_request(id)
                
                if db.get_withdrawal_request_status(id) == "incomplete":
                    db.update_withdrawal_request_status(id)

                    await bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text = f"<b><u>Заявка на вывод №{withdrawal_request[0]}</u></b>\n\n<b>Статус:</b> 🟢\n\n<b>Пользователь:</b> @{db.get_username(withdrawal_request[1])}\n<b>Сумма:</b> <code>{round(withdrawal_request[2], 2)} ₽</code>\n<b>Тип кошелька:</b> <code>{withdrawal_request[5]}</code>\n<b>Номер кошелька:</b> <code>{withdrawal_request[6]}</code>\n\n<b>Дата:</b> <code>{parse(withdrawal_request[3]).strftime('%d.%m.%Y %H:%M:%S')}</code>" ,
                        reply_markup=kb.back_to_withdrawal_requests_list_kb(id),
                        parse_mode=ParseMode.HTML
                    )
                    
                    await bot.send_message(
                        chat_id=withdrawal_request[1],
                        text="<b>✅ Вывод средств прошёл успешно.</b>",
                        parse_mode=ParseMode.HTML
                    )
                    
                else:
                    await bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text = f"<b><u>Заявка на вывод №{withdrawal_request[0]}</u></b>\n\n<b>Статус:</b> 🟢\n\n<b>Пользователь:</b> @{db.get_username(withdrawal_request[1])}\n<b>Сумма:</b> <code>{round(withdrawal_request[2], 2)} ₽</code>\n<b>Тип кошелька:</b> <code>{withdrawal_request[5]}</code>\n<b>Номер кошелька:</b> <code>{withdrawal_request[6]}</code>\n\n<b>Дата:</b> <code>{parse(withdrawal_request[3]).strftime('%d.%m.%Y %H:%M:%S')}</code>" ,
                        reply_markup=kb.back_to_withdrawal_requests_list_kb(id),
                        parse_mode=ParseMode.HTML
                    )
                
                return
                    
            if call.data == "add_new_bot":
                db.update_state(chat_id, states.new_bot_state)

                return await bot.edit_message_caption(
                    chat_id=chat_id,
                    message_id=message_id,
                    caption="<b>Получите токен бота в @BotFather\n\n⤵️ Введите токен нового бота:</b>",
                    parse_mode=ParseMode.HTML,
                    reply_markup=kb.back_to_user_bots_list_kb()
                )
                
                
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
                    return
                        
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
                        reply_markup=kb.back_to_withdrawal_requests_list_kb(withdrawal_request[0])
                    )
                    return
                
    except:
        await bot.answer_callback_query(
            callback_query_id=call.id,
            text="Произошла неизвестная ошибка!",
            show_alert=True
        )
        
        
async def check_qiwi_popup(chat_id, bill_id, premium_duration):
    qiwi = Qiwi()
    kb = Keyboards()
    
    while True:
        payment_status = await qiwi.check_payment(bill_id)
        
        if payment_status.lower() == "paid":
            db = DB()
            payment_amount = float(await qiwi.get_payment_amount(bill_id))
            db.add_new_replenishment(chat_id, payment_amount)
            
            for admin_id in cf.admins_chat_id:
                try:
                    await bot.send_message(
                        chat_id=admin_id, 
                        text=f"<b>💎 Пользователь @{db.get_username(chat_id)} приобрел подписку на {premium_duration} м.</b>",
                        parse_mode=ParseMode.HTML
                    )
                except:
                    continue

            db.update_subscription_time(chat_id, premium_duration)
                
            return await bot.send_message(
                chat_id=chat_id,
                text=f"<b>💎 Премимум подписка успешно оплачена.</b>",
                parse_mode=ParseMode.HTML
            )
        elif payment_status.lower() == "expired":
            
            return await bot.send_message(
                chat_id=chat_id,
                text=f"<b>⛔️ Время платежа истекло. Платеж отменен.</b>",
                reply_markup=kb.menu_button_kb()
            )
        else:
            await asyncio.sleep(10)


async def check_yoomoney_popup(chat_id, bill_id, payment_amount, premium_duration):
    start_time = datetime.now()
    yoomoney =  YooMoney()
    kb = Keyboards()
    
    while True:
        payment_status = yoomoney.operation_info(bill_id)
        if payment_status == "success":
            db = DB()
            db.add_new_replenishment(chat_id, payment_amount)
            
            for admin_id in cf.admins_chat_id:
                try:
                    await bot.send_message(
                        chat_id=admin_id, 
                        text=f"<b>💎 Пользователь @{db.get_username(chat_id)} приобрел подписку на {premium_duration} м.</b>",
                        parse_mode=ParseMode.HTML
                    )
                except:
                    continue

            db.update_subscription_time(chat_id, premium_duration)
                
            return await bot.send_message(
                chat_id=chat_id,
                text=f"<b>💎 Премимум подписка успешно оплачена.</b>",
                parse_mode=ParseMode.HTML
            )
        else:
            if datetime.now() >= start_time + timedelta(minutes=30):
                return await bot.send_message(
                    chat_id=chat_id,
                    text=f"<b>⛔️ Время платежа истекло. Платеж отменен.</b>",
                    reply_markup=kb.menu_button_kb()
                )
            else:
                await asyncio.sleep(10)


def generate_random_label():
    while True:
        db = DB()
        label = uuid.uuid4().hex
        
        if label not in db.get_all_labels():
            db.add_label(label)
            return label
    
def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(callback_handler)
