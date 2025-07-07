from flask import Flask, request, abort
import telebot
import logging

# --- Настройки ---
TOKEN = '8077877232:AAGCKJjE_yNyE-nW2-RxX4PLJ20l6zrsZWA'  # Твой токен
WEBHOOK_URL_BASE = 'https://telegram-bot-wu.onrender.com'  # Замени на URL твоего приложения на Render
WEBHOOK_URL_PATH = f"/{TOKEN}"  # Используем токен в пути для безопасности

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Включаем логирование для отладки
logging.basicConfig(level=logging.INFO)

# --- Клавиатура меню ---
from telebot import types

def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton('Вступить в WU SPACE', url='https://t.me/wu_space'),
        types.InlineKeyboardButton('О чем проект?', callback_data='about_project'),
        types.InlineKeyboardButton('Подробнее про события и запись в чат @artemiy_starodub', url='https://t.me/artemiy_starodub'),
        types.InlineKeyboardButton('Магазин 🛒', url='https://www.terrastra.net'),
        types.InlineKeyboardButton('Узнать больше о нас (музыка и обучение) 🎶', url='https://www.instagram.com/artemiy_teaching_valencia_/'),
        types.InlineKeyboardButton('Мой блог и темы терапии 🔥', url='https://www.instagram.com/artemiy_starod_psy'),
        types.InlineKeyboardButton('Записаться на сессию и пообщаться лично 🗣', url='https://t.me/artemiy_starodub')
    )
    return markup

# --- Обработчики команд и callback ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "Привет! Добро пожаловать в меню бота.\n\nВыбери интересующую тебя вкладку."
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: call.data == 'about_project')
def about_project_callback(call):
    about_text = (
        "Wu Space — это в первую очередь про комьюнити.\n\n"
        "Здесь собираются люди, которые хотят делиться мыслями, идеями и чувствами...\n\n"
        "Если коротко — Wu Space про живое общение, настоящее участие и ощущение, что ты не один, даже если вокруг большой мир."
    )
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, about_text)

# --- Webhook route для Telegram ---
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        abort(403)

# --- Простой тестовый route ---
@app.route('/', methods=['GET'])
def index():
    return 'Telegram bot is running', 200

# --- Функция установки webhook ---
def setup_webhook():
    logging.info("Removing existing webhook...")
    bot.remove_webhook()
    logging.info(f"Setting new webhook to {WEBHOOK_URL_BASE}{WEBHOOK_URL_PATH} ...")
    success = bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
    if success:
        logging.info("Webhook setup successful")
    else:
        logging.error("Failed to set webhook")

# --- Точка входа ---
if __name__ == '__main__':
    setup_webhook()  # Устанавливаем webhook при запуске
    app.run(host='0.0.0.0', port=10000)
