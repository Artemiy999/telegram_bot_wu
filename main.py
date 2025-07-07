import os
import telebot
from telebot import types
import threading
import time

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

CHAT_ID = -1002704677155  # ID чата для рассылок и сообщений из Make

auto_texts = [
    "Тема 1: Как дышать правильно для медитации.",
    "Тема 2: Польза регулярных сессий психотерапии.",
    "Тема 3: Практики осознанности в повседневной жизни.",
    "Тема 4: Гвоздестояние — что это и кому полезно.",
]

def main_menu():
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
    # Отвечаем лично пользователю, который нажал /start
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu())

# Функция для автопостинга в чат (например, раз в час)
def auto_posting(chat_id, delay=3600):
    while True:
        for text in auto_texts:
            try:
                bot.send_message(chat_id, text)
                print(f"Опубликовано сообщение в {chat_id}")
            except Exception as e:
                print(f"Ошибка при публикации в {chat_id}: {e}")
            time.sleep(delay)

def start_auto_posting():
    thread = threading.Thread(target=auto_posting, args=(CHAT_ID,))
    thread.daemon = True
    thread.start()

# Функция для Make: отправка сообщения в чат через бота
def send_message_to_chat_from_make(text):
    try:
        bot.send_message(CHAT_ID, text)
        print("Сообщение из Make отправлено в чат")
    except Exception as e:
        print(f"Ошибка при отправке из Make: {e}")

if __name__ == '__main__':
    start_auto_posting()
    bot.polling()
