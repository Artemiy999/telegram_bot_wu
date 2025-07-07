import os
import telegram

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    print("Переменная BOT_TOKEN не задана")
    exit(1)

bot = telegram.Bot(token=TOKEN)

WEBHOOK_URL = f"https://твой_рендер_URL/{TOKEN}"

bot.delete_webhook()
success = bot.set_webhook(WEBHOOK_URL)

if success:
    print(f"Webhook успешно установлен на {WEBHOOK_URL}")
else:
    print("Ошибка установки webhook")
