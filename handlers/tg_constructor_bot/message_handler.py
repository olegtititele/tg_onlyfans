import config.config as cf
from aiogram import Dispatcher, types
from aiogram.types import InputFile
from config.states import States
from create_bot import bot
from keyboards.keyboards import *
from telegram import ParseMode

import states.new_bot_state as new_bot_state
import states.upload_material_state as upload_material_state
import states.photo_price_state as photo_price_state
import states.video_price_state as video_price_state
import states.find_user_state as find_user_state
import states.find_bot_state as find_bot_state
import states.alert_state as alert_state
import states.change_balance_state as change_balance_state
import states.input_card_number_state as input_card_number_state
import states.input_withdrawal_amount_state as input_withdrawal_amount_state
import states.change_commission_percentage_state as change_commission_percentage_state
import states.change_releral_bonus_state as change_releral_bonus_state
import states.change_ref_in_user_bot_state as change_ref_in_user_bot_state
import states.start_referal_sum_state as start_referal_sum_state

async def message_handler(message: types.Message):
    db = DB()
    kb = Keyboards()
    states = States()
    chat_id = message.from_user.id
    
    current_state = db.get_state(chat_id)

    if message.text == "👤 Профиль 👤":
        db.update_state(chat_id, states.main_state)
        
        subscription_in_minutes = db.get_subscription_time(chat_id)
        
        if subscription_in_minutes >= 60:
            formatted_time = f'{int(subscription_in_minutes / 60)} ч.'
        else:
            formatted_time = f'{subscription_in_minutes} мин.'
        
        return await bot.send_message(
            chat_id=chat_id, 
            text=f"<b><u>Профиль</u></b>\n\n<b>👤 Профиль:</b> @{message.from_user.username}\n\n<b>💳 Баланс:</b> <code>{db.get_balance(chat_id)} ₽</code>\n\n<b>🔗 Кол-во приглашенных пользователей:</b> <code>{len(db.get_referals_count(chat_id))}</code>\n\n<b>💎 Премиум:</b> <code>{formatted_time}</code>",
            parse_mode=ParseMode.HTML,
            reply_markup=kb.profile_kb()
        )
    
    elif message.text == "💎 Премиум 💎":
        db.update_state(chat_id, states.main_state)
        photo = InputFile("background.jpg")
        
        
        return await bot.send_photo(
            chat_id=chat_id, 
            photo=photo,
            caption=f"<b><u>Возможности с Премиум подпиской</u></b>\n\n<b>• Комиссия:</b> <s>13%</s> <b>3%</b>\n\n<b>• Нет упоминания сервиса в вашем боте</b>\n\n<b>• Обьязательная подписка пользователя на ваш канал</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=kb.premium_price_kb()
        )

    elif message.text == "👥 Реферальная система 👥":
        db.update_state(chat_id, states.main_state)
        bot_username = (await bot.get_me()).username
        
        ref_link = f'<a href="https://t.me/{bot_username}?start={chat_id}">Ваша реферальная ссылка</a>'
        return await bot.send_message(
            chat_id=chat_id, 
            text=f"<b><u>Реферальная система</u></b>\n\n<b>🫂 Приглашайте друзей и зарабатывайте {db.get_referal_bonus()}% с комиссии!</b>\n\n<b>{ref_link}</b>",
            parse_mode=ParseMode.HTML
        )
        
        
        
    elif message.text == "🤖 Мои боты 🤖":
        cf.page = 1
        photo = InputFile("background.jpg")
        db.update_state(chat_id, states.main_state)
        
        return await bot.send_photo(
            chat_id=chat_id, 
            photo=photo,
            caption=f"<b><u>Мои боты</u></b>\n\n<b>🤖 Всего ботов:</b> <code>{len(db.get_user_bots(chat_id))}</code>",
            parse_mode=ParseMode.HTML,
            reply_markup=kb.user_bots_kb(chat_id, cf.page)[0]
        )
    
    elif message.text == "📃 Посмотреть список ботов":
        if chat_id in cf.admins_chat_id:
            cf.page = 1
            
            return await bot.send_message(
                chat_id=chat_id, 
                text="<b><u>Список всех ботов</u></b>",
                parse_mode=ParseMode.HTML,
                reply_markup=kb.all_bots_kb(cf.page)[0]
            )
            
    elif message.text == "💯 Комиссия":
        if chat_id in cf.admins_chat_id:
            db.update_state(chat_id, states.change_commission_percentage)
            
            return await bot.send_message(
                chat_id=chat_id, 
                text="<b>⤵️ Введите новый процент комиссии:</b>",
                parse_mode=ParseMode.HTML
            )
    
    elif message.text == "💯 Реферал":
        if chat_id in cf.admins_chat_id:
            db.update_state(chat_id, states.change_referal_bonus)
            
            return await bot.send_message(
                chat_id=chat_id, 
                text="<b>⤵️ Введите новый процент реферала:</b>",
                parse_mode=ParseMode.HTML
            )
            
    elif message.text == "💯 Реферал в боте пользователя":
        if chat_id in cf.admins_chat_id:
            db.update_state(chat_id, states.change_ref_in_user_bot)
            
            return await bot.send_message(
                chat_id=chat_id, 
                text="<b>⤵️ Введите новый процент реферала в боте пользователя:</b>",
                parse_mode=ParseMode.HTML
            )
        
    elif message.text == "💯 Реферал при старте":
        if chat_id in cf.admins_chat_id:
            db.update_state(chat_id, states.start_referal_sum)
            
            return await bot.send_message(
                chat_id=chat_id, 
                text="<b>⤵️ Введите новый реферал при старте в боте пользователя:</b>",
                parse_mode=ParseMode.HTML
            )
    
    elif message.text == "✉️ Рассылка":
        if chat_id in cf.admins_chat_id:
            db.update_state(chat_id, states.alert)
            
            return await bot.send_message(
                chat_id=chat_id, 
                text="<b>Отправьте текст/фото с текстом для рассылки:</b>",
                parse_mode=ParseMode.HTML
            )
        
    elif message.text == "💰 Зачислить баланс":
        if chat_id in cf.admins_chat_id:
            db.update_state(chat_id, states.main_state)
            
            return await bot.send_message(
                chat_id=chat_id, 
                text="<b>В каком боте вы хотите пополнить баланс пользователя?</b>",
                parse_mode=ParseMode.HTML,
                reply_markup=kb.choose_bot_for_popup_kb()
            )
            
    elif message.text == "🏦 Заявки на вывод":
        if chat_id in cf.admins_chat_id:
            cf.page = 1
            db.update_state(chat_id, states.main_state)
            
            return await bot.send_message(
                chat_id=chat_id, 
                text="<b><u>Заявки на вывод</u></b>",
                parse_mode=ParseMode.HTML,
                reply_markup=kb.withdrawal_requests_kb(cf.page)[0]
            )
        
        
    
    if current_state == states.new_bot_state:
        await new_bot_state.message_handler(message, chat_id)
        
    elif current_state == states.upload_material:
        await upload_material_state.message_handler(message, chat_id)
                
    elif current_state == states.photo_price_state:
        await photo_price_state.message_handler(message, chat_id)
        
    elif current_state == states.video_price_state:
        await video_price_state.message_handler(message, chat_id)
        
    elif current_state == states.find_user:
        await find_user_state.message_handler(message, chat_id)
        
    elif current_state == states.find_bot:
        await find_bot_state.message_handler(message, chat_id)
        
    elif current_state == states.change_balance:
        await change_balance_state.message_handler(message, chat_id)
                
    elif current_state == states.alert:
        await alert_state.message_handler(message, chat_id)
             
    elif current_state == states.input_card_number:
        await input_card_number_state.message_handler(message, chat_id)
    
    elif current_state == states.input_withdrawal_amount:
        await input_withdrawal_amount_state.message_handler(message, chat_id)
    
    elif current_state == states.change_commission_percentage:
        await change_commission_percentage_state.message_handler(message, chat_id)
    
    elif current_state == states.change_referal_bonus:
        await change_releral_bonus_state.message_handler(message, chat_id)
    
    elif current_state == states.change_ref_in_user_bot:
        await change_ref_in_user_bot_state.message_handler(message, chat_id)
    elif current_state == states.start_referal_sum:
        await start_referal_sum_state.message_handler(message, chat_id)
    else:
        return
  


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(message_handler, content_types=types.ContentTypes.ANY)
