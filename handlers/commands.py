import os
import time
from threading import *
from db.db import DB
from keyboards.keyboards import Keyboards
import config.config as cf
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from config.states import States
from create_bot import bot
from telegram import ParseMode

async def command_start(message: types.Message):
    db = DB()
    kb = Keyboards()
    states = States()
    chat_id = message.from_user.id
    
    db.update_state(chat_id, states.main_state)
    
    

    if db.check_if_user_exists(chat_id):
        
        await bot.send_message(
            chat_id=chat_id,
            text=f"<b>{message.from_user.full_name}, Добро пожаловать в бота!</b>\n\n<code>{cf.bot_description}</code>",
            parse_mode=ParseMode.HTML,
            reply_markup=kb.menu_button_kb()
        )
    else:
        if message.from_user.username is None:
            await bot.send_message(
                chat_id=chat_id,
                text="<b>Для того чтобы пользоваться ботом, необходимо указать @username!</b>",
                parse_mode=ParseMode.HTML,
            )
        else:
            invited_by_id = message.get_args()
            if not invited_by_id.isdigit():
                db.add_user(chat_id, message.from_user.username, None)
            else:
                db.add_user(chat_id, message.from_user.username, invited_by_id)
                
                await bot.send_message(
                    chat_id=invited_by_id,
                    text=f"<b>➕ У вас новый реферал!</b>",
                    parse_mode=ParseMode.HTML
                )
            
            for admin_id in cf.admins_chat_id:
                await bot.send_message(
                    chat_id=admin_id,
                    text=f"<b>👤 Зарегистрирован новый пользователь:</b> @{message.from_user.username}",
                    parse_mode=ParseMode.HTML
                )
                
            return await bot.send_message(
                chat_id=chat_id,
                text=f"<b>{message.from_user.full_name}, Добро пожаловать в бота!</b>\n\n<code>{cf.bot_description}</code>",
                parse_mode=ParseMode.HTML,
                reply_markup=kb.menu_button_kb()
            )
        
async def command_admin(message: types.Message):
    db = DB()
    kb = Keyboards()
    states = States()
    chat_id = message.from_user.id

    if chat_id in cf.admins_chat_id:
        db.update_state(chat_id, states.main_state)
        if "db" in message.text:
            f = open("database.db", "rb")
            return await bot.send_document(message.chat.id, f)
          
        
        text = f"<b><u>Профиль</u></b>\n\n<b>👋 Саламалейкум, @{message.from_user.username}!</b>\n\n<b>🏦 Всего пополнений во всех ботах:</b> <code>{db.get_total_replenishment()} ₽</code>\n\n<b>🤖 Всего ботов:</b> <code>{len(db.get_all_users_bots())}</code>\n\n<b>💯 Процент комиссии:</b> <code>{db.get_commission_percentage()}%</code>\n\n<b>💯 Процент реферала с комиссии:</b> <code>{db.get_referal_bonus()}%</code>\n\n<b>💯 Процент реферала в боте пользователя:</b> <code>{db.get_referal_bonus_in_user_bot()}%</code>"
        
        await bot.send_message(
            chat_id=message.chat.id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=kb.admin_kb()
        )
    
    
    
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_admin, commands=['admin'])
