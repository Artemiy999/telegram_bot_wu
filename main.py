import os
from flask import Flask, request
import telegram
import logging

TOKEN = os.getenv("BOT_TOKEN")
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/healthz', methods=['GET'])
def health_check():
    return "ok"

@app.route('/webhook', methods=['POST'])  # <-- вот тут исправили
def webhook():
    try:
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat.id
        message = update.message.text

        logger.info(f"Received message from {chat_id}: {message}")

        if message == '/start':
            bot.send_message(chat_id=chat_id, text="Привет! Я тебя слышу.")
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}")
    return "ok"
