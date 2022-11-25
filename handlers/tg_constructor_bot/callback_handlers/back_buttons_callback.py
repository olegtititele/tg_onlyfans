import config.config as cf
from aiogram import types
from aiogram.types import InputFile
from config.bot_texts import *
from config.states import States
from create_bot import bot
from db.db import DB
from keyboards.keyboards import *
from telegram import ParseMode


async def back_buttons_callback(call, chat_id, message_id):
    db = DB()
    kb = Keyboards()
    states = States()
    
    if call.data == "back_to_user_bots_list":
        cf.page = 1
        db.update_state(chat_id, states.main_state)
        
        return await bot.edit_message_caption(
            chat_id=chat_id,
            message_id=message_id,
            caption=f"<b><u>Мои боты</u></b>\n\n<b>🤖 Всего ботов:</b> <code>{len(db.get_user_bots(chat_id))}</code>",
            parse_mode=ParseMode.HTML,
            reply_markup=kb.user_bots_kb(chat_id, cf.page)[0]
        )

    if call.data == "back_to_user_bot_info":
        db.update_state(chat_id, states.main_state)
        
        current_bot = db.get_current_bot(chat_id)

        media = types.InputMediaPhoto(media=InputFile("background.jpg"))
            
        await bot.edit_message_media(
            chat_id=chat_id,
            message_id=message_id,
            media=media,
        )
        
        return await bot.edit_message_caption(
            chat_id=chat_id,
            message_id=message_id,
            caption=bot_info_text(current_bot),
            parse_mode=ParseMode.HTML,
            reply_markup=kb.bot_info_kb(chat_id)
        )
        
    if call.data == "back_to_profile":

        return await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"<b><u>Профиль</u></b>\n\n<b>👤 Профиль:</b> @{call.from_user.username}\n\n<b>💳 Баланс:</b> <code>{db.get_balance(chat_id)} ₽</code>",
            parse_mode=ParseMode.HTML,
            reply_markup=kb.profile_kb()
        )
    
    if call.data == "back_to_all_bots_list":
        
        return await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="<b><u>Список всех ботов</u></b>",
            parse_mode=ParseMode.HTML,
            reply_markup=kb.all_bots_kb(cf.page)[0]
        )
    
    if call.data == "back_to_withdrawal_requests_list":
        
        return await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="<b><u>Заявки на вывод</u></b>",
            parse_mode=ParseMode.HTML,
            reply_markup=kb.withdrawal_requests_kb(cf.page)[0]
        )
        
    if call.data == "back_to_premium":

        return await bot.edit_message_caption(
            chat_id=chat_id,
            message_id=message_id,
            caption=f"<b><u>Возможности с Премиум подпиской</u></b>\n\n<b>• Комиссия:</b> <s>13%</s> <b>3%</b>\n\n<b>• Нет упоминания сервиса в вашем боте</b>\n\n<b>• Обьязательная подписка пользователя на ваш канал</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=kb.premium_price_kb()
        )
