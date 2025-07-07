from flask import Flask, request, jsonify
import telebot
from telebot import types
import os

TOKEN = '8077877232:AAGCKJjE_yNyE-nW2-RxX4PLJ20l6zrsZWA'
CHAT_ID = -1001234567890  # Заменить на ID канала или чата

WEBHOOK_URL = 'https://telegram-bot-wu.onrender.com'  # 🟡 ВСТАВЬ СЮДА СВОЙ Render URL

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- Главное меню ---
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

# --- Обработка callback ---
@bot.callback_query_handler(func=lambda call: call.data == 'about_project')
def about_project_callback(call):
    about_text = (
        "Wu Space — это в первую очередь про комьюнити...\n\n"
        "Если коротко — Wu Space про живое общение, настоящее участие и ощущение, что ты не один, даже если вокруг большой мир."
    )
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, about_text)

# --- Обработка команды /start ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "Привет! Добро пожаловать в меню бота.\n\nВыбери интересующую тебя вкладку."
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu())

# --- Эндпоинт для Telegram Webhook ---
@app.route('/', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

# --- Эндпоинт для Make ---
@app.route('/send', methods=['POST'])
def send_from_make():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({'error': 'Missing "text" parameter'}), 400
    try:
        bot.send_message(CHAT_ID, text)
        return jsonify({'status': 'Message sent'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- Настройка Webhook ---
def setup_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)

# --- Запуск приложения ---
if __name__ == '__main__':
    setup_webhook()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
