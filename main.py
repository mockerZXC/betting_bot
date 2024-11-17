# Стандартные библиотеки
import os
import logging
from threading import Thread

# Внешние библиотеки
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask, request

# Локальные импорты
from config.config import REFERRAL_LINK, PROMO_CODE, TOKEN
from database.db_manager import DBManager
from config.languages import LANGUAGES

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и базы данных
app = Flask(__name__)
bot = telebot.TeleBot(TOKEN)
db = DBManager('bot_database.db')

def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
    return wrapper

@app.route('/webhook', methods=['POST'])
@error_handler
def webhook():
    data = request.json
    status_mapping = {
        'click': 'clicked',
        'register': 'registered',
        'deposit': 'deposited'
    }
    if data['type'] in status_mapping:
        update_referral_status(data['user_id'], status_mapping[data['type']])
    return 'OK', 200

@error_handler
def update_referral_status(user_id, status):
    db.update_user_status(user_id, status)
    lang = db.get_user_language(user_id)
    if status == 'deposited':
        bot.send_message(user_id, LANGUAGES[lang]['deposit_confirmed'])

@bot.message_handler(commands=['start'])
@error_handler
def start(message):
    username = message.from_user.username or message.from_user.first_name
    welcome_text = f"👋 Hello, {username}!"
    markup = InlineKeyboardMarkup(row_width=3)
    btn_ua = InlineKeyboardButton("🇺🇦 Українська", callback_data='lang_ua')
    btn_en = InlineKeyboardButton("🇺🇸 English", callback_data='lang_en')
    btn_ru = InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru')
    markup.add(btn_ua, btn_en, btn_ru)
    bot.send_message(message.chat.id, welcome_text)
    bot.send_message(message.chat.id, "🌍 Choose your language:", reply_markup=markup)

@error_handler
def show_menu(chat_id, lang):
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        ('registration_button', 'registration'),
        ('forecast_button', 'forecast'),
        ('profile_button', 'profile'),
        ('instruction_button', 'instruction')
    ]
    for text_key, callback_data in buttons:
        markup.add(InlineKeyboardButton(
            LANGUAGES[lang][text_key], 
            callback_data=callback_data
        ))
    bot.send_message(
        chat_id,
        LANGUAGES[lang]['choose_action'],
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
@error_handler
def language_callback(call):
    user_id = call.from_user.id
    lang = call.data.split('_')[1]
    db.set_user_language(user_id, lang)
    bot.answer_callback_query(call.id, text=LANGUAGES[lang]['language_selected'])
    show_menu(call.message.chat.id, lang)

@bot.callback_query_handler(func=lambda call: call.data == 'registration')
@error_handler
def registration_callback(call):
    user_id = call.from_user.id
    lang = db.get_user_language(user_id)
    if not db.is_user_registered(user_id):
        registration_text = LANGUAGES[lang]['registration_link'].format(
            link=REFERRAL_LINK,
            promo_code=PROMO_CODE
        )
        bot.send_message(call.message.chat.id, registration_text)
    else:
        bot.send_message(call.message.chat.id, LANGUAGES[lang]['already_registered'])
logging.basicConfig(level=logging.DEBUG)

def registration_callback(call):
    try:
        logging.debug(f"Registration callback started for user {call.from_user.id}")
        # Ваш код здесь
        logging.debug(f"Registration link: {REFERRAL_LINK}")
        bot.send_message(call.message.chat.id, f"Вот ваша ссылка для регистрации: {REFERRAL_LINK}")
    except Exception as e:
        logging.error(f"Error in registration_callback: {e}", exc_info=True)
if __name__ == '__main__':
    try:
        logger.info("Bot starting...")
        bot.polling(none_stop=True)
    except Exception as e:
        logger.critical(f"Critical error: {e}", exc_info=True)