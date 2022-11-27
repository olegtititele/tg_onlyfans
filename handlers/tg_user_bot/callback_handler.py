from db.db import DB

from .methods import *

menu_keyboard = { "keyboard": [["📹 Видео", "📷 Фото"], ["💼 Профиль"], ["💵 Пополнить баланс"]], "resize_keyboard": True}


async def callback_handler(token, callback):
    db = DB()
    chat_id = callback['callback_query']['from']['id']
    call_data = callback['callback_query']['data']
    bot_username = (await get_me(token))['username']
    admin_id = db.get_user_bot_created_by_id(bot_username)
    
    if db.get_subscription_time(admin_id) > 0:
        subscription_channel_id = db.get_bot_subscription_channel_id(bot_username)
        if not subscription_channel_id is None:
            user_channel_status = (await get_chat_member(token=token, chat_id=subscription_channel_id, user_id=chat_id))['status']
            
            if user_channel_status == 'left':
                subscription_channel_link = db.get_bot_subscription_channel_link(bot_username)
                return await send_message(
                    token=token,
                    chat_id=chat_id,
                    text=f"<b>Подпишитесь на канал:  {subscription_channel_link}</b>"
                )
    
    
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
