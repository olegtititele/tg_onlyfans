import asyncio
import logging
from threading import *

import aioschedule
from aiogram import executor
from telegram import ParseMode

import handlers.userbot_handler as us_bot
from create_bot import bot, dp
from db.db import DB
from handlers import callback_handler, commands, message_handler
from keyboards.keyboards import *

logging.basicConfig(level=logging.INFO)



commands.register_handlers_client(dp)
message_handler.register_handlers_client(dp)
callback_handler.register_handlers_client(dp)
    

async def bot_on_start():
    db = DB()
    db.create_yoomoney_labels_table()
    db.create_bot_information_table()
    db.create_withdrawal_requests_table()
    db.create_replenishment_table()
    db.create_photos_table()
    db.create_videos_table()
    db.create_users_table()
    db.create_users_bots_table()
    db.create_transactions_table()
    
    asyncio.create_task(scheduler())
    
    for bot in db.get_all_users_bots():
        token = bot[1]
        try:
            asyncio.create_task(us_bot.run(token))
        except:
            pass
    
async def admin_today_alert():
    db = DB()
    for admin_id in cf.admins_chat_id:
        try:
            await bot.send_message(
                chat_id=admin_id, 
                text=f"<b><u>За сегодня</u></b>\n\n<b>🤖 Новых ботов:</b> <code>{db.get_today_new_bots()}</code>\n\n<b>💰 Пополнений:</b> <code>{db.get_today_replenishment()} ₽</code>\n\n<b>👤 Новых пользователей конструктора:</b> <code>{db.get_today_new_users()}</code>\n\n<b>👥 Новых пользователей ботов:</b> <code>{db.get_today_users_user_bots()}</code>",
                parse_mode=ParseMode.HTML
            )
        except:
            continue

async def scheduler():
    aioschedule.every().day.at("20:00").do(admin_today_alert)
    
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
        
    
    
if __name__ == "__main__":
    asyncio.gather(bot_on_start())
    executor.start_polling(dp, skip_updates=True)
    
