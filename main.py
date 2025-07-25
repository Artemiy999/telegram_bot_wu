import os
from flask import Flask, request
import telegram
import logging
from dotenv import load_dotenv

# Загружаем .env
load_dotenv()

# Получаем токены
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/healthz', methods=['GET'])
def health_check():
    return "ok"

@app.route('/webhook', methods=['POST'])
def webhook():
    # Проверка секрета Telegram (высокая защита от фейковых запросов)
    if request.headers.get('X-Telegram-Bot-Api-Secret-Token') != WEBHOOK_SECRET:
        logger.warning("⚠️ Отказано в доступе: подделка запроса.")
        return "unauthorized", 403

    try:
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat.id
        message = update.message.text

        logger.info(f"Получено сообщение от {chat_id}: {message}")

        if message == '/start':
            bot.send_message(chat_id=chat_id, text="Привет! Я тебя слышу.")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
    return "ok"
