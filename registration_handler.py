from telebot import types
from config import REFERRAL_LINK, PROMO_CODE, LANGUAGES

def send_registration_message(bot, chat_id, language):
    """
    Отправляет сообщение с реферальной ссылкой и промокодом
    """
    markup = types.InlineKeyboardMarkup()
    register_button = types.InlineKeyboardButton(
        text=LANGUAGES[language]['registration_button'],
        url=REFERRAL_LINK
    )
    markup.add(register_button)

    # Формируем текст сообщения с реферальной ссылкой и промокодом
    message_text = (
        f"{LANGUAGES[language]['registration_info']}\n\n"
        f"🔗 {REFERRAL_LINK}\n"
        f"🎁 {LANGUAGES[language]['promo_code']}: {PROMO_CODE}"
    )

    bot.send_message(
        chat_id=chat_id,
        text=message_text,
        reply_markup=markup,
        parse_mode='HTML'
    )