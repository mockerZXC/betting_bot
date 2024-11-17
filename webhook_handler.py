from telebot import TeleBot

class WebhookHandler:
    def __init__(self, bot_token, admin_group_id):
        self.bot = TeleBot(bot_token)
        self.admin_group_id = admin_group_id

    async def process_webhook(self, data):
        event_type = data['event_type']
        # Форматируем сообщение для группы
        message = self.format_webhook_data(data)
        # Отправляем в группу
        await self.bot.send_message(
            chat_id=self.admin_group_id,
            text=message,
            parse_mode='HTML'
        )
        # Обрабатываем событие
        if event_type == 'registration':
            await self.handle_registration(data)
        elif event_type == 'deposit':
            await self.handle_deposit(data)

    def format_webhook_data(self, data):
        """Форматирование данных для отправки в группу"""
        if data['event_type'] == 'registration':
            return f"""
🆕 Новая регистрация
👤 ID: {data['user_id']}
📍 Гео: {data['user_data']['geo']}
🌐 IP: {data['user_data']['ip']}
📱 Устройство: {data['user_data']['device']}
⏰ Время: {data['timestamp']}
            """
        else:  # deposit
            return f"""
💰 Новый депозит
👤 ID: {data['user_id']}
💵 Сумма: {data['deposit_data']['amount']} {data['deposit_data']['currency']}
🏦 Метод: {data['deposit_data']['payment_method']}
⏰ Время: {data['timestamp']}
            """

    async def handle_registration(self, data):
        
        pass

    async def handle_deposit(self, data):
        
        pass

