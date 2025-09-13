import logging
from aiogram import Bot, Dispatcher, executor, types
import os

# تفعيل اللوجات (مفيدة لو حصلت أخطاء)
logging.basicConfig(level=logging.INFO)

# توكن البوت (حطه من متغير البيئة أو اكتبه مباشرة)
API_TOKEN = os.getenv("BOT_TOKEN")  # تأكد أنك ضايف BOT_TOKEN في Secrets

# إنشاء البوت والديسباتشر
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# أمر /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("حياك الله 🤝، معك بوت الحجز الخاص بالملعب!")


# أمر /help
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("الأوامر المتاحة:\n/start - ترحيب\n/help - المساعدة")


# أي رسالة ثانية
@dp.message_handler()
async def echo_message(message: types.Message):
    await message.reply("تم استلام رسالتك ✅")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)