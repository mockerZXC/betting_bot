from config import config
from config.languages import notifications
from datetime import datetime

class NotificationManager:
    def __init__(self, bot):
        self.bot = bot
        self.admin_ids = config.ADMIN_IDS
        self.group_id = config.CHAT_ID
        
    def send_notification(self, message_type, data, lang='ru'):
        """
        Отправка уведомлений в группу и админам
        """
        text = self._get_notification_text(message_type, data, lang)
        
        # Отправка в группу
        try:
            self.bot.send_message(self.group_id, text)
        except Exception as e:
            print(f"Ошибка отправки в группу: {e}")
            
        # Отправка админам
        for admin_id in self.admin_ids:
            try:
                self.bot.send_message(admin_id, text)
            except Exception as e:
                print(f"Ошибка отправки админу {admin_id}: {e}")

    def _get_notification_text(self, message_type, data, lang):
        """
        Формирование текста уведомления в зависимости от типа
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        notification_types = {
            'registration': notifications[lang]['new_registration'].format(
                user_id=data['user_id'],
                geo=data.get('user_data', {}).get('geo', 'Unknown'),
                ip=data.get('user_data', {}).get('ip', 'Unknown'),
                device=data.get('user_data', {}).get('device', 'Unknown'),
                timestamp=timestamp
            ),
            'deposit': notifications[lang]['new_deposit'].format(
                user_id=data['user_id'],
                amount=data.get('deposit_data', {}).get('amount', '0'),
                currency=data.get('deposit_data', {}).get('currency', 'USD'),
                payment_method=data.get('deposit_data', {}).get('payment_method', 'Unknown'),
                timestamp=timestamp
            ),
            'first_deposit': notifications[lang]['first_deposit'].format(
                user_id=data['user_id'],
                amount=data.get('deposit_data', {}).get('amount', '0'),
                timestamp=timestamp
            ),
            'repeat_deposit': notifications[lang]['repeat_deposit'].format(
                user_id=data['user_id'],
                amount=data.get('deposit_data', {}).get('amount', '0'),
                timestamp=timestamp
            ),
            'withdrawal': notifications[lang]['withdrawal'].format(
                user_id=data['user_id'],
                amount=data.get('withdrawal_data', {}).get('amount', '0'),
                timestamp=timestamp
            ),
            'app_launch': notifications[lang]['app_launch'].format(
                user_id=data['user_id'],
                timestamp=timestamp
            )
        }
        
        return notification_types.get(message_type, 'Unknown notification type')

    def notify_registration(self, user_id, user_data, lang='ru'):
        """Уведомление о регистрации"""
        data = {
            'user_id': user_id,
            'user_data': user_data,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.send_notification('registration', data, lang)

    def notify_deposit(self, user_id, deposit_data, is_first=False, lang='ru'):
        """Уведомление о депозите"""
        data = {
            'user_id': user_id,
            'deposit_data': deposit_data,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        message_type = 'first_deposit' if is_first else 'repeat_deposit'
        self.send_notification(message_type, data, lang)

    def notify_withdrawal(self, user_id, withdrawal_data, lang='ru'):
        """Уведомление о выводе средств"""
        data = {
            'user_id': user_id,
            'withdrawal_data': withdrawal_data,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.send_notification('withdrawal', data, lang)

    def notify_app_launch(self, user_id, lang='ru'):
        """Уведомление о запуске приложения"""
        data = {
            'user_id': user_id,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.send_notification('app_launch', data, lang)