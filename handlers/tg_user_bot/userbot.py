import asyncio
from .methods import *
from db.db import DB
from .message_handler import message_handler
from .callback_handler import callback_handler

async def check_updates(token, update):
    if "message" in update:
        await message_handler(token, update)
    elif "callback_query":
        await callback_handler(token, update)
    else:
        pass


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
                    
            
            await asyncio.sleep(2)
        except:
            await asyncio.sleep(10)
