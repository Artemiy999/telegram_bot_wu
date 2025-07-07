from flask import Flask, request
import telebot
import os

TOKEN = '8077877232:AAGCKJjE_yNyE-nW2-RxX4PLJ20l6zrsZWA'
WEBHOOK_URL = 'https://telegram-bot-wu.onrender.com/'  # 🟡 Замени на твой render-домен

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Главное меню
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

# Обработка callback-кнопки
@bot.callback_query_handler(func=lambda call: call.data == 'about_project')
def about_project_callback(call):
    about_text = (
        "Wu Space — это в первую очередь про комьюнити.\n\n"
        "Здесь собираются люди, которые хотят делиться мыслями, идеями и чувствами...\n\n"
        "Если коротко — Wu Space про живое общение, настоящее участие и ощущение, что ты не один, даже если вокруг большой мир."
    )
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, about_text)

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "Привет! Добро пожаловать в меню бота.\n\nВыбери интересующую тебя вкладку."
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu())

# Обработка POST-запросов от Telegram
@app.route(f"/{TOKEN}", methods=['POST'])
def receive_update():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

# Установка webhook при запуске
@app.before_first_request
def setup_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")

# Пинг для Render (необязательный, но полезен)
@app.route('/', methods=['GET'])
def index():
    return 'Bot is running', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

