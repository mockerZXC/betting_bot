from config.config import ADMIN_IDS
from config.languages import get_text
from database.db_manager import (
    get_all_users, 
    get_user_data, 
    get_referral_data, 
    get_deposit_data
)
from telebot import types

class AdminPanel:
    def __init__(self, bot):
        self.bot = bot

    def check_admin(self, user_id):
        """Проверка прав администратора"""
        return str(user_id) in ADMIN_IDS

    def get_user_stats(self, user_id, lang):
        """Получение статистики пользователя"""
        try:
            user_data = get_user_data(user_id)
            if not user_data:
                return get_text('user_not_found', lang)
            return {
                'games_played': user_data.get('games_played', 0),
                'wins': user_data.get('wins', 0),
                'deposits': user_data.get('deposits', 0),
                'registration_date': user_data.get('registration_date'),
                'last_activity': user_data.get('last_activity')
            }
        except Exception as e:
            print(f"Error in get_user_stats: {e}")
            return get_text('error_message', lang)

    def admin_stats(self, user_id, lang):
        """Отображение общей статистики администратору"""
        if not self.check_admin(user_id):
            return get_text('access_denied', lang)
        
        try:
            users = get_all_users()
            stats = self._calculate_stats(users)
            stats_text = self._format_stats_message(stats, lang)
            markup = self._create_admin_markup(lang)
            
            return {
                'text': stats_text,
                'markup': markup
            }
        except Exception as e:
            print(f"Error in admin_stats: {e}")
            return get_text('error_message', lang)

    def _calculate_stats(self, users):
        """Подсчет статистики"""
        return {
            'total_users': len(users),
            'total_games': sum(user.get('games_played', 0) for user in users),
            'total_wins': sum(user.get('wins', 0) for user in users),
            'total_deposits': sum(user.get('deposits', 0) for user in users),
            'active_users': len([u for u in users if u.get('is_active', False)]),
            'depositors': len([u for u in users if u.get('has_deposit', False)])
        }

    def _format_stats_message(self, stats, lang):
        """Форматирование сообщения со статистикой"""
        return f"""
📊 <b>{get_text('admin_stats_title', lang)}</b>
👥 {get_text('total_users', lang)}: {stats['total_users']}
🎮 {get_text('total_games', lang)}: {stats['total_games']}
🏆 {get_text('total_wins', lang)}: {stats['total_wins']}
💰 {get_text('total_deposits', lang)}: {stats['total_deposits']}
⚡️ {get_text('active_users', lang)}: {stats['active_users']}
💳 {get_text('depositors', lang)}: {stats['depositors']}
        """

    def _create_admin_markup(self, lang):
        """Создание клавиатуры админ-панели"""
        markup = types.InlineKeyboardMarkup(row_width=2)
        buttons = [
            types.InlineKeyboardButton(
                get_text('user_stats_btn', lang),
                callback_data='admin_user_stats'
            ),
            types.InlineKeyboardButton(
                get_text('referral_stats_btn', lang),
                callback_data='admin_referral_stats'
            ),
            types.InlineKeyboardButton(
                get_text('deposit_stats_btn', lang),
                callback_data='admin_deposit_stats'
            ),
            types.InlineKeyboardButton(
                get_text('back_btn', lang),
                callback_data='admin_back'
            )
        ]
        markup.add(*buttons)
        return markup

    def get_referral_stats(self, lang):
        """Получение статистики по рефералам"""
        try:
            referral_data = get_referral_data()
            return self._format_referral_stats(referral_data, lang)
        except Exception as e:
            print(f"Error in get_referral_stats: {e}")
            return get_text('error_message', lang)

    def get_deposit_stats(self, lang):
        """Получение статистики по депозитам"""
        try:
            deposit_data = get_deposit_data()
            return self._format_deposit_stats(deposit_data, lang)
        except Exception as e:
            print(f"Error in get_deposit_stats: {e}")
            return get_text('error_message', lang)

    def _format_referral_stats(self, referral_data, lang):
        """Форматирование статистики рефералов"""
        # Здесь нужно реализовать форматирование статистики рефералов
        pass

    def _format_deposit_stats(self, deposit_data, lang):
        """Форматирование статистики депозитов"""
        # Здесь нужно реализовать форматирование статистики депозитов
        pass
