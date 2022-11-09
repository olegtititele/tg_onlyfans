from aiogram.types import ReplyKeyboardRemove, \
	ReplyKeyboardMarkup, KeyboardButton, \
	InlineKeyboardMarkup, InlineKeyboardButton


class ScrollKeyboard():

	def __init__(self, buttons: dict, height, current_page, next_call_data, previous_call_data):
		self.buttons = buttons
		self.height = height
		self.current_page = current_page
		self.next_call_data = next_call_data
		self.previous_call_data = previous_call_data

	def get_pages(self):
		pages = len(self.buttons) // self.height + bool(len(self.buttons) % self.height)
		return pages
		
	def render_keyboard(self):

		pages = self.get_pages()
		kb = InlineKeyboardMarkup()

		first_index = self.height * (self.current_page - 1)
		last_index = self.height * self.current_page

		for button, callback in list(self.buttons.items())[first_index:last_index]:
			btn = InlineKeyboardButton(button, callback_data=callback)
			kb.add(btn)

		if pages == 0 or pages == 1:
			return kb

		btn1 = InlineKeyboardButton(f"⬅", callback_data=f"{self.previous_call_data}")
		btn2 = InlineKeyboardButton(f'{self.current_page} | {pages}', callback_data=f'{self.current_page} | {pages}')
		btn3 = InlineKeyboardButton(f'➡', callback_data=f"{self.next_call_data}")
		
		kb.add(btn1, btn2, btn3)

		return kb