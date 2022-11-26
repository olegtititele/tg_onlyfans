import json
import mysql.connector
from datetime import datetime, timedelta
from dateutil.parser import parse

class DB():

    def __init__(self):
        self.connection = mysql.connector.connect(user='fans_buy', password='AdminNeSoset3.', host='localhost', database='fans_buy_database')

    
    def add_column(self):
        cursor = self.connection.cursor()
        cursor.execute("ALTER TABLE users ADD current_material TEXT;")
        self.connection.commit()

    # # user

    def create_users_table(self):
        cursor = self.connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS users (user_id BIGINT PRIMARY KEY, username TEXT, state TEXT, status TEXT, balance REAL, current_bot TEXT, invited_by TEXT, storage TEXT, invited_time TIMESTAMP, subscription_time TIMESTAMP, current_material TEXT);''')
        self.connection.commit()
        

    def add_user(self, user_id, username, invited_by):
        cursor = self.connection.cursor()
        state = "main_state"
        status = "user"
        balance = 0
        current_bot = None
        storage = {}
        current_material = None
        cursor.execute("INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (user_id, username, state, status, balance, current_bot, invited_by, json.dumps(storage), datetime.now(), datetime.now(), current_material, ))
        self.connection.commit()
        
    def check_if_user_exists(self, user_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = '%s';", (user_id,))
            cursor.fetchone()[0]
            return True
        except:
            return False
        
    def get_user(self, user):
        cursor = self.connection.cursor()
        if user.isdigit():
            user_id = int(user)
            cursor.execute("SELECT * FROM users WHERE user_id = '%s';", (user_id,))
            data = cursor.fetchone()
        else:
            cursor.execute("SELECT * FROM users WHERE username = %s;", (user,))
            data = cursor.fetchone()
        
        return data
    
    def get_username(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT username FROM users WHERE user_id = '%s';", (user_id,))
        data = cursor.fetchone()[0]
        return data
    
    def get_invited_by(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT invited_by FROM users WHERE user_id = '%s';", (user_id,))
        data = cursor.fetchone()[0]
        return data
        
    def get_state(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT state FROM users WHERE user_id = '%s';", (user_id,))
        data = cursor.fetchone()[0]
        return data

    def update_state(self, user_id, state):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET state = %s WHERE user_id = '%s'", (state, user_id,))
        self.connection.commit()
        
    # storage
    def get_storage(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT storage FROM users WHERE user_id = '%s';", (user_id,))
        storage = json.loads(cursor.fetchone()[0])
        
        return storage
    
    def update_storage(self, user_id, storage):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET storage = %s WHERE user_id = '%s';", (json.dumps(storage), user_id,))
        self.connection.commit()
        
    def get_current_material(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT current_material FROM users WHERE user_id = '%s';", (user_id,))
        data = cursor.fetchone()[0]
        return data

    def update_current_material(self, user_id, current_material):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET current_material = %s WHERE user_id = '%s'", (current_material, user_id,))
        self.connection.commit()
        
    def get_balance(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT balance FROM users WHERE user_id = '%s';", (user_id,))
        balance = round(cursor.fetchone()[0], 2)
        return balance
    
    def update_balance(self, user_id, balance):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET balance = %s WHERE user_id = '%s'", (balance, user_id,))
        self.connection.commit()

    def get_current_bot(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT current_bot FROM users WHERE user_id = '%s';", (user_id,))
        data = cursor.fetchone()[0]
        return data

    def update_current_bot(self, user_id, current_bot):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET current_bot = %s WHERE user_id = '%s';", (current_bot, user_id,))
        self.connection.commit()
        
    def get_all_users(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users;")
        data = cursor.fetchall()
        
        return data
    
    def get_referals_count(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE invited_by = %s;", (user_id,))
        data = cursor.fetchall()
        return data
        
    def get_today_new_users(self):
        cursor = self.connection.cursor()
        users = self.get_all_users()
        today = 0
        
        for user in users:
            cursor.execute("SELECT invited_time FROM users WHERE user_id = '%s';", (user[0],))
            invited_time = cursor.fetchone()[0]
            if datetime.now() + timedelta(days=-1) <= invited_time:
                today += 1
                
        return today
    
    def get_subscription_time(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT subscription_time FROM users WHERE user_id = '%s';", (user_id,))
        minutes = ((datetime.now() - cursor.fetchone()[0]).total_seconds() / 60) * (-1)
        
        if minutes <= 0:
            return 0
        
        return minutes
    
    def update_subscription_time(self, user_id, premium_duration):
        cursor = self.connection.cursor()
        cursor.execute("SELECT subscription_time FROM users WHERE user_id = '%s';", (user_id,))
        subscription_time = cursor.fetchone()[0]
        
        if subscription_time < datetime.now():
            new_subscription_time = datetime.now() + timedelta(days=premium_duration*30)
        else:
            new_subscription_time = subscription_time + timedelta(days=premium_duration*30)
            
            
        cursor.execute("UPDATE users SET subscription_time = %s WHERE user_id = '%s'", (new_subscription_time, user_id,))
        self.connection.commit()
    
    def get_all_users_with_premium(self):
        users = self.get_all_users()
        premium_users = 0
        
        for user in users:
            sub_time = self.get_subscription_time(user[0])
            
            if sub_time > 0:
                premium_users += 1
        
        
        return premium_users
    
    
    
    
    
    # # bot information
    
    def drop_bot_information(self):
        cursor = self.connection.cursor()
        cursor.execute(f'''DROP TABLE bot_information;''')
        self.connection.commit()
        
    def create_bot_information_table(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f'''CREATE TABLE bot_information (commission_percentage INT, referal_bonus INT, referal_bonus_in_user_bot INT, start_referal_sum REAL);''')
            self.connection.commit()
            cursor.execute("INSERT INTO bot_information VALUES (%s, %s, %s, %s)", (15, 10, 5, 20))
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
        cursor.execute("UPDATE bot_information SET commission_percentage = %s;", (percentage,))
        self.connection.commit()
        
    def get_referal_bonus(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT referal_bonus FROM bot_information;")
        data = cursor.fetchone()[0]
        return data
    
    def update_referal_bonus(self, percentage):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE bot_information SET referal_bonus = %s;", (percentage,))
        self.connection.commit()
        
    def get_referal_bonus_in_user_bot(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT referal_bonus_in_user_bot FROM bot_information;")
        data = cursor.fetchone()[0]
        return data
    
    def update_referal_bonus_in_user_bot(self, percentage):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE bot_information SET referal_bonus_in_user_bot = %s;", (percentage,))
        self.connection.commit()
    
    def get_start_referal_sum_in_user_bot(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT start_referal_sum FROM bot_information;")
        data = cursor.fetchone()[0]
        return data
    
    def update_start_referal_sum_in_user_bot(self, sum):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE bot_information SET start_referal_sum = %s;", (sum,))
        self.connection.commit()
        
        
        
        
    # # user_bot table
    
    def create_users_bots_table(self):
        cursor = self.connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS users_bots (bot_username TEXT, token TEXT, created_by_id BIGINT, created_by_username TEXT, created_time TIMESTAMP, photo_price REAL, video_price REAL, referal_sum REAL, invited_ref_sum REAL);''')
        self.connection.commit()
        
    def add_new_bot(self, bot_username, token, created_by_id, created_by_username):
        created_time = datetime.now()
        photo_price = 10
        video_price = 10
        referal_sum = 20
        invited_ref_sum = 20
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO users_bots VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (bot_username, token, created_by_id, created_by_username, created_time, photo_price, video_price, referal_sum, invited_ref_sum, ))
        self.connection.commit()
        
    def delete_user_bot(self, bot_username):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM users_bots WHERE bot_username = %s;", (bot_username, ))
        self.connection.commit()
        
    def get_bot_referal_sum(self, bot_username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT referal_sum FROM users_bots WHERE bot_username = %s;", (bot_username,))
        data = cursor.fetchone()[0]
        
        return data

    def update_bot_referal_sum(self, bot_username, referal_sum):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users_bots SET referal_sum = %s WHERE bot_username = %s", (referal_sum, bot_username,))
        self.connection.commit()
        
    def get_bot_invited_ref_sum(self, bot_username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT invited_ref_sum FROM users_bots WHERE bot_username = %s;", (bot_username,))
        data = cursor.fetchone()[0]
        
        return data

    def update_bot_invited_ref_sum(self, bot_username, invited_ref_sum):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users_bots SET invited_ref_sum = %s WHERE bot_username = %s", (invited_ref_sum, bot_username,))
        self.connection.commit()
        
    def get_bot_token(self, bot_username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT token FROM users_bots WHERE bot_username = %s;", (bot_username,))
        data = cursor.fetchone()[0]
        
        return data
    
    def get_user_bot(self, bot_username):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users_bots WHERE bot_username = %s;", (bot_username,))
            data = cursor.fetchone()
        except:
            return None
        
        return data
        
    def get_user_bot_created_by_id(self, bot_username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT created_by_id FROM users_bots WHERE bot_username = %s;", (bot_username,))
        data = cursor.fetchone()[0]
        
        return data
    
    def get_user_bot_created_by_username(self, bot_username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT created_by_username FROM users_bots WHERE bot_username = %s;", (bot_username,))
        data = cursor.fetchone()[0]
        
        return data
    
    def get_user_bots(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users_bots WHERE created_by_id = %s;", (user_id,))
        data = cursor.fetchall()
        
        return data
        
    def get_all_users_bots(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users_bots;")
        data = cursor.fetchall()
        
        return data
        
    def get_user_bot_created_time(self, bot_username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT created_time FROM users_bots WHERE bot_username = %s;", (bot_username,))
        data = cursor.fetchone()[0]
        created_time = data.strftime("%d.%m.%Y %H:%M:%S")
        
        return created_time
        
        
    def get_user_bot_photo_price(self, bot_username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT photo_price FROM users_bots WHERE bot_username = %s;", (bot_username,))
        data = cursor.fetchone()[0]
        
        return data
    
    def update_user_bot_photo_price(self, bot_username, price):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users_bots SET photo_price = %s WHERE bot_username = %s", (price, bot_username,))
        self.connection.commit()
        
        
    def get_user_bot_video_price(self, bot_username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT video_price FROM users_bots WHERE bot_username = %s;", (bot_username,))
        data = cursor.fetchone()[0]
        
        return data
    
    def update_user_bot_video_price(self, bot_username, price):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users_bots SET video_price = %s WHERE bot_username = %s", (price, bot_username,))
        self.connection.commit()
        
    def get_today_new_bots(self):
        user_bots = self.get_all_users_bots()
        total = 0
        
        for user_bot in user_bots:
            bot_username = user_bot[0]
            created_time = self.get_user_bot_created_time(bot_username)

            if datetime.now() + timedelta(days=-1) <= parse(created_time):
                total += 1
                
        return total
    
    def get_today_users_user_bots(self):
        user_bots = self.get_all_users_bots()
        today = 0
        
        for user_bot in user_bots:
            bot_username = user_bot[0]
            for user in self.get_subscriptions_from_user_bot(bot_username):
                if datetime.now() + timedelta(days=-1) <= user[1]:
                    today += 1
                
        return today
        
    
    
    
    
    # # transactions
    
    def create_transactions_table(self):
        cursor = self.connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS transactions (user_id BIGINT, bot_username TEXT, date TIMESTAMP, sum REAL);''')
        self.connection.commit()
        
    def add_new_transaction(self, user_id, bot_username, sum):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO transactions VALUES (%s, %s, %s, %s)", (user_id, bot_username, datetime.now(), sum, ))
        self.connection.commit()  
        
    def get_transactions(self, bot_username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM transactions WHERE bot_username = %s;", (bot_username,))
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
                transaction_date = transaction[2]
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
                reg_date = bot_user[1]
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
                transaction_date = transaction[2]
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
                reg_date = bot_user[1]
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
                transaction_date = transaction[2]
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
                reg_date = bot_user[1]
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
        cursor.execute("INSERT INTO withdrawal_requests VALUES (%s, %s, %s, %s, %s, %s, %s)", (withdrawal_id, user_id, sum, datetime.now(), "incomplete", wallet_type, wallet_number, ))
        self.connection.commit()
        
    def get_withdrawal_requests(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM withdrawal_requests ORDER BY status DESC;")
        data = cursor.fetchall()
        
        return data
    
    def get_withdrawal_request(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM withdrawal_requests WHERE id = %s;", (id, ))
        data = cursor.fetchone()
        
        return data
    
    def update_withdrawal_request_status(self, id):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE withdrawal_requests SET status = %s WHERE id = %s;", ("complete", id, ))
        self.connection.commit()
        
    def get_withdrawal_request_status(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT status FROM withdrawal_requests WHERE id = %s;", (id, ))
        data = cursor.fetchone()[0]
        
        return data
    
    
    # # replenishment
    
    def create_replenishment_table(self):
        cursor = self.connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS replenishment (user_id BIGINT, sum REAL, time TIMESTAMP);''')
        self.connection.commit()
        
    def add_new_replenishment(self, user_id, sum):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO replenishment VALUES (%s, %s, %s)", (user_id, sum, datetime.now(), ))
        self.connection.commit()
    
    def get_total_replenishment(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT sum FROM replenishment;")
        data = cursor.fetchall()
        total_replenishment = 0
        
        for sum in data:
            total_replenishment += sum[0]
            
        return total_replenishment
    
    def get_today_replenishment(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM replenishment;")
        data = cursor.fetchall()
        today = 0
        
        for rep in data:
            sum = int(rep[1])
            time = rep[2]

            if datetime.now() + timedelta(days=-1) <= time:
                today += sum
                
        return today
    
    
    
    
    
    # # materials
    
    def create_materials_table(self):
        cursor = self.connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS materials_table (filename TEXT, file_type TEXT, bot_username TEXT, viewed_users TEXT);''')
        self.connection.commit()
    
    def add_material(self, filename, file_type, bot_username):
        viewed_users = []
        my_cursor = self.connection.cursor()
        my_cursor.execute("INSERT INTO materials_table VALUES (%s, %s, %s, %s)", (filename, file_type, bot_username, json.dumps(viewed_users), ))
        self.connection.commit()
        
    def get_all_filenames(self, file_type):
        cursor = self.connection.cursor()
        cursor.execute("SELECT filename FROM materials_table WHERE file_type = %s;", (file_type, ))
        data = cursor.fetchall()
        
        return data
    
    def get_bot_photos(self, bot_username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT filename FROM materials_table WHERE bot_username = %s AND file_type = 'photo';", (bot_username,))
        data = cursor.fetchall()
        
        return data
    
    def get_bot_videos(self, bot_username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT filename FROM materials_table WHERE bot_username = %s AND file_type = 'video';", (bot_username,))
        data = cursor.fetchall()
        
        return data
    
    def delete_photo(self, filename):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM materials_table WHERE filename = %s AND file_type = 'photo';", (filename, ))
        self.connection.commit()
        
    def delete_video(self, filename):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM materials_table WHERE filename = %s AND file_type = 'video';", (filename, ))
        self.connection.commit()
        
    def get_total_bots_photos(self, user_id):
        user_bots = self.get_user_bots(user_id)
        total_images = 0
        
        for user_bot in user_bots:
            bot_username = user_bot[0]
            images = len(self.get_bot_photos(bot_username))
            total_images += images
                
        return total_images
    
    def get_total_bots_videos(self, user_id):
        user_bots = self.get_user_bots(user_id)
        total_videos = 0
        
        for user_bot in user_bots:
            bot_username = user_bot[0]
            videos = len(self.get_bot_videos(bot_username))
            total_videos += videos
                
        return total_videos
    
    def get_viewed_users_on_photo(self, filename):
        cursor = self.connection.cursor()
        cursor.execute("SELECT viewed_users FROM materials_table WHERE filename = %s AND file_type = 'photo';", (filename, ))
        data = json.loads(cursor.fetchone()[0])
        
        return data
        
    def update_viewed_users_on_photo(self, filename, viewed_users):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE materials_table SET viewed_users = %s WHERE filename = %s AND file_type = 'photo';", (json.dumps(viewed_users), filename, ))
        self.connection.commit()
        
    def get_viewed_users_on_video(self, filename):
        cursor = self.connection.cursor()
        cursor.execute("SELECT viewed_users FROM materials_table WHERE filename = %s AND file_type = 'video';", (filename, ))
        data = json.loads(cursor.fetchone()[0])
        
        return data
        
    def update_viewed_users_on_video(self, filename, viewed_users):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE materials_table SET viewed_users = %s WHERE filename = %s AND file_type = 'video';", (json.dumps(viewed_users), filename, ))
        self.connection.commit()
        
    def get_photo_info(self, filename):
        cursor = self.connection.cursor()
        cursor.execute("SELECT bot_username FROM materials_table WHERE filename = %s AND file_type = 'photo';", (filename, ))
        data = cursor.fetchone()[0]
        
        return data
    
    def get_video_info(self, filename):
        cursor = self.connection.cursor()
        cursor.execute("SELECT bot_username FROM materials_table WHERE filename = %s AND file_type = 'video';", (filename, ))
        data = cursor.fetchone()[0]
        
        return data




    # # user_bot
    
    def create_bot_table(self, bot_username):
        cursor = self.connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {bot_username} (user_id BIGINT PRIMARY KEY, username TEXT, reg_date TIMESTAMP, state TEXT, balance REAL, invited_by TEXT, referal_balance REAL);''')
        self.connection.commit()
        
    def add_new_user_in_user_bot(self, bot_username, user_id, username, invited_by):
        cursor = self.connection.cursor()
        reg_date = datetime.now()
        state = "main_state"
        balance = 0
        referal_balance = self.get_bot_referal_sum(bot_username)
        cursor.execute(f"INSERT INTO {bot_username} VALUES (%s, %s, %s, %s, %s, %s, %s);", (user_id, username, reg_date, state, balance, str(invited_by), referal_balance, ))
        self.connection.commit()
        
    def check_if_user_exists_in_user_bot(self, bot_username, user_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM {bot_username} WHERE user_id = '%s';", (user_id,))
            cursor.fetchone()[0]
            return True
        except Exception:
            return False
        
    def get_user_from_user_bot(self, bot_username, user):
        cursor = self.connection.cursor()
        if str(user).isdigit():
            user_id = int(user)
            cursor.execute(f"SELECT * FROM {bot_username} WHERE user_id = '%s';", (user_id,))
            data = cursor.fetchone()
        else:
            cursor.execute(f"SELECT * FROM {bot_username} WHERE username = %s;", (user,))
            data = cursor.fetchone()
        
        return data
    
    def get_users_from_bot(self, bot_username):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT user_id FROM {bot_username};")
        data = cursor.fetchall()
        
        return data
        
    def get_subscriptions_from_user_bot(self, bot_username):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT user_id, reg_date FROM {bot_username};")
        data = cursor.fetchall()
        return data
    
    def get_username_from_user_bot(self, bot_username, user_id):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT username FROM {bot_username} WHERE user_id = '%s';", (user_id,))
        data = cursor.fetchone()[0]
        return data
    
    def get_state_from_user_bot(self, bot_username, user_id):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT state FROM {bot_username} WHERE user_id = '%s';", (user_id,))
        data = cursor.fetchone()[0]
        return data

    def update_state_from_user_bot(self, bot_username, user_id, state):
        cursor = self.connection.cursor()
        cursor.execute(f"UPDATE {bot_username} SET state = %s WHERE user_id = '%s'", (state, user_id, ))
        self.connection.commit()
    
    def get_balance_from_user_bot(self, bot_username, user_id):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT balance FROM {bot_username} WHERE user_id = '%s';", (user_id,))
        data = round(cursor.fetchone()[0], 2)
        return data

    def update_balance_from_user_bot(self, bot_username, user_id, balance):
        cursor = self.connection.cursor()
        cursor.execute(f"UPDATE {bot_username} SET balance = %s WHERE user_id = '%s'", (balance, user_id, ))
        self.connection.commit()
        
    def get_referal_balance_from_user_bot(self, bot_username, user_id):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT referal_balance FROM {bot_username} WHERE user_id = '%s';", (user_id,))
        data = round(cursor.fetchone()[0], 2)
        return data

    def update_referal_balance_from_user_bot(self, bot_username, user_id, balance):
        cursor = self.connection.cursor()
        cursor.execute(f"UPDATE {bot_username} SET referal_balance = %s WHERE user_id = '%s'", (balance, user_id, ))
        self.connection.commit()
        
    def get_invited_by_from_user_bot(self, bot_username, user_id):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT invited_by FROM {bot_username} WHERE user_id = '%s';", (user_id,))
        data = cursor.fetchone()[0]
        return data
        
    def get_invited_users_from_user_bot(self, bot_username, user_id):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT invited_by FROM {bot_username} WHERE invited_by = %s;", (user_id, ))
        data = len(cursor.fetchall())
        return data

    def get_len_users_in_user_bots(self):
        user_bots = self.get_all_users_bots()
        users = 0
        for user_bot in user_bots:
            bot_username = user_bot[0]
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT user_id FROM {bot_username};")
            data = len(cursor.fetchall())
            users += data

        return users




# yoomoney labels

    def create_yoomoney_labels_table(self):
        cursor = self.connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS yoomoney_labels (label TEXT);''')
        self.connection.commit()

    def add_label(self, label):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO yoomoney_labels VALUES (%s)", (label, ))
        self.connection.commit()
        
    def get_all_labels(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT label FROM yoomoney_labels;")
        data = cursor.fetchall()
        
        return data
