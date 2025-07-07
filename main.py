from flask import Flask, request, jsonify
import telebot
from telebot import types
import threading

TOKEN = '8077877232:AAGCKJjE_yNyE-nW2-RxX4PLJ20l6zrsZWA'
CHAT_ID = -1002704677155  # Канал или групповой чат
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)  # Исправлено

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

# Обработчик callback
@bot.callback_query_handler(func=lambda call: call.data == 'about_project')
def about_project_callback(call):
    about_text = (
        "Wu Space — это в первую очередь про комьюнити.\n\n"
        "Здесь собираются люди, которые хотят делиться мыслями, идеями и чувствами, открыто и без лишних фильтров. "
        "Это пространство для тех, кто ищет глубину, вдохновение и поддержку.\n\n"
        "В Wu Space нет давления, нет гонки за лайками или популярностью. Это как уютная гостиная, где можно спокойно поговорить о важном, "
        "послушать других и быть услышанным.\n\n"
        "Внутри есть разные ветки, чтобы легко ориентироваться, что вам интересно:\n\n"
        "Анонсы — все важные новости и события, чтобы ничего не пропустить;\n\n"
        "Внутренний круг — ежедневная информация, посты про древний мир, философию и глубокие темы;\n\n"
        "Чат общения — место для свободного общения, как для тех, кто в Валенсии, так и для друзей со всего мира.\n\n"
        "Здесь мы вместе создаём атмосферу доверия и искренности — место, где каждый может быть собой и найти своих людей.\n\n"
        "Если коротко — Wu Space про живое общение, настоящее участие и ощущение, что ты не один, даже если вокруг большой мир."
    )
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, about_text)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "Привет! Добро пожаловать в меню бота.\n\nВыбери интересующую тебя вкладку."
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu())

# Обработка POST-запроса от Make
@app.route('/send', methods=['POST'])
def send_from_make():
    data = request.get_json()
    text = data.get('text')

    if not text:
        return jsonify({'error': 'Missing \"text\" parameter'}), 400

    try:
        bot.send_message(CHAT_ID, text)
        return jsonify({'status': 'Message sent'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Запуск
def run_flask():
    app.run(host="0.0.0.0", port=5000)

def run_telebot():
    bot.polling(none_stop=True)

if __name__ == '__main__':  # Исправлено
    threading.Thread(target=run_flask).start()
    threading.Thread(target=run_telebot).start()
