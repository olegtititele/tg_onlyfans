import asyncio
import binascii
import json
import os
import uuid
from datetime import datetime, timedelta

import aiohttp
from db.db import DB
from payments.QIWI import Qiwi
from payments.YOOMONEY import YooMoney

menu_keyboard = { "keyboard": [["🖼 Видео", "🖼 Фото"], ["💼 Профиль"], ["💵 Пополнить баланс"]], "resize_keyboard": True}


async def get_updates(token, offset=0):
    async with aiohttp.ClientSession() as session:
        URL = 'https://api.telegram.org/bot'
        async with session.get(f'{URL}{token}/getUpdates?offset={offset}') as resp:
            result = await resp.json()
            return result['result']
        
async def check_updates(token, update):
    if "message" in update:
        await check_message(token, update)
    elif "callback_query":
        await check_callback(token, update)
    else:
        pass

async def send_message(token, chat_id, text, reply_markup):
    data = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup), 'parse_mode': 'HTML'}
    
    async with aiohttp.ClientSession() as session:
        URL = 'https://api.telegram.org/bot'
        async with session.get(f'{URL}{token}/sendMessage', data=data) as resp:
            await resp.json()
            
            
async def send_photo(token, data):
    async with aiohttp.ClientSession() as session:
        URL = 'https://api.telegram.org/bot'
        async with session.post(f'{URL}{token}/sendPhoto', data=data) as resp:
            await resp.json()
            
async def send_video(token, data):
    async with aiohttp.ClientSession() as session:
        URL = 'https://api.telegram.org/bot'
        async with session.post(f'{URL}{token}/sendVideo', data=data) as resp:
            await resp.json()
           
           
async def get_me(token):
    async with aiohttp.ClientSession() as session:
        URL = 'https://api.telegram.org/bot'
        async with session.get(f'{URL}{token}/getMe') as resp:
            return await resp.json()


async def check_callback(token, callback):
    db = DB()
    chat_id = callback['callback_query']['from']['id']
    call_data = callback['callback_query']['data']
    bot_username = (await get_me(token))['result']['username']
    
    
    if call_data == "qiwi":
        db.update_state_from_user_bot(bot_username, chat_id, "popup_balance_qiwi")
        
        return await send_message(
            token=token,
            chat_id=chat_id,
            text=f"<b>Введите сумму пополнения:</b>",
            reply_markup=menu_keyboard
        )
    
    elif call_data == "yoomoney":
        db.update_state_from_user_bot(bot_username, chat_id, "popup_balance_yoomoney")

        return await send_message(
            token=token,
            chat_id=chat_id,
            text=f"<b>Введите сумму пополнения:</b>",
            reply_markup=menu_keyboard
        )
    


async def check_message(token, message):
    db = DB()
    chat_id = message['message']['from']['id']
    message_text = message['message']['text']
    bot_username = (await get_me(token))['result']['username']
    
    if "/start" in message_text:
        db.update_state_from_user_bot(bot_username, chat_id, "main_state")
        
        if not db.check_if_user_exists_in_user_bot(bot_username, chat_id):
            try:
                args = message_text.split(" ")[1]
            
                if args.isdigit():
                    invited_by = args
                    referal_sum = db.get_start_referal_sum_in_user_bot()
                    referal_balance = db.get_referal_balance_from_user_bot(bot_username, invited_by)
                    new_balance = referal_balance + referal_sum
                    db.update_referal_balance_from_user_bot(bot_username, invited_by, new_balance)
                    
                    try:
                        await send_message(
                            token=token,
                            chat_id=invited_by,
                            text=f"<b>➕ У вас новый реферал! Вы получили {referal_sum} ₽ на реферальный баланс.</b>",
                            reply_markup=menu_keyboard
                        )
                    except:
                        pass
                    
                else:
                    invited_by = None
            except:
                invited_by = None
            
            db.add_new_user_in_user_bot(bot_username, chat_id, message['message']['from']['username'], invited_by)
            
            
            try:
                await send_message(
                    token=token,
                    chat_id=db.get_user_bot_created_by_id(bot_username),
                    text=f"<b>👤 Зарегистрирован новый пользователь:</b> @{message['message']['from']['username']}",
                    reply_markup=menu_keyboard
                )
            except:
                pass
            
        balance = db.get_balance_from_user_bot(bot_username, chat_id)
        referal_balance = db.get_referal_balance_from_user_bot(bot_username, chat_id)
        invited_users = db.get_invited_users_from_user_bot(bot_username, chat_id)
        photo_price = db.get_user_bot_photo_price(bot_username)
        video_price = db.get_user_bot_video_price(bot_username)
        admin = db.get_user_bot_created_by_username(bot_username)
        admin_id = db.get_user_bot_created_by_id(bot_username)
        
        if db.get_subscription_time(admin_id) > 0:
            return await send_message(
                token=token,
                chat_id=chat_id,
                text=f"<b>Привет, {message['message']['from']['first_name']}</b>\n\n<b>👤 Ваш ID:</b> <code>{chat_id}</code>\n\n<b>💵 Баланс:</b> <code>{balance} ₽</code>\n\n<b>💸 Реф. баланс:</b> <code>{referal_balance} ₽</code>\n\n<b>👤 Приглашено:</b> <code>{invited_users}</code>\nt.me/{bot_username}?start={chat_id}\n\n<b>🖼 Стоимость фото:</b> <code>{photo_price} ₽</code>\n\n<b>🖼 Стоимость видео:</b> <code>{video_price} ₽</code>\n\n<b>Администратор:</b> @{admin}",
                reply_markup=menu_keyboard
            )
        
        return await send_message(
            token=token,
            chat_id=chat_id,
            text=f"<b>Привет, {message['message']['from']['first_name']}</b>\n\n<b>👤 Ваш ID:</b> <code>{chat_id}</code>\n\n<b>💵 Баланс:</b> <code>{balance} ₽</code>\n\n<b>💸 Реф. баланс:</b> <code>{referal_balance} ₽</code>\n\n<b>👤 Приглашено:</b> <code>{invited_users}</code>\nt.me/{bot_username}?start={chat_id}\n\n<b>🖼 Стоимость фото:</b> <code>{photo_price} ₽</code>\n\n<b>🖼 Стоимость видео:</b> <code>{video_price} ₽</code>\n\n<b>Администратор:</b> @{admin}\n\n<b>⚙️ Бот сделан в @FansBuyBot</b>",
            reply_markup=menu_keyboard
        )
        
    elif message_text == "💼 Профиль":
        db.update_state_from_user_bot(bot_username, chat_id, "main_state")
        
        balance = db.get_balance_from_user_bot(bot_username, chat_id)
        referal_balance = db.get_referal_balance_from_user_bot(bot_username, chat_id)
        invited_users = db.get_invited_users_from_user_bot(bot_username, chat_id)
        photo_price = db.get_user_bot_photo_price(bot_username)
        video_price = db.get_user_bot_video_price(bot_username)
        admin = db.get_user_bot_created_by_username(bot_username) 
        admin_id = db.get_user_bot_created_by_id(bot_username)
        
        if db.get_subscription_time(admin_id) > 0:
            return await send_message(
                token=token,
                chat_id=chat_id,
                text=f"<b><u>Профиль</u></b>\n\n<b>👤 Ваш ID:</b> <code>{chat_id}</code>\n\n<b>💵 Баланс:</b> <code>{balance} ₽</code>\n\n<b>💸 Реф. баланс:</b> <code>{referal_balance} ₽</code>\n\n<b>👤 Приглашено:</b> <code>{invited_users}</code>\nt.me/{bot_username}?start={chat_id}\n\n<b>🖼 Стоимость фото:</b> <code>{photo_price} ₽</code>\n\n<b>🖼 Стоимость видео:</b> <code>{video_price} ₽</code>\n\n<b>Администратор:</b> @{admin}",
                reply_markup=menu_keyboard
            )
            
        return await send_message(
            token=token,
            chat_id=chat_id,
            text=f"<b><u>Профиль</u></b>\n\n<b>👤 Ваш ID:</b> <code>{chat_id}</code>\n\n<b>💵 Баланс:</b> <code>{balance} ₽</code>\n\n<b>💸 Реф. баланс:</b> <code>{referal_balance} ₽</code>\n\n<b>👤 Приглашено:</b> <code>{invited_users}</code>\nt.me/{bot_username}?start={chat_id}\n\n<b>🖼 Стоимость фото:</b> <code>{photo_price} ₽</code>\n\n<b>🖼 Стоимость видео:</b> <code>{video_price} ₽</code>\n\n<b>Администратор:</b> @{admin}\n\n<b>⚙️ Бот сделан в @FansBuyBot</b>",
            reply_markup=menu_keyboard
        )
        
    elif message_text == "🖼 Фото":
        
        bot_photos = db.get_bot_photos(bot_username)
        balance = db.get_balance_from_user_bot(bot_username, chat_id)
        referal_balance = db.get_referal_balance_from_user_bot(bot_username, chat_id)
        photo_price = db.get_user_bot_photo_price(bot_username)
        admin_id = db.get_user_bot_created_by_id(bot_username)
        
        if len(bot_photos) == 0:
            return await send_message(
                token=token,
                chat_id=chat_id,
                text=f"<b>В данном боте еще нет приватных фото! Ждите пополнения.</b>",
                reply_markup=menu_keyboard
            )
            
        else:
            if str(admin_id) == str(chat_id):
                return await send_message(
                    token=token,
                    chat_id=chat_id,
                    text=f"<b>Вы можете просмотреть фото в основном боте).</b>",
                    reply_markup=menu_keyboard
                )
                
            else:
                if referal_balance >= photo_price:
                    for photo in bot_photos:
                        viewed_users = db.get_viewed_users_on_photo(photo[0])
                        if str(chat_id) not in viewed_users:
                            
                            # Списать у пользователя
                            new_balance = referal_balance - photo_price
                            db.update_referal_balance_from_user_bot(bot_username, chat_id, new_balance)
                            
                            viewed_users.append(str(chat_id))
                            db.update_viewed_users_on_photo(photo[0], viewed_users)
                            
                            data = {'chat_id': str(chat_id), 'photo': open(f'materials/photos/{photo[0]}.jpg', 'rb')}
                            
                            return await send_photo(token, data)
                else:        
                    if balance < photo_price:
                        return await send_message(
                            token=token,
                            chat_id=chat_id,
                            text=f"<b>У вас недостаточно средств для покупки фото. Пополните баланс.</b>",
                            reply_markup=menu_keyboard
                        )
                        
                    else:
                        for photo in bot_photos:
                            viewed_users = db.get_viewed_users_on_photo(photo[0])
                            if str(chat_id) not in viewed_users:
                                
                                # Списать у пользователя
                                new_balance = balance - photo_price
                                db.update_balance_from_user_bot(bot_username, chat_id, new_balance)
                                
                                # Пополнить у админа
                                old_admin_balance = db.get_balance(admin_id)
                                new_admin_balance = old_admin_balance + photo_price
                                db.update_balance(admin_id, new_admin_balance)
                                
                                # Добавить транзакцию
                                db.add_new_transaction(chat_id, bot_username, photo_price)
                                
                                
                                
                                viewed_users.append(str(chat_id))
                                db.update_viewed_users_on_photo(photo[0], viewed_users)
                                
                                data = {'chat_id': str(chat_id), 'photo': open(f'materials/photos/{photo[0]}.jpg', 'rb')}
                                
                                return await send_photo(token, data)
                
                
                return await send_message(
                    token=token,
                    chat_id=chat_id,
                    text=f"<b>Вы просмотрели все приватные фото в этом боте! Ждите пополнения.</b>",
                    reply_markup=menu_keyboard
                )
        
    elif message_text == "🖼 Видео":
        db.update_state_from_user_bot(bot_username, chat_id, "main_state")
        
        bot_videos = db.get_bot_videos(bot_username)
        balance = db.get_balance_from_user_bot(bot_username, chat_id)
        referal_balance = db.get_referal_balance_from_user_bot(bot_username, chat_id)
        video_price = db.get_user_bot_video_price(bot_username)
        admin_id = db.get_user_bot_created_by_id(bot_username)

        
        if len(bot_videos) == 0:
            return await send_message(
                token=token,
                chat_id=chat_id,
                text=f"<b>В данном боте еще нет приватных видео! Ждите пополнения.</b>",
                reply_markup=menu_keyboard
            )
            
        else:
            if str(admin_id) == str(chat_id):
                return await send_message(
                    token=token,
                    chat_id=chat_id,
                    text=f"<b>Вы можете просмотреть видео в основном боте).</b>",
                    reply_markup=menu_keyboard
                )
                
            else:
                if referal_balance >= video_price:
                    for video in bot_videos:
                        viewed_users = db.get_viewed_users_on_video(video[0])
                        if str(chat_id) not in viewed_users:
                            
                            # Списать у пользователя
                            new_balance = referal_balance - video_price
                            db.update_referal_balance_from_user_bot(bot_username, chat_id, new_balance)
                            
                            viewed_users.append(str(chat_id))
                            db.update_viewed_users_on_video(video[0], viewed_users)
                            
                            data = {'chat_id': str(chat_id), 'video':  open(f'materials/videos/{video[0]}.mp4', 'rb')}
                            
                            return await send_video(token, data)
                else:
                    if balance < video_price:
                        return await send_message(
                            token=token,
                            chat_id=chat_id,
                            text=f"<b>У вас недостаточно средств для покупки видео. Пополните баланс.</b>",
                            reply_markup=menu_keyboard
                        )
                        
                    else:
                        for video in bot_videos:
                            viewed_users = db.get_viewed_users_on_video(video[0])
                            if str(chat_id) not in viewed_users:
                                # Списать у пользователя
                                new_balance = balance - video_price
                                db.update_balance_from_user_bot(bot_username, chat_id, new_balance)
                                
                                # Пополнить у админа
                                old_admin_balance = db.get_balance(admin_id)
                                new_admin_balance = old_admin_balance + video_price
                                db.update_balance(admin_id, new_admin_balance)
                                
                                # Добавить транзакцию
                                db.add_new_transaction(chat_id, bot_username, video_price)
                                
                                
                                viewed_users.append(str(chat_id))
                                db.update_viewed_users_on_video(video[0], viewed_users)
                                
                                data = {'chat_id': str(chat_id), 'video': open(f'materials/videos/{video[0]}.mp4', 'rb')}
                                
                                return await send_video(token, data)
                
                
                return await send_message(
                    token=token,
                    chat_id=chat_id,
                    text=f"<b>Вы просмотрели все приватные видео в этом боте! Ждите пополнения.</b>",
                    reply_markup=menu_keyboard
                )
    
    elif message_text == "💵 Пополнить баланс":
        db.update_state_from_user_bot(bot_username, chat_id, "main_state")
        
        keyboard = {
            "inline_keyboard": [[
                {
                    "text": '🥝 QIWI',
                    "callback_data": "qiwi"
                },
                {
                    "text": '👛 YOOMONEY',
                    "callback_data": "yoomoney"
                }
            ]]
        }
        
        return await send_message(
            token=token,
            chat_id=chat_id,
            text=f"<b>Выберите способ оплаты:</b>",
            reply_markup=keyboard
        )
    
    else:
        state = db.get_state_from_user_bot(bot_username, chat_id)
        
        if state == "popup_balance_qiwi":
            try:
                if float(message_text.replace(',', '.')) > 5:
                    qiwi = Qiwi()
                    bill_id = binascii.b2a_hex(os.urandom(15))
                    
                    await qiwi.make_bill(bill_id, message_text, f"@{bot_username}")
                    pay_url = await qiwi.get_pay_url(bill_id)
                    
                    keyboard = {
                        "inline_keyboard": [[
                            {
                                "text": 'Оплатить',
                                "url": f"{pay_url}"
                            }
                        ]]
                    }
                    
                    db.update_state_from_user_bot(bot_username, chat_id, "main_state")
                    
                    asyncio.create_task(check_qiwi_popup(token, chat_id, message['message']['from']['username'], bot_username, bill_id))
                    
                    return await send_message(
                        token=token,
                        chat_id=chat_id,
                        text=f"<b>Оплатите счет в течении 30 минут. Средства на баланс зачислятся автоматически.</b>",
                        reply_markup=keyboard
                    )
                    
                else:
                    return await send_message(
                        token=token,
                        chat_id=chat_id,
                        text=f"<b>Сумма пополнения должна быть больше 5. Попробуйте еще раз.</b>",
                        reply_markup=menu_keyboard
                    )

            except:
                return await send_message(
                    token=token,
                    chat_id=chat_id,
                    text=f"<b>Сумма пополнения должна быть числом. Попробуйте еще раз.</b>",
                    reply_markup=menu_keyboard
                )
            
        elif state == "popup_balance_yoomoney":
            try:
                if float(message_text.replace(',', '.')) > 1:
                    yoomoney = YooMoney()
                    bill_id = generate_random_label()

                    pay_url = yoomoney.make_bill(bill_id, message_text, f"@{bot_username}")
                    
                    keyboard = {
                        "inline_keyboard": [[
                            {
                                "text": 'Оплатить',
                                "url": f"{pay_url}"
                            }
                        ]]
                    }
                    
                    db.update_state_from_user_bot(bot_username, chat_id, "main_state")
                    
                    asyncio.create_task(check_yoomoney_popup(token, chat_id, message['message']['from']['username'], bot_username, bill_id, message_text.replace(',', '.')))
                    
                    
                    return await send_message(
                        token=token,
                        chat_id=chat_id,
                        text=f"<b>Оплатите счет в течении 30 минут. Средства на баланс зачислятся автоматически.</b>",
                        reply_markup=keyboard
                    )
                    
                else:
                    return await send_message(
                        token=token,
                        chat_id=chat_id,
                        text=f"<b>Сумма пополнения должна быть больше 5. Попробуйте еще раз.</b>",
                        reply_markup=menu_keyboard
                    )
            except:
                return await send_message(
                    token=token,
                    chat_id=chat_id,
                    text=f"<b>Сумма пополнения должна быть числом. Попробуйте еще раз.</b>",
                    reply_markup=menu_keyboard
                )
        
            

async def check_qiwi_popup(token, chat_id, username, bot_username, bill_id):
    qiwi = Qiwi()
    
    while True:
        payment_status = await qiwi.check_payment(bill_id)
        
        if payment_status.lower() == "paid":
            db = DB()
            referal_id = db.get_invited_by_from_user_bot(bot_username, chat_id)
            payment_amount = float(await qiwi.get_payment_amount(bill_id))
            old_balance = db.get_balance_from_user_bot(bot_username, chat_id)
            new_balance = old_balance + payment_amount
            db.update_balance_from_user_bot(bot_username, chat_id, new_balance)
            db.add_new_replenishment(chat_id, payment_amount)
            
            
            try:   
                await send_message(
                    token=token,
                    chat_id=db.get_user_bot_created_by_id(bot_username),
                    text=f"<b>💲 Пользователь @{username} пополнил баланс на {payment_amount} ₽.</b>",
                    reply_markup=menu_keyboard
                )
            except:
                pass
            
            if not referal_id is None:
                old_balance = db.get_balance_from_user_bot(bot_username, referal_id)
                referal_bonus = payment_amount * float(db.get_referal_bonus_in_user_bot()/100)
                new_balance = old_balance + referal_bonus
                db.update_balance_from_user_bot(bot_username, referal_id, new_balance)

                await send_message(
                    token=token,
                    chat_id=referal_id,
                    text=f"<b>💲 Вознаграждение с реферала\n\nНа ваш баланс зачислено {referal_bonus} ₽.</b>",
                    reply_markup=menu_keyboard
                )
            
            return await send_message(
                token=token,
                chat_id=chat_id,
                text=f"<b>💲 На ваш баланс зачислено {payment_amount} ₽.</b>",
                reply_markup=menu_keyboard
            )
        elif payment_status.lower() == "expired":
            return await send_message(
                token=token,
                chat_id=chat_id,
                text=f"<b>⛔️ Время платежа истекло. Платеж отменен.</b>",
                reply_markup=menu_keyboard
            )
        else:
            await asyncio.sleep(10)
    
    
async def check_yoomoney_popup(token, chat_id, username, bot_username, bill_id, popup_sum):
    start_time = datetime.now()
    yoomoney =  YooMoney()
    while True:
        payment_status = yoomoney.operation_info(bill_id)
        if payment_status == "success":
            db = DB()
            referal_id = db.get_invited_by_from_user_bot(bot_username, chat_id)
            payment_amount = float(popup_sum)
            old_balance = db.get_balance_from_user_bot(bot_username, chat_id)
            new_balance = old_balance + payment_amount
            db.update_balance_from_user_bot(bot_username, chat_id, new_balance)
            db.add_new_replenishment(chat_id, payment_amount)
            
            try:
                await send_message(
                    token=token,
                    chat_id=db.get_user_bot_created_by_id(bot_username),
                    text=f"<b>💲 Пользователь @{username} пополнил баланс на {payment_amount} ₽.</b>",
                    reply_markup=menu_keyboard
                )
            except:
                pass
            
            
            if not referal_id is None:
                old_balance = db.get_balance_from_user_bot(bot_username, referal_id)
                referal_bonus = payment_amount * float(db.get_referal_bonus_in_user_bot()/100)
                new_balance = old_balance + referal_bonus
                db.update_balance_from_user_bot(bot_username, referal_id, new_balance)

                await send_message(
                    token=token,
                    chat_id=referal_id,
                    text=f"<b>💲 Вознаграждение с реферала\n\nНа ваш баланс зачислено {referal_bonus} ₽.</b>",
                    reply_markup=menu_keyboard
                )
            
            
            return await send_message(
                token=token,
                chat_id=chat_id,
                text=f"<b>💲 На ваш баланс зачислено {payment_amount} ₽.</b>",
                reply_markup=menu_keyboard
            )
        else:
            if datetime.now() >= start_time + timedelta(minutes=30):
                return await send_message(
                    token=token,
                    chat_id=chat_id,
                    text=f"<b>⛔️ Время платежа истекло. Платеж отменен.</b>",
                    reply_markup=menu_keyboard
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
    

async def run(token):
    try:
        update_id = (await get_updates(token))[-1]['update_id']
    except:
        update_id = 0
        
    try:
        bot_username = (await get_me(token))['result']['username']
    except KeyError:
        return
    
    while True:
        try:
            if DB().get_user_bot(bot_username) is None:
                return
            
            updates = await get_updates(token, update_id)
            for update in updates:
                if update_id < update['update_id']:
                    update_id = update['update_id']
                    await check_updates(token, update)
                    
            
            await asyncio.sleep(1)
        except:
            await asyncio.sleep(10)
