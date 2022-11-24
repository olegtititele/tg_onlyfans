import json
import sqlite3
import mysql.connector
import binascii
import os
from dateutil.parser import parse
# from datetime import datetime, timedelta

# from dateutil.parser import parse


class DB():

    def __init__(self):
        self.connection = sqlite3.connect("database.db")
        self.my_connection = mysql.connector.connect(user='fans_buy', password='AdminNeSoset3.', host='localhost', database='fans_buy_database')
    
    def create_users_table(self):
        cursor = self.my_connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS users (user_id BIGINT PRIMARY KEY, username TEXT, state TEXT, status TEXT, balance REAL, current_bot TEXT, invited_by TEXT, storage TEXT, invited_time TIMESTAMP, subscription_time TIMESTAMP);''')
        self.my_connection.commit()
        
    def users(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT user_id, username, state, status, balance, current_bot, invited_by, storage, invited_time, subscription_time FROM users;")
        data = cursor.fetchall()
        
        for user in data:
            user_id = user[0]
            print(user_id)
            username = user[1]
            state = user[2]
            status = user[3]
            balance = user[4]
            current_bot = user[5]
            invited_by = user[6]
            storage = user[7]
            invited_time = user[8]
            subscription_time = user[9]
           
           
            my_cursor = self.my_connection.cursor()
            my_cursor.execute("INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (user_id, username, state, status, balance, current_bot, invited_by, json.dumps(storage), invited_time, subscription_time, ))
            self.my_connection.commit()
            
            
            
    #####################################   
    def generate_random_id(self, material_list):
        while True:
            id = binascii.b2a_hex(os.urandom(25)).decode()
            
            if id not in material_list:
                return id
            
    def photos(self):
        cursor = self.connection.cursor()
        cursor.execute(f'''SELECT * FROM photos_table;''')
        photos = cursor.fetchall()

        for photo in photos:
            material = photo[0]
            bot_username = photo[1]
            viewed_users = photo[2]
            while True:
                filename = binascii.b2a_hex(os.urandom(25)).decode()
                
                if filename not in self.get_all_filenames('photo'):
                    break

            img_option = open(f'materials/photos/{filename}.jpg', 'wb')
            img_option.write(material)
            
            self.add_material(filename, "photo", bot_username, viewed_users)
            
    def videos(self):
        cursor = self.connection.cursor()
        cursor.execute(f'''SELECT * FROM videos_table;''')
        videos = cursor.fetchall()

        for video in videos:
            material = video[0]
            bot_username = video[1]
            viewed_users = video[2]
            while True:
                filename = binascii.b2a_hex(os.urandom(25)).decode()
                
                if filename not in self.get_all_filenames('video'):
                    break

            img_option = open(f'materials/videos/{filename}.mp4', 'wb')
            img_option.write(material)
            
            self.add_material(filename, "video", bot_username, viewed_users)
        
        
        
    def create_materials_table(self):
        cursor = self.my_connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS materials_table (filename TEXT, file_type TEXT, bot_username TEXT, viewed_users TEXT);''')
        self.my_connection.commit()
    
    def add_material(self, filename, file_type, bot_username, viewed_users):
        my_cursor = self.my_connection.cursor()
        my_cursor.execute("INSERT INTO materials_table VALUES (%s, %s, %s, %s)", (filename, file_type, bot_username, json.dumps(viewed_users), ))
        self.my_connection.commit()
        
    def get_all_filenames(self, file_type):
        cursor = self.my_connection.cursor()
        cursor.execute("SELECT filename FROM materials_table WHERE file_type = %s;", (file_type, ))
        data = cursor.fetchall()
        
        return data
    #########################
    
    def create_users_bots_table(self):
        cursor = self.my_connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS users_bots (bot_username TEXT, token TEXT, created_by_id BIGINT, created_by_username TEXT, created_time TIMESTAMP, photo_price REAL, video_price REAL, referal_sum REAL);''')
        self.my_connection.commit()
        
    def add_user_bots(self):
        cursor = self.connection.cursor()
        cursor.execute(f'''SELECT * FROM users_bots;''')
        data = cursor.fetchall()
        
        for bot in data:
            bot_username = bot[0]
            print(bot_username)
            token = bot[1]
            created_by_id = bot[2]
            created_by_username = bot[3]
            created_time = bot[4]
            photo_price = bot[5]
            video_price = bot[6]
            
            my_cursor = self.my_connection.cursor()
            my_cursor.execute("INSERT INTO users_bots VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (bot_username, token, created_by_id, created_by_username, created_time, photo_price, video_price, 20, ))
            self.my_connection.commit()
    #########################
    
    def create_transactions_table(self):
        cursor = self.my_connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS transactions (user_id BIGINT, bot_username TEXT, date TIMESTAMP, sum REAL);''')
        self.my_connection.commit()
    
    
    def add_transactions(self):
        cursor = self.connection.cursor()
        cursor.execute(f'''SELECT * FROM transactions;''')
        data = cursor.fetchall()
        
        for transaction in data:
            user_id = transaction[0]
            print(user_id)
            bot_username = transaction[1]
            date = parse(transaction[2])
            sum = transaction[3]
            
            my_cursor = self.my_connection.cursor()
            my_cursor.execute("INSERT INTO transactions VALUES (%s, %s, %s, %s)", (user_id, bot_username, date, sum, ))
            self.my_connection.commit()
    ###########################
    
    
    def create_withdrawal_requests_table(self):
        cursor = self.my_connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS withdrawal_requests (id BIGINT, user_id BIGINT, sum REAL, date TIMESTAMP, status TEXT, wallet_type TEXT, wallet_number TEXT);''')
        self.my_connection.commit()
        
    def add_withdrawal_requests(self):
        cursor = self.connection.cursor()
        cursor.execute(f'''SELECT * FROM withdrawal_requests;''')
        data = cursor.fetchall()
        
        for w_r in data:
            id = w_r[0]
            user_id = w_r[1]
            sum = w_r[2]
            date = parse(w_r[3])
            status = w_r[4]
            wallet_type = w_r[5]
            wallet_number = w_r[6]
            print(wallet_number)
            
            my_cursor = self.my_connection.cursor()
            my_cursor.execute("INSERT INTO withdrawal_requests VALUES (%s, %s, %s, %s, %s, %s, %s)", (id, user_id, sum, date, status, wallet_type, wallet_number, ))
            self.my_connection.commit()
    #######################
    
    def create_replenishment_table(self):
        cursor = self.my_connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS replenishment (user_id BIGINT, sum REAL, time TIMESTAMP);''')
        self.my_connection.commit()
        
    
    def add_replenishments(self):
        cursor = self.connection.cursor()
        cursor.execute(f'''SELECT * FROM replenishment;''')
        data = cursor.fetchall()
        
        for rep in data:
            user_id = rep[0]
            sum = rep[1]
            print(sum)
            time = parse(rep[2])
            
            my_cursor = self.my_connection.cursor()
            my_cursor.execute("INSERT INTO replenishment VALUES (%s, %s, %s)", (user_id, sum, time, ))
            self.my_connection.commit()
    #########################
    
    def user_bots_info(self):
        cursor = self.connection.cursor()
        cursor.execute(f'''SELECT bot_username FROM users_bots;''')
        data = cursor.fetchall()
        
        for bot in data:
            my_cursor = self.my_connection.cursor()
            my_cursor.execute(f'''CREATE TABLE IF NOT EXISTS {bot[0]} (user_id BIGINT PRIMARY KEY, username TEXT, reg_date TIMESTAMP, state TEXT, balance REAL, invited_by TEXT, referal_balance REAL);''')
            self.my_connection.commit()
            
            cursor = self.connection.cursor()
            cursor.execute(f'''SELECT * FROM {bot[0]};''')
            data = cursor.fetchall()
        
            for user in data:
                user_id = user[0]
                print(user_id)
                username = user[1]
                reg_date = parse(user[2])
                state = user[3]
                balance = user[4]
                invited_by = user[5]
                referal_balance = user[6]
                
                
                my_cursor = self.my_connection.cursor()
                my_cursor.execute(f"INSERT INTO {bot[0]} VALUES (%s, %s, %s, %s, %s, %s, %s)", (user_id, username, reg_date, state, balance, invited_by, referal_balance, ))
                self.my_connection.commit()
    ##############################
    
    
    def create_yoomoney_labels_table(self):
        cursor = self.my_connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS yoomoney_labels (label TEXT);''')
        self.my_connection.commit()
        
    def add_labels(self):
        cursor = self.connection.cursor()
        cursor.execute(f'''SELECT label FROM yoomoney_labels;''')
        data = cursor.fetchall()
        
        for label in data:
            print(label[0])
            my_cursor = self.my_connection.cursor()
            my_cursor.execute("INSERT INTO yoomoney_labels VALUES (%s)", (label[0], ))
            self.my_connection.commit()
    
        
        
        
        
if __name__ == "__main__":
    db = DB()
    db.create_users_table()
    db.create_materials_table()
    db.create_users_bots_table()
    db.create_transactions_table()
    db.create_withdrawal_requests_table()
    db.create_replenishment_table()
    db.create_yoomoney_labels_table()
    
    db.users()
    db.photos()
    db.videos()
    db.add_replenishments()
    db.add_withdrawal_requests()
    db.add_transactions()
    db.add_user_bots()
    db.user_bots_info()
    db.add_labels()
