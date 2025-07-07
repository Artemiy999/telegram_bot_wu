import os
import telebot
from telebot import types
import time
import threading

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# ID чата (группы/канала), куда бот будет писать сообщения
CHAT_ID = -1002704677155  # <-- замени на свой чат ID


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
    # Отправляем сообщение в чат (а не пользователю, который написал)
    bot.send_message(CHAT_ID, welcome_text, reply_markup=main_menu())

# Функция для автопубликаций в чат
def auto_posting(chat_id, delay=86400):
    while True:
        for text in auto_texts:
            try:
                bot.send_message(chat_id, text)
                print(f"Опубликовано сообщение в {chat_id}")
            except Exception as e:
                print(f"Ошибка при публикации в {chat_id}: {e}")
            time.sleep(delay)  # пауза между публикациями (по умолчанию 24 часа)

# Запуск автопубликаций в отдельном потоке
def start_auto_posting():
    thread = threading.Thread(target=auto_posting, args=(CHAT_ID, 3600))  # раз в час
    thread.daemon = True
    thread.start()

if __name__ == '__main__':
    start_auto_posting()
    bot.polling()

