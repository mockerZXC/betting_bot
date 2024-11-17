import os
from dotenv import load_dotenv
load_dotenv()

# Основные настройки бота
MAIN_BOT_TOKEN = os.getenv('MAIN_BOT_TOKEN', '7902272485:AAGmEYDGsAXb1kkdGNYKhJQBGqnR4XCatpw')
TRACKING_BOT_TOKEN = os.getenv('TRACKING_BOT_TOKEN', '7835033607:AAF3A67roK9Qtd7RXLTOLS0udijd7jROlVA')
ADMIN_IDS = [int(id) for id in os.getenv('ADMIN_IDS', '5060688161').split(',')]
CHAT_ID = '-1002383704511'

# Реферальная система
REFERRAL_LINK = 'https://1wzvro.top/v3/aggressive-casino?p=8vwc'
PROMO_CODE = 'funtop'

# Пути к ресурсам
IMAGES_PATHS = {
    'luckyjet': 'resources/images/luckyjet/',
    'mines': 'resources/images/mines/'
}

# Настройки изображений
IMAGE_EXTENSIONS = {
    'luckyjet': '.jpg',
    'mines': '.jpg'
}

# Файлы данных
MULTIPLIERS_FILE = 'data/luckyjet_coefficients.json'

# Языковые настройки
DEFAULT_LANGUAGE = 'en'
ALLOWED_LANGUAGES = ['ru', 'ua', 'en']

# Webhook URLs
BASE_WEBHOOK_URL = f'https://api.telegram.org/bot7835033607:AAF3A67roK9Qtd7RXLTOLS0udijd7jROlVA/sendMessage?chat_id={CHAT_ID}&text='
WEBHOOK_URLS = {
    'registration': BASE_WEBHOOK_URL + 'Игрок:+{user_id}+Зарегистрировался+ГЕО:+{country}',
    'deposit': BASE_WEBHOOK_URL + 'Игрок:+{user_id}+Внес+депозит:+{amount}+USD',
    'first_deposit': BASE_WEBHOOK_URL + 'Игрок:+{user_id}+Сделал+первый+депозит:+{amount}+USD',
    'repeat_deposit': BASE_WEBHOOK_URL + 'Игрок:+{user_id}+Сделал+повторный+депозит:+{amount}+USD',
    'income': BASE_WEBHOOK_URL + 'Игрок:+{user_id}+Получил+выплату:+{amount}+USD'
}

# Настройки логирования
LOGGING = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'logs/bot.log'
}

# Защита от спама
SPAM_PROTECTION = {
    'max_requests_per_minute': 5,
    'ban_duration_minutes': 30
}

# Настройки базы данных
DATABASE_CONFIG = {
    'name': 'database/bot_database.db',
    'backup_path': 'backups/',
    'tables': {
        'users': 'users',
        'stats': 'stats',
        'referrals': 'referrals'
    }
}

# Настройки игр
GAMES = {
    'luckyjet': {
        'min_coefficient': 1.2,
        'max_coefficient': 10.0
    },
    'mines': {
        'grid_sizes': [(3, 3), (5, 5), (7, 7)],
        'max_mines': 5
    }
}

# Настройки профиля пользователя
USER_PROFILE = {
    'default_balance': 0,
    'default_currency': 'USD'
}

# Настройки статистики
STATS_CONFIG = {
    'chart_type': 'line',
    'max_history_days': 30
}

# Настройки админ-панели
ADMIN_PANEL = {
    'allowed_commands': ['stats', 'ban', 'unban', 'message_all'],
    'stats_update_interval': 3600  # в секундах
}

# Настройки уведомлений
NOTIFICATIONS = {
    'welcome_message': True,
    'deposit_reminder': {
        'enabled': True,
        'interval_hours': 24
    }
}

# Пути к шрифтам для генерации изображений
FONTS = {
    'regular': 'resources/fonts/regular.ttf',
    'bold': 'resources/fonts/bold.ttf'
}

# Настройки резервного копирования
BACKUP = {
    'enabled': True,
    'interval_hours': 24,
    'max_backups': 7
}