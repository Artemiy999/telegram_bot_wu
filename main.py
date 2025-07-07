import os
from flask import Flask, request, jsonify
import telebot
from telebot import types
from threading import Thread
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
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

# Callback на кнопку "О проекте"
@bot.callback_query_handler(func=lambda call: call.data == 'about_project')
def about_project_callback(call):
    about_text = (
        "Wu Space — это в первую очередь про комьюнити.\n\n"
        "Здесь собираются люди, которые хотят делиться мыслями, идеями и чувствами, открыто и без лишних фильтров. "
        "Это пространство для тех, кто ищет глубину, вдохновение и поддержку.\n\n"
        "Внутри есть разные ветки:\n"
        "— Анонсы\n— Внутренний круг\n— Общение\n\n"
        "Wu Space — про настоящее участие и ощущение, что ты не один."
    )
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, about_text)

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "Привет! Добро пожаловать в меню бота.\n\nВыбери интересующую тебя вкладку."
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu())

# Webhook-приём сообщений от Make
@app.route('/send', methods=['POST'])
def send_from_make():
    data = request.get_json()
    text = data.get('text')

    if not text:
        return jsonify({'error': 'Missing \"text\" parameter'}), 400

    try:
        bot.send_message(chat_id=CHAT_ID, text=text)
        return jsonify({'status': 'Message sent'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Запуск Flask
def run_flask():
    app.run(host="0.0.0.0", port=5000)

# Запуск бота (важно: без polling)
def run_bot():
    from flask import abort

    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + '/webhook')

    @app.route('/webhook', methods=['POST'])
    def webhook():
        if request.headers.get('content-type') == 'application/json':
            json_string = request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            abort(403)

# Основной запуск
if __name__ == '__main__':
    Thread(target=run_flask).start()
    Thread(target=run_bot).start()
