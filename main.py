import os
import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

# تحميل القيم من ملف التكوين
load_dotenv("config.env")
TOKEN = os.environ.get("TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ADMIN_ID = int(os.environ.get("ADMIN_ID", 0))
DEFAULT_REPLY = os.environ.get("DEFAULT_REPLY", "شكرًا على رسالتك! سنتواصل معك قريبًا.")

# تفعيل OpenAI
openai.api_key = OPENAI_API_KEY

# رسالة ترحيبية
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

# --- لوحة التحكم --- #

# تحديث الرد الافتراضي
def set_default_reply(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        update.message.reply_text("آسف، هذا الأمر لك فقط.")
        return

    new_reply = " ".join(context.args)
    if not new_reply:
        update.message.reply_text("اكتب الرد الجديد بعد الأمر.")
        return

    global DEFAULT_REPLY
    DEFAULT_REPLY = new_reply
    update.message.reply_text(f"تم تحديث الرد الافتراضي إلى: {DEFAULT_REPLY}")

# إعادة تشغيل البوت
def restart_bot(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        update.message.reply_text("آسف، هذا الأمر لك فقط.")
        return
    update.message.reply_text("جارٍ إعادة تشغيل البوت...")
    os._exit(0)

# مثال أمر آخر للإدارة (اختياري)
def admin_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id == ADMIN_ID:
        update.message.reply_text("أنت المشرف! الأمر نفذ بنجاح.")
    else:
        update.message.reply_text("آسف، هذا الأمر لك فقط.")

# --- نهاية لوحة التحكم --- #

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, ai_reply))
    dp.add_handler(CommandHandler("setreply", set_default_reply))
    dp.add_handler(CommandHandler("restart", restart_bot))
    dp.add_handler(CommandHandler("admin", admin_command))

    updater.start_polling()
    print("Bot started with ChatGPT and Admin Panel...")
    updater.idle()

if __name__ == "__main__":
    main()