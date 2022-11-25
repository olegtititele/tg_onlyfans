from db.db import DB

def bot_info_text(bot_username):
    db = DB()
    created_date = db.get_user_bot_created_time(bot_username)
    users_count = len(db.get_users_from_bot(bot_username))
    images = len(db.get_bot_photos(bot_username))
    photo_price = db.get_user_bot_photo_price(bot_username)
    videos = len(db.get_bot_videos(bot_username))
    video_price = db.get_user_bot_video_price(bot_username)
    created_by_username = db.get_user_bot_created_by_username(bot_username)
    start_ref_sum = db.get_bot_referal_sum(bot_username)
    invited_ref_sum = db.get_bot_invited_ref_sum(bot_username)
    
    
    text = f"<b><u>Информация о боте</u></b>\n\n<b>🤖 Username бота:</b> @{bot_username}\n\n<b>👥 Кол-во пользователей:</b> <code>{users_count}</code>\n\n<b>👔 Админ:</b> @{created_by_username}\n\n<b>⌚️ Дата создания бота:</b> <code>{created_date}</code>\n\n<b>💲 Реферал за приглашенного пользователя:</b> <code>{invited_ref_sum} ₽</code>\n\n<b>💲 Стартовый баланс:</b> <code>{start_ref_sum} ₽</code>\n\n<b>🖼 Фото:</b> <code>{images}</code>\n<b>💲 Стоимость фото:</b> <code>{photo_price} ₽</code>\n\n<b>🖼 Видео:</b> <code>{videos}</code>\n<b>💲 Стоимость видео:</b> <code>{video_price} ₽</code>"
    
    return text