import os
import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

# تحميل القيم من ملف التكوين
load_dotenv("config.env")
TOKEN = os.environ.get("TOKEN")  # placeholder: YOUR_BOT_TOKEN
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")  # placeholder: YOUR_OPENAI_KEY
ADMIN_ID = int(os.environ.get("ADMIN_ID", 0))  # placeholder: YOUR_TELEGRAM_ID
DEFAULT_REPLY = os.environ.get("DEFAULT_REPLY", "شكرًا على رسالتك! سنتواصل معك قريبًا.")

# تفعيل OpenAI
openai.api_key = OPENAI_API_KEY

# رسالة ترحيبية عند بدء البوت
def start(update: Update, context: CallbackContext):
    update.message.reply_text("أهلًا! يمكنك مراسلتي، وسأرد عليك باستخدام الذكاء الاصطناعي.")

# الردود باستخدام ChatGPT
def ai_reply(update: Update, context: CallbackContext):
    user_msg = update.message.text
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_msg,
            max_tokens=150
        )
        reply = response.choices[0].text.strip()
    except Exception as e:
        reply = DEFAULT_REPLY
        print(e)
    
    update.message.reply_text(reply)

# أمر الإدارة (يعمل فقط للـ ADMIN_ID)
def admin_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id == ADMIN_ID:
        update.message.reply_text("أمر الإدارة نفذ بنجاح!")
    else:
        update.message.reply_text("آسف، هذا الأمر لك فقط.")

# تشغيل البوت
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, ai_reply))
    dp.add_handler(CommandHandler("admin", admin_command))

    updater.start_polling()
    print("Bot started with ChatGPT...")
    updater.idle()

if __name__ == "__main__":
    main()