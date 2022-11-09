import json
import sqlite3
from datetime import datetime, timedelta

from dateutil.parser import parse


class DB():

    def __init__(self):
        self.connection = sqlite3.connect("database.db")


    # # user

    def create_users_table(self):
        cursor = self.connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS users (user_id BIGINT PRIMARY KEY, username TEXT, state TEXT, status TEXT, balance REAL, current_bot TEXT, invited_by TEXT, current_material BLOB, storage TEXT);''')
        self.connection.commit()

    def add_user(self, user_id, username, invited_by):
        cursor = self.connection.cursor()
        state = "main_state"
        status = "user"
        balance = 0
        current_bot = None
        current_material = None
        storage = {}
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, username, state, status, balance, current_bot, invited_by, current_material, json.dumps(storage), ))
        self.connection.commit()
        
    def check_if_user_exists(self, user_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = ?;", (user_id,))
            data = cursor.fetchone()[0]
            return True
        except Exception:
            return False
        
    def get_user(self, user):
        cursor = self.connection.cursor()
        if user.isdigit():
            user_id = int(user)
            cursor.execute("SELECT * FROM users WHERE user_id = ?;", (user_id,))
            data = cursor.fetchone()
        else:
            cursor.execute("SELECT * FROM users WHERE username = ?;", (user,))
            data = cursor.fetchone()
        
        return data
    
    def get_username(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT username FROM users WHERE user_id = ?;", (user_id,))
        data = cursor.fetchone()[0]
        return data
    
    def get_invited_by(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT invited_by FROM users WHERE user_id = ?;", (user_id,))
        data = cursor.fetchone()[0]
        return data
        
    def get_state(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT state FROM users WHERE user_id = ?;", (user_id,))
        data = cursor.fetchone()[0]
        return data

    def update_state(self, user_id, state):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET state = ? WHERE user_id = ?", (state, user_id,))
        self.connection.commit()
        
    # storage
    def get_storage(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT storage FROM users WHERE user_id = ?;", (user_id,))
        storage = json.loads(cursor.fetchone()[0])
        
        return storage
    
    def update_storage(self, user_id, storage):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET storage = ? WHERE user_id = ?;", (json.dumps(storage), user_id,))
        self.connection.commit()
        
    def get_balance(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT balance FROM users WHERE user_id = ?;", (user_id,))
        balance = round(cursor.fetchone()[0], 2)
        return balance
    
    def update_balance(self, user_id, balance):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (balance, user_id,))
        self.connection.commit()

    def get_current_bot(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT current_bot FROM users WHERE user_id = ?;", (user_id,))
        data = cursor.fetchone()[0]
        return data

    def update_current_bot(self, user_id, current_bot):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET current_bot = ? WHERE user_id = ?;", (current_bot, user_id,))
        self.connection.commit()
        
    def get_current_material(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT current_material FROM users WHERE user_id = ?;", (user_id,))
        data = cursor.fetchone()[0]
        return data

    def update_current_material(self, user_id, current_material):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET current_material = ? WHERE user_id = ?", (current_material, user_id,))
        self.connection.commit()
        
    def get_all_users(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users;")
        data = cursor.fetchall()
        
        return data
    
    def get_referals_count(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE invited_by = ?;", (user_id,))
        data = cursor.fetchall()
        return data
        
        
    
    
    # # bot information
    
    def create_bot_information_table(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f'''CREATE TABLE bot_information (commission_percentage INT, referal_bonus INT, qiwi_api TEXT);''')
            self.connection.commit()
            cursor.execute("INSERT INTO bot_information VALUES (?, ?, ?)", (15, 10, None, ))
            self.connection.commit()
        except:
            pass
     
    def get_commission_percentage(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT commission_percentage FROM bot_information;")
        data = cursor.fetchone()[0]
        return data
    
    def update_commission_percentage(self, percentage):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE bot_information SET commission_percentage = ?;", (percentage,))
        self.connection.commit()
        
    def get_referal_bonus(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT referal_bonus FROM bot_information;")
        data = cursor.fetchone()[0]
        return data
    
    def update_referal_bonus(self, percentage):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE bot_information SET referal_bonus = ?;", (percentage,))
        self.connection.commit()
        
    def get_qiwi_api(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT qiwi_api FROM bot_information;")
        data = cursor.fetchone()[0]
        return data
    
    def update_qiwi_api(self, qiwi_api):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE bot_information SET qiwi_api = ?;", (qiwi_api,))
        self.connection.commit()
        
        
        
    # # user_bot table
    
    def create_users_bots_table(self):
        cursor = self.connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS users_bots (bot_username TEXT PRIMARY KEY, token TEXT, created_by_id BIGINT, created_by_username TEXT, created_time TIMESTAMP, photo_price REAL, video_price REAL);''')
        self.connection.commit()
        
    def add_new_bot(self, bot_username, token, created_by_id, created_by_username):
        created_time = datetime.now()
        photo_price = 10
        video_price = 10
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO users_bots VALUES (?, ?, ?, ?, ?, ?, ?)", (bot_username, token, created_by_id, created_by_username, created_time, photo_price, video_price, ))
        self.connection.commit()
        
    def delete_user_bot(self, bot_username):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM users_bots WHERE bot_username = ?;", (bot_username, ))
        self.connection.commit()
        
    def get_user_bot(self, bot_username):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users_bots WHERE bot_username = ?;", (bot_username,))
            data = cursor.fetchone()
        except:
            return None
        
        return data
        
    def get_user_bot_created_by_id(self, bot_username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT created_by_id FROM users_bots WHERE bot_username = ?;", (bot_username,))
        data = cursor.fetchone()[0]
        
        return data
    
    def get_user_bot_created_by_username(self, bot_username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT created_by_username FROM users_bots WHERE bot_username = ?;", (bot_username,))
        data = cursor.fetchone()[0]
        
        return data
    
    def get_user_bots(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users_bots WHERE created_by_id = ?;", (user_id,))
        data = cursor.fetchall()
        
        return data
        
    def get_all_users_bots(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users_bots;")
        data = cursor.fetchall()
        
        return data
        
    def get_user_bot_created_time(self, bot_username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT created_time FROM users_bots WHERE bot_username = ?;", (bot_username,))
        data = cursor.fetchone()[0]
        created_time = parse(data).strftime("%d.%m.%Y %H:%M:%S")
        
        return created_time
        
        
    def get_user_bot_photo_price(self, bot_username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT photo_price FROM users_bots WHERE bot_username = ?;", (bot_username,))
        data = cursor.fetchone()[0]
        
        return data
    
    def update_user_bot_photo_price(self, bot_username, price):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users_bots SET photo_price = ? WHERE bot_username = ?", (price, bot_username,))
        self.connection.commit()
        
        
    def get_user_bot_video_price(self, bot_username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT video_price FROM users_bots WHERE bot_username = ?;", (bot_username,))
        data = cursor.fetchone()[0]
        
        return data
    
    def update_user_bot_video_price(self, bot_username, price):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users_bots SET video_price = ? WHERE bot_username = ?", (price, bot_username,))
        self.connection.commit()
        
    
    
    
    
    # # transactions
    
    def create_transactions_table(self):
        cursor = self.connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS transactions (user_id BIGINT, bot_username TEXT, date TIMESTAMP, sum REAL);''')
        self.connection.commit()
        
    def add_new_transaction(self, user_id, bot_username, sum):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO transactions VALUES (?, ?, ?, ?)", (user_id, bot_username, datetime.now(), sum, ))
        self.connection.commit()  
        
    def get_transactions(self, bot_username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM transactions WHERE bot_username = ?;", (bot_username,))
        data = cursor.fetchall()
        
        return data
        
    # total
    def get_total_income(self, user_id):
        user_bots = self.get_user_bots(user_id)
        total_income = 0
        
        for user_bot in user_bots:
            bot_username = user_bot[0]
            transactions = self.get_transactions(bot_username)
            for transaction in transactions:
                transaction_sum = float(transaction[3])
                total_income += transaction_sum
                
        return total_income
    
    def get_total_subscriptions(self, user_id):
        user_bots = self.get_user_bots(user_id)
        total_subscriptions = 0
        
        for user_bot in user_bots:
            bot_username = user_bot[0]
            bot_users = len(self.get_subscriptions_from_user_bot(bot_username))
            total_subscriptions += bot_users
            
        return total_subscriptions
        
    
    # month
    def get_monthly_income(self, user_id):
        user_bots = self.get_user_bots(user_id)
        monthly_income = 0
        
        for user_bot in user_bots:
            bot_username = user_bot[0]
            transactions = self.get_transactions(bot_username)
            for transaction in transactions:
                transaction_date = parse(transaction[2])
                if datetime.now() + timedelta(days=-30) <= transaction_date:
                    transaction_sum = float(transaction[3])
                    monthly_income += transaction_sum
                
        return monthly_income
    
    def get_monthly_subscriptions(self, user_id):
        user_bots = self.get_user_bots(user_id)
        monthly_subscriptions = 0
        
        for user_bot in user_bots:
            bot_username = user_bot[0]
            bot_users = self.get_subscriptions_from_user_bot(bot_username)
            for bot_user in bot_users:
                reg_date = parse(bot_user[1])
                if datetime.now() + timedelta(days=-30) <= reg_date:
                    monthly_subscriptions += 1
            
        return monthly_subscriptions
    
    
    # week
    def get_weekly_income(self, user_id):
        user_bots = self.get_user_bots(user_id)
        weekly_income = 0
        
        for user_bot in user_bots:
            bot_username = user_bot[0]
            transactions = self.get_transactions(bot_username)
            for transaction in transactions:
                transaction_date = parse(transaction[2])
                if datetime.now() + timedelta(days=-7) <= transaction_date:
                    transaction_sum = float(transaction[3])
                    weekly_income += transaction_sum
                
        return weekly_income
    
    def get_weekly_subscriptions(self, user_id):
        user_bots = self.get_user_bots(user_id)
        weekly_subscriptions = 0
        
        for user_bot in user_bots:
            bot_username = user_bot[0]
            bot_users = self.get_subscriptions_from_user_bot(bot_username)
            for bot_user in bot_users:
                reg_date = parse(bot_user[1])
                if datetime.now() + timedelta(days=-7) <= reg_date:
                    weekly_subscriptions += 1
            
        return weekly_subscriptions
    
    
    # day
    def get_daily_income(self, user_id):
        user_bots = self.get_user_bots(user_id)
        daily_income = 0
        
        for user_bot in user_bots:
            bot_username = user_bot[0]
            transactions = self.get_transactions(bot_username)
            for transaction in transactions:
                transaction_date = parse(transaction[2])
                if datetime.now() + timedelta(days=-1) <= transaction_date:
                    transaction_sum = float(transaction[3])
                    daily_income += transaction_sum
                
        return daily_income
    
    def get_daily_subscriptions(self, user_id):
        user_bots = self.get_user_bots(user_id)
        daily_subscriptions = 0
        
        for user_bot in user_bots:
            bot_username = user_bot[0]
            bot_users = self.get_subscriptions_from_user_bot(bot_username)
            for bot_user in bot_users:
                reg_date = parse(bot_user[1])
                if datetime.now() + timedelta(days=-1) <= reg_date:
                    daily_subscriptions += 1
            
        return daily_subscriptions
            
        

    # # withdrawal requests

    def create_withdrawal_requests_table(self):
        cursor = self.connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS withdrawal_requests (id BIGINT, user_id BIGINT, sum REAL, date TIMESTAMP, status TEXT, wallet_type TEXT, wallet_number TEXT);''')
        self.connection.commit()
        
    def add_new_withdrawal_request(self, withdrawal_id, user_id, sum, wallet_type, wallet_number):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO withdrawal_requests VALUES (?, ?, ?, ?, ?, ?, ?)", (withdrawal_id, user_id, sum, datetime.now(), "incomplete", wallet_type, wallet_number, ))
        self.connection.commit()
        
    def get_withdrawal_requests(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM withdrawal_requests ORDER BY status DESC;")
        data = cursor.fetchall()
        
        return data
    
    def get_withdrawal_request(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM withdrawal_requests WHERE id = ?;", (id, ))
        data = cursor.fetchone()
        
        return data
    
    def update_withdrawal_request_status(self, id):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE withdrawal_requests SET status = ? WHERE id = ?;", ("complete", id, ))
        self.connection.commit()
        
    def get_withdrawal_request_status(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT status FROM withdrawal_requests WHERE id = ?;", (id, ))
        data = cursor.fetchone()[0]
        
        return data
    
    
    # # replenishment
    
    def create_replenishment_table(self):
        cursor = self.connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS replenishment (user_id BIGINT, sum REAL);''')
        self.connection.commit()
        
    def add_new_replenishment(self, user_id, sum):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO replenishment VALUES (?, ?)", (user_id, sum, ))
        self.connection.commit()
    
    def get_total_replenishment(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT sum FROM replenishment;")
        data = cursor.fetchall()
        total_replenishment = 0
        
        for sum in data:
            total_replenishment += sum[0]
            
        return total_replenishment
    

    # # photos table
    
    def create_photos_table(self):
        cursor = self.connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS photos_table (photo BLOB, bot_username TEXT, viewed_users TEXT);''')
        self.connection.commit()
        
        
    def add_photo(self, photo, bot_username):
        viewed_users = []
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO photos_table VALUES (?, ?, ?)", (photo, bot_username, json.dumps(viewed_users), ))
        self.connection.commit()
        
    def get_user_bot_photos(self, bot_username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT photo FROM photos_table WHERE bot_username = ?;", (bot_username,))
        data = cursor.fetchall()
        
        return data
    
    def get_total_bots_images(self, user_id):
        user_bots = self.get_user_bots(user_id)
        total_images = 0
        
        for user_bot in user_bots:
            bot_username = user_bot[0]
            images = len(self.get_user_bot_photos(bot_username))
            total_images += images
                
        return total_images
    
    def delete_photo(self, bot_username, photo):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM photos_table WHERE bot_username = ? AND photo = ?;", (bot_username, photo, ))
        self.connection.commit()
        
    def get_viewed_users_on_photo(self, bot_username, photo):
        cursor = self.connection.cursor()
        cursor.execute("SELECT viewed_users FROM photos_table WHERE bot_username = ? AND photo = ?;", (bot_username, photo, ))
        data = json.loads(cursor.fetchone()[0])
        
        return data
        
    def update_viewed_users_on_photo(self, bot_username, photo, viewed_users):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE photos_table SET viewed_users = ? WHERE bot_username = ? AND photo = ?;", (json.dumps(viewed_users), bot_username, photo,))
        self.connection.commit()
    
    
    
    
    # # videos table
    
    def create_videos_table(self):
        cursor = self.connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS videos_table (video BLOB, bot_username TEXT, viewed_users TEXT);''')
        self.connection.commit()
        
        
    def add_video(self, video, bot_username):
        viewed_users = []
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO videos_table VALUES (?, ?, ?)", (video, bot_username, json.dumps(viewed_users), ))
        self.connection.commit()
        
    def get_user_bot_videos(self, bot_username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT video FROM videos_table WHERE bot_username = ?;", (bot_username,))
        data = cursor.fetchall()
        
        return data
    
    def get_total_bots_videos(self, user_id):
        user_bots = self.get_user_bots(user_id)
        total_videos = 0
        
        for user_bot in user_bots:
            bot_username = user_bot[0]
            videos = len(self.get_user_bot_videos(bot_username))
            total_videos += videos
                
        return total_videos
    
    def delete_video(self, bot_username, video):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM videos_table WHERE bot_username = ? AND video = ?;", (bot_username, video, ))
        self.connection.commit()
        
    def get_viewed_users_on_video(self, bot_username, video):
        cursor = self.connection.cursor()
        cursor.execute("SELECT viewed_users FROM videos_table WHERE bot_username = ? AND video = ?;", (bot_username, video, ))
        data = json.loads(cursor.fetchone()[0])
        
        return data
        
    def update_viewed_users_on_video(self, bot_username, video, viewed_users):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE videos_table SET viewed_users = ? WHERE bot_username = ? AND video = ?;", (json.dumps(viewed_users), bot_username, video,))
        self.connection.commit()
    




    # # user_bot
    
    def create_bot_table(self, bot_username):
        cursor = self.connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {bot_username} (user_id BIGINT PRIMARY KEY, username TEXT, reg_date TIMESTAMP, state TEXT, balance REAL, invited_by TEXT);''')
        self.connection.commit()
        
    def add_new_user_in_user_bot(self, bot_username, user_id, username, invited_by):
        cursor = self.connection.cursor()
        reg_date = datetime.now()
        state = "main_state"
        balance = 0
        cursor.execute(f"INSERT INTO {bot_username} VALUES (?, ?, ?, ?, ?, ?);", (user_id, username, reg_date, state, balance, invited_by, ))
        self.connection.commit()
        
    def check_if_user_exists_in_user_bot(self, bot_username, user_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM {bot_username} WHERE user_id = ?;", (user_id,))
            data = cursor.fetchone()[0]
            return True
        except Exception:
            return False
        
    def get_user_from_user_bot(self, bot_username, user):
        cursor = self.connection.cursor()
        if user.isdigit():
            user_id = int(user)
            cursor.execute(f"SELECT * FROM {bot_username} WHERE user_id = ?;", (user_id,))
            data = cursor.fetchone()
        else:
            cursor.execute(f"SELECT * FROM {bot_username} WHERE username = ?;", (user,))
            data = cursor.fetchone()
        
        return data
        
    def get_subscriptions_from_user_bot(self, bot_username):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT user_id, reg_date FROM {bot_username};")
        data = cursor.fetchall()
        return data
    
    def get_state_from_user_bot(self, bot_username, user_id):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT state FROM {bot_username} WHERE user_id = ?;", (user_id,))
        data = cursor.fetchone()[0]
        return data

    def update_state_from_user_bot(self, bot_username, user_id, state):
        cursor = self.connection.cursor()
        cursor.execute(f"UPDATE {bot_username} SET state = ? WHERE user_id = ?", (state, user_id, ))
        self.connection.commit()
    
    def get_balance_from_user_bot(self, bot_username, user_id):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT balance FROM {bot_username} WHERE user_id = ?;", (user_id,))
        data = round(cursor.fetchone()[0], 2)
        return data

    def update_balance_from_user_bot(self, bot_username, user_id, balance):
        cursor = self.connection.cursor()
        cursor.execute(f"UPDATE {bot_username} SET balance = ? WHERE user_id = ?", (balance, user_id, ))
        self.connection.commit()
        
    def get_invited_users_from_user_bot(self, bot_username, user_id):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT invited_by FROM {bot_username} WHERE invited_by = ?;", (user_id, ))
        data = len(cursor.fetchall())
        return data


