from telebot import types
from config.languages import LANGUAGES  

def start_command(message, bot):
    user_id = message.from_user.id
    username = message.from_user.first_name
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    btn_ru = types.InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru')
    btn_ua = types.InlineKeyboardButton("🇺🇦 Українська", callback_data='lang_ua')
    btn_en = types.InlineKeyboardButton("🇬🇧 English", callback_data='lang_en')
    
    markup.add(btn_ru, btn_ua, btn_en)
    
    bot.send_message(
        message.chat.id,
        LANGUAGES['en']['welcome'].format(username=username),
        reply_markup=markup
    )