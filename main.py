import logging
from flask import Flask, request, abort
import telebot

# Ваш токен бота
TOKEN = '8077877232:AAGCKJjE_yNyE-nW2-RxX4PLJ20l6zrsZWA'

# Публичный URL вашего сервера, где доступен бот (от Render или другого)
WEBHOOK_URL_BASE = 'https://telegram-bot-wu.onrender.com'
WEBHOOK_URL_PATH = f'/{TOKEN}'

# Инициализация бота и Flask
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

# ------------------------
# Эндпоинт для health check (Render и другие сервисы мониторинга могут ping-ить этот URL)
@app.route('/healthz')
def healthz():
    return "OK", 200

# ------------------------
# Основной webhook endpoint, на который Telegram отправляет обновления
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_str = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return '', 200
    else:
        abort(403)

# ------------------------
# Установка webhook при старте
def setup_webhook():
    logging.info("Removing existing webhook...")
    bot.remove_webhook()
    full_url = WEBHOOK_URL_BASE + WEBHOOK_URL_PATH
    logging.info(f"Setting webhook to {full_url} ...")
    success = bot.set_webhook(url=full_url)
    if success:
        logging.info("Webhook setup successful")
    else:
        logging.error("Failed to set webhook")

# ------------------------
# Обработка команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    welcome_text = (
        "Привет! Добро пожаловать в меню бота.\n\n"
        "Выбери интересующую тебя вкладку:"
    )
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        telebot.types.InlineKeyboardButton('Вступить в WU SPACE', url='https://t.me/wu_space'),
        telebot.types.InlineKeyboardButton('О чем проект?', callback_data='about_project'),
        telebot.types.InlineKeyboardButton('Подробнее про события и запись в чат @artemiy_starodub', url='https://t.me/artemiy_starodub'),
        telebot.types.InlineKeyboardButton('Магазин 🛒', url='https://www.terrastra.net'),
        telebot.types.InlineKeyboardButton('Узнать больше о нас (музыка и обучение) 🎶', url='https://www.instagram.com/artemiy_teaching_valencia_/'),
        telebot.types.InlineKeyboardButton('Мой блог и темы терапии 🔥', url='https://www.instagram.com/artemiy_starod_psy'),
        telebot.types.InlineKeyboardButton('Записаться на сессию и пообщаться лично 🗣', url='https://t.me/artemiy_starodub')
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# Обработка callback query для "about_project"
@bot.callback_query_handler(func=lambda call: call.data == 'about_project')
def handle_about_project(call):
    about_text = (
        "Wu Space — это в первую очередь про комьюнити.\n\n"
        "Здесь собираются люди, которые хотят делиться мыслями, идеями и чувствами...\n\n"
        "Если коротко — Wu Space про живое общение, настоящее участие и ощущение, что ты не один, даже если вокруг большой мир."
    )
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, about_text)

# ------------------------
# Запуск Flask-сервера и установка webhook
if __name__ == '__main__':
    setup_webhook()
    app.run(host='0.0.0.0', port=10000)
