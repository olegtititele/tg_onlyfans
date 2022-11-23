import config.config as cf
from create_bot import bot
from keyboards.keyboards import *


async def scroll_buttons_callback(call, chat_id, message_id):
    kb = Keyboards()
    
    if call.data == "previous_withdrawal_requests_list":  
        return await previous_page(chat_id, message_id, kb.withdrawal_requests_kb(cf.page-1))
        
    if call.data == "next_withdrawal_requests_list":
        return await next_page(chat_id, message_id, kb.withdrawal_requests_kb(cf.page+1))
    
    if call.data == "previous_bots_list":  
        return await previous_page(chat_id, message_id, kb.all_bots_kb(cf.page-1))
        
    if call.data == "next_bots_list":
        return await next_page(chat_id, message_id, kb.all_bots_kb(cf.page+1))
        
    if call.data == "previous_user_bots_list":  
        return await previous_page(chat_id, message_id, kb.user_bots_kb(chat_id, cf.page-1))
        
    if call.data == "next_user_bots_list":
        return await next_page(chat_id, message_id, kb.user_bots_kb(chat_id, cf.page+1))
        
        
async def next_page(chat_id, message_id, kb_info: tuple):
    scroll_kb_info = kb_info

    scroll_kb = scroll_kb_info[0]
    pages = scroll_kb_info[1]

    if cf.page >= pages:
        return
    else:
        cf.page += 1

    return await bot.edit_message_reply_markup(
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

    return await bot.edit_message_reply_markup(
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=scroll_kb
    )