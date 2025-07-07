import os
from flask import Flask, request, jsonify
import telebot

TOKEN = os.getenv("TOKEN")
CHAT_ID = -1002704677155

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def main_menu():
    from telebot import types
    markup = types.InlineKeyboardMarkup(row_width=1)

    btn_events = types.InlineKeyboardButton(
        'Хочу знать больше про события 📅', 
        url='https://t.me/wu_space/5'
    )
    btn_events_info = types.InlineKeyboardButton(
        'Подробнее про события и запись в чат @artemiy_starodub',
        url='https://t.me/artemiy_starodub'
    )
    btn_community = types.InlineKeyboardButton(
        'Комьюнити и общение 👥',
        url='https://t.me/wu_space/3'
    )
    btn_meditations = types.InlineKeyboardButton(
        'Медитации, подкасты и музыка 🎧',
        url='https://t.me/wu_space/1'
    )
    btn_shop = types.InlineKeyboardButton(
        'Магазин 🛒',
        url='https://www.terrastra.net'
    )
    btn_about = types.InlineKeyboardButton(
        'Узнать больше о нас (музыка и обучение) 🎶',
        url='https://www.instagram.com/artemiy_teaching_valencia_/'
    )
    btn_blog = types.InlineKeyboardButton(
        'Мой блог и темы терапии 🔥',
        url='https://www.instagram.com/artemiy_starod_psy'
    )
    btn_session = types.InlineKeyboardButton(
        'Записаться на сессию и пообщаться лично 🗣️',
        url='https://t.me/artemiy_starodub'
    )

    markup.add(
        btn_events, btn_events_info, btn_community, btn_meditations,
        btn_shop, btn_about, btn_blog, btn_session
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Привет! Добро пожаловать в меню бота.\n\n"
        "Выбери интересующую тебя вкладку."
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu())

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    if not data or 'text' not in data or not data['text'].strip():
        return jsonify({"error": "Missing required parameter 'text'"}), 400

    text = data['text']
    try:
        bot.send_message(CHAT_ID, text)
        return jsonify({"status": "Message sent"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Запускаем бота в отдельном потоке, а Flask API — в основном
    import threading

    def run_bot():
        bot.infinity_polling()

    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=5000)

