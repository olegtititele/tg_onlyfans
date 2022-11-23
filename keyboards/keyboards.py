import config.config as cf
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from dateutil.parser import parse
from db.db import DB
import config.config as cf
from keyboards.scroll_keyboard import ScrollKeyboard

height = 9
back_to_menu_btn = InlineKeyboardButton(f'🔙 Назад в меню', callback_data='back_to_menu')

class Keyboards():

	def __init__(self):
		self.db = DB()


	def menu_button_kb(self):
		profile_btn = KeyboardButton('👤 Профиль 👤')
		premium_btn = KeyboardButton('💎 Премиум 💎')
		ref_btn = KeyboardButton('👥 Реферальная система 👥')
		my_bots_btn = KeyboardButton('🤖 Мои боты 🤖')
		
		main_menu_kb = ReplyKeyboardMarkup(
			resize_keyboard=True, one_time_keyboard=False
		)


		main_menu_kb.add(profile_btn, premium_btn)
		main_menu_kb.add(ref_btn)
		main_menu_kb.add(my_bots_btn)

		return main_menu_kb

	def premium_price_kb(self):
		first_btn = InlineKeyboardButton(f'1 месяц / {cf.price_for_one_month} ₽', callback_data=f'one_month_price')
		second_btn = InlineKeyboardButton(f'3 месяца / {cf.price_for_three_month} ₽', callback_data=f'three_month_price')
		third_btn = InlineKeyboardButton(f'6 месяцев / {cf.price_for_six_month} ₽', callback_data=f'six_month_price')
		kb = InlineKeyboardMarkup()
		kb.row(first_btn)
		kb.row(second_btn)
		kb.row(third_btn)

		return kb

	def payment_methods_kb(self):
		popup_qiwi = InlineKeyboardButton('🥝 QIWI', callback_data=f'popup_qiwi')
		popup_ym = InlineKeyboardButton('👛 YOOMONEY', callback_data=f'popup_yoomoney')
		popup_from_balance = InlineKeyboardButton(f'💳 Баланс ', callback_data=f'popup_from_balance')
		back_btn = InlineKeyboardButton('🔙 Назад', callback_data='back_to_premium')
		kb = InlineKeyboardMarkup()
		kb.row(popup_qiwi)
		kb.row(popup_ym)
		kb.row(popup_from_balance)
		kb.row(back_btn)

		return kb

	def pay_kb(self, pay_url):
		popup_btn = InlineKeyboardButton('Оплатить', url=f'{pay_url}')
		kb = InlineKeyboardMarkup()
		kb.row(popup_btn)
  
		return kb

	def admin_kb(self):
		show_bots_list_btn = KeyboardButton('📃 Посмотреть список ботов')
		change_proc_btn = KeyboardButton('💯 Комиссия')
		change_ref_btn = KeyboardButton('💯 Реферал')
		change_ref_in_user_bot_btn = KeyboardButton('💯 Реферал в боте пользователя')
		start_referal_btn = KeyboardButton('💯 Реферал при старте')
		withdrawal_requests_btn = KeyboardButton('🏦 Заявки на вывод')
		popup_balance_btn = KeyboardButton('💰 Зачислить баланс')
		alert_btn = KeyboardButton('✉️ Рассылка')
		
		kb = ReplyKeyboardMarkup(
			resize_keyboard=True, one_time_keyboard=False
		)
  
		kb.add(show_bots_list_btn)
		kb.add(change_proc_btn, change_ref_btn)
		kb.add(change_ref_in_user_bot_btn)
		kb.add(start_referal_btn)
		kb.add(alert_btn, popup_balance_btn)
		kb.add(withdrawal_requests_btn)


		return kb

	def choose_bot_for_popup_kb(self):
		this_bot_btn = InlineKeyboardButton('В боте конструкторе', callback_data=f'popup_in_this_bot')
		another_bot_btn = InlineKeyboardButton('В другом боте', callback_data=f'popup_in_another_bot')
		kb = InlineKeyboardMarkup()
		kb.row(this_bot_btn)
		kb.row(another_bot_btn)

		return kb

	def profile_kb(self):
		statistic_btn = InlineKeyboardButton('📈 Статистика', callback_data=f'statistic')
		withdrawal_btn = InlineKeyboardButton('💸 Вывод средств', callback_data=f'withdrawal')
		kb = InlineKeyboardMarkup()
		kb.row(statistic_btn)
		kb.row(withdrawal_btn)

		return kb

	def withdrawal_kb(self):
		qiwi_btn = InlineKeyboardButton('🥝 QIWI', callback_data=f'QIWI_withdrawal')
		ym_btn = InlineKeyboardButton('👛 YOOMONEY', callback_data=f'YOOMONEY_withdrawal')
		back_btn = InlineKeyboardButton('🔙 Назад', callback_data='back_to_profile')
		kb = InlineKeyboardMarkup()
		kb.row(qiwi_btn, ym_btn)
		kb.row(back_btn)

		return kb

	def confrim_withdrawal_kb(self, id):
		confrim_btn = InlineKeyboardButton('✅ Отправил', callback_data=f'confrim_withdrawal-{id}')
		kb = InlineKeyboardMarkup()
		kb.row(confrim_btn)

		return kb

	def confrimed_withdrawal_kb(self):
		confrim_btn = InlineKeyboardButton('☑️ Средства отправлены', callback_data=f'----------')
		kb = InlineKeyboardMarkup()
		kb.row(confrim_btn)

		return kb
		
	def all_bots_kb(self, page):
		buttons = {}
		bots = self.db.get_all_users_bots()
		next_call_data = "next_bots_list"
		previous_call_data = "previous_bots_list"

		for bot in bots:
			buttons[f"@{bot[0]}"] = f"admin|{bot[0]}"

		scroll_kb = ScrollKeyboard(buttons, height, page, next_call_data, previous_call_data)
		pages = scroll_kb.get_pages()
		kb = scroll_kb.render_keyboard()
  
		return kb, pages
 
	def user_bots_kb(self, user_id, page):
		buttons = {}
		bots = self.db.get_user_bots(user_id)
		next_call_data = "next_user_bots_list"
		previous_call_data = "previous_user_bots_list"

		for bot in bots:
			buttons[f"@{bot[0]}"] = bot[0]

		scroll_kb = ScrollKeyboard(buttons, height, page, next_call_data, previous_call_data)
		pages = scroll_kb.get_pages()
		kb = scroll_kb.render_keyboard()

		add_new_bot_btn = InlineKeyboardButton('➕ Добавить бота', callback_data='add_new_bot')
		kb.row(add_new_bot_btn)
  
		return kb, pages

	def bot_info_kb(self):
		show_all_images_btn = InlineKeyboardButton('📷 Посмотреть все изображения', callback_data=f'show_all_images')
		show_all_videos_btn = InlineKeyboardButton('🎥 Посмотреть все видео', callback_data=f'show_all_videos')
		edit_photo_price_btn = InlineKeyboardButton('💶 Изменить стоимость фото', callback_data=f'edit_photo_price')
		edit_video_price_btn = InlineKeyboardButton('💷 Изменить стоимость видео', callback_data=f'edit_video_price')
		upload_material_btn = InlineKeyboardButton('🖼 Загрузить материал', callback_data=f'upload_material')
		delete_bot_btn = InlineKeyboardButton('🗑 Удалить бота', callback_data=f'delete_bot')
		back_btn = InlineKeyboardButton('🔙 Назад', callback_data='back_to_user_bots_list')
  
		kb = InlineKeyboardMarkup()
		kb.add(show_all_images_btn)
		kb.add(show_all_videos_btn)
		kb.add(edit_photo_price_btn)
		kb.add(edit_video_price_btn)
		kb.add(upload_material_btn)
		kb.add(delete_bot_btn)
		kb.add(back_btn)
  
		return kb

	def show_images_kb(self, current_material, total_materials):
		btn1 = InlineKeyboardButton(f"«", callback_data=f"previous_image")
		btn2 = InlineKeyboardButton(f'{current_material} | {total_materials}', callback_data=f'{current_material} | {total_materials}')
		btn3 = InlineKeyboardButton(f'»', callback_data=f"next_image")
		delete_material_btn = InlineKeyboardButton('🗑 Удалить', callback_data=f'delete_image')
		back_btn = InlineKeyboardButton('🔙 Назад', callback_data='back_to_user_bot_info')
		kb = InlineKeyboardMarkup()
  		
		kb.add(delete_material_btn)
		kb.add(btn1, btn2, btn3)
		kb.add(back_btn)
  
		return kb

	def show_videos_kb(self, current_material, total_materials):
		btn1 = InlineKeyboardButton(f"«", callback_data=f"previous_video")
		btn2 = InlineKeyboardButton(f'{current_material} | {total_materials}', callback_data=f'{current_material} | {total_materials}')
		btn3 = InlineKeyboardButton(f'»', callback_data=f"next_video")
		delete_material_btn = InlineKeyboardButton('🗑 Удалить', callback_data=f'delete_video')
		back_btn = InlineKeyboardButton('🔙 Назад', callback_data='back_to_user_bot_info')
		kb = InlineKeyboardMarkup()
  		
		kb.add(delete_material_btn)
		kb.add(btn1, btn2, btn3)
		kb.add(back_btn)
  
		return kb
 
	def withdrawal_requests_kb(self, page):
		buttons = {}
		withdrawal_requests = self.db.get_withdrawal_requests()
		next_call_data = "next_withdrawal_requests_list"
		previous_call_data = "previous_withdrawal_requests_list"

		for withdrawal_request in withdrawal_requests:
			if withdrawal_request[4] == "incomplete":
				buttons[f'⚪️ {round(withdrawal_request[2], 2)} ₽ | {parse(withdrawal_request[3]).strftime("%d.%m.%Y %H:%M")}'] = withdrawal_request[0]
			else:
				buttons[f'🟢 {round(withdrawal_request[2], 2)} ₽ | {parse(withdrawal_request[3]).strftime("%d.%m.%Y %H:%M")}'] = withdrawal_request[0]
			

		scroll_kb = ScrollKeyboard(buttons, height, page, next_call_data, previous_call_data)
		pages = scroll_kb.get_pages()
		kb = scroll_kb.render_keyboard()
  
		return kb, pages

	def delete_img_kb(self, id):
		decline_btn = InlineKeyboardButton('⛔️ Удалить', callback_data=f'del_img-{id}')
		kb = InlineKeyboardMarkup()
		kb.row(decline_btn)

		return kb

	def delete_video_kb(self, id):
		decline_btn = InlineKeyboardButton('⛔️ Удалить', callback_data=f'del_vid-{id}')
		kb = InlineKeyboardMarkup()
		kb.row(decline_btn)

		return kb

	def back_to_user_bots_list_kb(self):
		back_btn = InlineKeyboardButton('🔙 Назад', callback_data='back_to_user_bots_list')
		kb = InlineKeyboardMarkup()
		kb.add(back_btn)

		return kb

	def back_to_user_bot_info_kb(self):
		back_btn = InlineKeyboardButton('🔙 Назад', callback_data='back_to_user_bot_info')
		kb = InlineKeyboardMarkup()
		kb.add(back_btn)

		return kb

	def back_to_profile_kb(self):
		back_btn = InlineKeyboardButton('🔙 Назад', callback_data='back_to_profile')
		kb = InlineKeyboardMarkup()
		kb.add(back_btn)

		return kb

	def back_to_all_bots_list_kb(self):
		back_btn = InlineKeyboardButton('🔙 Назад', callback_data='back_to_all_bots_list')
		kb = InlineKeyboardMarkup()
		kb.add(back_btn)

		return kb

	def back_to_withdrawal_requests_list_kb(self, w_id):
		db = DB()
		kb = InlineKeyboardMarkup()
  
		if db.get_withdrawal_request_status(w_id) == "incomplete":
			confrim_btn = InlineKeyboardButton('✅ Отправил средства', callback_data=f'c_w_adm-{w_id}')
			kb.add(confrim_btn)
   
		back_btn = InlineKeyboardButton('🔙 Назад', callback_data='back_to_withdrawal_requests_list')
		kb.add(back_btn)

		return kb