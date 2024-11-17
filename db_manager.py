import sqlite3
from datetime import datetime
import logging
import atexit
from typing import Tuple

class DBManager:
    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def is_user_registered(self, user_id):
        self.cursor.execute("SELECT is_registered FROM users WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else False

    def create_tables(self):
        try:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                language TEXT DEFAULT 'ru',
                registration_date TIMESTAMP,
                is_registered BOOLEAN DEFAULT FALSE,
                has_deposit BOOLEAN DEFAULT FALSE
            )
            ''')
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS stats (
                user_id INTEGER PRIMARY KEY,
                games_played INTEGER DEFAULT 0,
                games_won INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
            ''')
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS referrals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                referrer_id INTEGER,
                clicked BOOLEAN DEFAULT FALSE,
                registered BOOLEAN DEFAULT FALSE,
                deposited BOOLEAN DEFAULT FALSE,
                click_date TIMESTAMP,
                register_date TIMESTAMP,
                deposit_date TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (referrer_id) REFERENCES users(user_id)
            )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Ошибка при создании таблиц: {e}")
            self.conn.rollback()

    def add_user(self, user_id: int, username: str):
        try:
            self.cursor.execute('INSERT OR IGNORE INTO users (user_id, username, registration_date) VALUES (?, ?, CURRENT_TIMESTAMP)', (user_id, username))
            self.cursor.execute('INSERT OR IGNORE INTO stats (user_id) VALUES (?)', (user_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Ошибка при добавлении пользователя: {e}")
            self.conn.rollback()

    def get_user_language(self, user_id: int) -> str:
        try:
            self.cursor.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
            result = self.cursor.fetchone()
            return result[0] if result else 'ru'
        except sqlite3.Error as e:
            logging.error(f"Ошибка при получении языка пользователя: {e}")
            return 'en'

    def set_user_language(self, user_id: int, language: str):
        try:
            self.cursor.execute('UPDATE users SET language = ? WHERE user_id = ?', (language, user_id))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Ошибка при установке языка пользователя: {e}")
            self.conn.rollback()


    def update_user_stats(self, user_id: int, game_won: bool):
        try:
            self.cursor.execute('UPDATE stats SET games_played = games_played + 1, games_won = games_won + ? WHERE user_id = ?', (int(game_won), user_id))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Ошибка при обновлении статистики пользователя: {e}")
            self.conn.rollback()

    def get_user_stats(self, user_id: int) -> Tuple[int, int]:
        try:
            self.cursor.execute('SELECT games_played, games_won FROM stats WHERE user_id = ?', (user_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(f"Ошибка при получении статистики пользователя: {e}")
            return (0, 0)

    def update_user_status(self, user_id: int, status_type: str, value: bool):
        try:
            if status_type == 'registration':
                self.cursor.execute('UPDATE users SET is_registered = ? WHERE user_id = ?', (value, user_id))
            elif status_type == 'deposit':
                self.cursor.execute('UPDATE users SET has_deposit = ? WHERE user_id = ?', (value, user_id))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Ошибка при обновлении статуса пользователя: {e}")
            self.conn.rollback()

    def get_user_status(self, user_id: int) -> dict:
        try:
            self.cursor.execute('SELECT is_registered, has_deposit FROM users WHERE user_id = ?', (user_id,))
            result = self.cursor.fetchone()
            return {
                'is_registered': result[0] if result else False,
                'has_deposit': result[1] if result else False
            }
        except sqlite3.Error as e:
            logging.error(f"Ошибка при получении статуса пользователя: {e}")
            return {'is_registered': False, 'has_deposit': False}

    def add_referral(self, user_id: int, referrer_id: int):
        try:
            self.cursor.execute('''
                INSERT INTO referrals (user_id, referrer_id) 
                VALUES (?, ?)
            ''', (user_id, referrer_id))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Ошибка при добавлении реферала: {e}")
            self.conn.rollback()

    def get_referral_stats(self, referrer_id: int) -> dict:
        try:
            self.cursor.execute('''
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN registered THEN 1 ELSE 0 END) as registered,
                    SUM(CASE WHEN deposited THEN 1 ELSE 0 END) as deposited
                FROM referrals 
                WHERE referrer_id = ?
            ''', (referrer_id,))
            result = self.cursor.fetchone()
            return {
                'total': result[0],
                'registered': result[1],
                'deposited': result[2]
            }
        except sqlite3.Error as e:
            logging.error(f"Ошибка при получении статистики рефералов: {e}")
            return {'total': 0, 'registered': 0, 'deposited': 0}

    def update_referral_status(self, user_id, status):
        try:
            if status == 'clicked':
                self.cursor.execute('UPDATE referrals SET clicked = TRUE, click_date = ? WHERE user_id = ?', (datetime.now(), user_id))
            elif status == 'registered':
                self.cursor.execute('UPDATE referrals SET registered = TRUE, register_date = ? WHERE user_id = ?', (datetime.now(), user_id))
            elif status == 'deposited':
                self.cursor.execute('UPDATE referrals SET deposited = TRUE, deposit_date = ? WHERE user_id = ?', (datetime.now(), user_id))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Ошибка при обновлении статуса реферала: {e}")
            self.conn.rollback()

    def close(self):
        self.conn.close()

# Создаем глобальный экземпляр DBManager
db = DBManager('bot_database.db')

# Вспомогательные функции для работы с базой данных
def get_user_language(user_id: int) -> str:
    return db.get_user_language(user_id)

def set_user_language(user_id: int, language: str):
    db.set_user_language(user_id, language)

def add_user(user_id: int, username: str):
    db.add_user(user_id, username)

def update_user_stats(user_id: int, game_won: bool):
    db.update_user_stats(user_id, game_won)

def get_user_stats(user_id: int) -> Tuple[int, int]:
    return db.get_user_stats(user_id)

def update_user_status(user_id: int, status_type: str, value: bool):
    db.update_user_status(user_id, status_type, value)

def get_user_status(user_id: int) -> dict:
    return db.get_user_status(user_id)

def add_referral(user_id: int, referrer_id: int):
    db.add_referral(user_id, referrer_id)

def get_referral_stats(referrer_id: int) -> dict:
    return db.get_referral_stats(referrer_id)

def update_referral_status(user_id: int, status: str):
    db.update_referral_status(user_id, status)

def close(self):
        if self.conn:
            self.conn.close()

db = DBManager('bot_database.db')

atexit.register(db.close)