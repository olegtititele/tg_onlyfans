import aiohttp
import json

URL = 'https://api.telegram.org/bot'

async def get_updates(token, offset=0):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{URL}{token}/getUpdates?offset={offset}') as resp:
            result = await resp.json()
            return result['result']

async def send_message(token, chat_id, text, reply_markup={}):
    data = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup), 'parse_mode': 'HTML'}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{URL}{token}/sendMessage', data=data) as resp:
            await resp.json()
            
async def send_photo(token, chat_id, photo, caption=""):
    data = {'chat_id': chat_id, 'photo': photo, 'caption': caption}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{URL}{token}/sendPhoto', data=data) as resp:
            await resp.json()
            
async def send_video(token, chat_id, video):
    data = {'chat_id': str(chat_id), 'video': video}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{URL}{token}/sendVideo', data=data) as resp:
            await resp.json()
           
async def get_me(token):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{URL}{token}/getMe') as resp:
            return (await resp.json())['result']
        
async def get_chat_member(token, chat_id, user_id):
    data = {'chat_id': str(chat_id), 'user_id': int(user_id)}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{URL}{token}/getChatMember', data=data) as resp:
            return (await resp.json())['result']