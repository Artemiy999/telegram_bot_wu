import os
from flask import Flask, request
import telegram
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    logger.error("BOT_TOKEN не найден в переменных окружения")
    exit(1)

app = Flask(__name__)
bot = telegram.Bot(token=TOKEN)

# Проверка работоспособности сервиса
@app.route("/healthz")
def health():
    return "OK", 200

# Основной маршрут для webhook - принимает POST от Telegram
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    try:
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        if update.message:
            chat_id = update.message.chat.id
            text = update.message.text or ""
            logger.info(f"Получено сообщение от {chat_id}: {text}")

            # Пример простого ответа
            bot.send_message(chat_id=chat_id, text="Привет! Я работаю!")
    except Exception as e:
        logger.error(f"Ошибка обработки update: {e}")
    return "ok", 200


if __name__ == "__main__":
    # Для локального теста (НЕ для Render, на Render запускаем gunicorn)
    app.run(host="0.0.0.0", port=10000)
