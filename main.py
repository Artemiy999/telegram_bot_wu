from flask import Flask, request, jsonify
import telebot
from telebot import types
import threading

TOKEN = '8077877232:AAGCKJjE_yNyE-nW2-RxX4PLJ20l6zrsZWA'
CHAT_ID = -1002704677155  # Групповой чат или канал
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# --- Главное меню ---
def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)

    markup.add(
        types.InlineKeyboardButton('Хочу знать больше про события 📅', url='https://t.me/wu_space/5'),
        types.InlineKeyboardButton('Подробнее про события и запись в чат @artemiy_starodub', url='https://t.me/artemiy_starodub'),
        types.InlineKeyboardButton('Комьюнити и общение 👥', url='https://t.me/wu_space/3'),
        types.InlineKeyboardButton('Медитации, подкасты и музыка 🎧', url='https://t.me/wu_space/1'),
        types.InlineKeyboardButton('Магазин 🛒', url='https://www.terrastra.net'),
        types.InlineKeyboardButton('Узнать больше о нас (музыка и обучение) 🎶', url='https://www.instagram.com/artemiy_teaching_valencia_/'),
        types.InlineKeyboardButton('Мой блог и темы терапии 🔥', url='https://www.instagram.com/artemiy_starod_psy'),
        types.InlineKeyboardButton('Записаться на сессию и пообщаться лично 🗣️', url='https://t.me/artemiy_starodub')
    )

    return markup

# --- Обработка /start от пользователя ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Привет! Добро пожаловать в меню бота.\n\n"
        "Выбери интересующую тебя вкладку."
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu())

# --- Обработка POST-запроса от Make ---
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

# --- Запуск Flask + Telegram Bot ---
def run_flask():
    app.run(host="0.0.0.0", port=5000)

def run_telebot():
    bot.polling()

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    threading.Thread(target=run_telebot).start()
