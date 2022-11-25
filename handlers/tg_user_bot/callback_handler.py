from db.db import DB

from .methods import *

menu_keyboard = { "keyboard": [["🖼 Видео", "🖼 Фото"], ["💼 Профиль"], ["💵 Пополнить баланс"]], "resize_keyboard": True}


async def callback_handler(token, callback):
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
