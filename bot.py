import asyncio
import logging
from threading import *

from aiogram import executor

import handlers.userbot_handler as us_bot
from create_bot import dp
from db.db import DB
from handlers import callback_handler, commands, message_handler
from keyboards.keyboards import *

logging.basicConfig(level=logging.INFO)



commands.register_handlers_client(dp)
message_handler.register_handlers_client(dp)
callback_handler.register_handlers_client(dp)
    

async def bot_on_start():
    db = DB()
    db.create_bot_information_table()
    db.create_withdrawal_requests_table()
    db.create_replenishment_table()
    db.create_photos_table()
    db.create_videos_table()
    db.create_users_table()
    db.create_users_bots_table()
    db.create_transactions_table()
    
    for bot in db.get_all_users_bots():
        token = bot[1]
        try:
            asyncio.create_task(us_bot.run(token))
        except:
            pass
    
    
if __name__ == "__main__":
    asyncio.gather(bot_on_start())
    executor.start_polling(dp, skip_updates=True)
    
