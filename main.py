import os
from flask import Flask, request, jsonify
import telegram
import logging

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    logger.error("Переменная окружения BOT_TOKEN не установлена")
    exit(1)

app = Flask(__name__)
bot = telegram.Bot(token=TOKEN)

@app.route("/healthz")
def health():
    return "OK", 200

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    try:
        # Получаем обновление от Telegram
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        
        if update.message:
            chat_id = update.message.chat.id
            text = update.message.text or ""

            logger.info(f"Получено сообщение от {chat_id}: {text}")

            # Обработка команд
            if text.startswith("/start"):
                reply = (
                    "Привет! Я - твой бот.\n"
                    "Напиши /info, чтобы узнать больше обо мне."
                )
            elif text.startswith("/info"):
                reply = (
                    "Я умею:\n"
                    "- Отвечать на твои сообщения\n"
                    "- Поддерживать простой диалог\n"
                    "- И многое другое!\n\n"
                    "Пиши что угодно — я отвечу!"
                )
            else:
                # Ответ на любое другое сообщение — эхо с дополнением
                reply = f"Ты написал: {text}"

            bot.send_message(chat_id=chat_id, text=reply)

    except Exception as e:
        logger.error(f"Ошибка обработки обновления: {e}")

    return jsonify(ok=True)

if __name__ == "__main__":
    # Для локального теста
    app.run(host="0.0.0.0", port=10000)
