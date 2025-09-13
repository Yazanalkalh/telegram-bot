from aiogram import Bot, Dispatcher, executor, types
import os

API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))  # ضع chat_id الخاص بك في Secrets

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# لتخزين الرسائل مؤقتًا
user_messages = {}

# استقبال أي رسالة من أي شخص
@dp.message_handler()
async def forward_to_admin(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "غير معروف"

    # حفظ الرسالة
    user_messages[message.message_id] = user_id

    # إعادة توجيه الرسالة إليك
    text = f"رسالة جديدة من @{username} (ID:{user_id}):\n{message.text}\n\nللرد استخدم:\n/reply {message.message_id} نص الرد"
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)

    # رسالة شكر للمرسل
    await message.reply("شكرًا لملاحظتك! سيتم مراجعتها من قبل الإدارة ✅")


# أمر للرد على الرسائل مباشرة
@dp.message_handler(commands=['reply'])
async def reply_to_user(message: types.Message):
    try:
        args = message.text.split(maxsplit=2)
        if len(args) < 3:
            await message.reply("صيغة الأمر خاطئة! استخدم:\n/reply message_id نص الرد")
            return

        msg_id = int(args[1])
        reply_text = args[2]

        if msg_id in user_messages:
            user_id = user_messages[msg_id]
            await bot.send_message(chat_id=user_id, text=reply_text)
            await message.reply("تم إرسال الرد ✅")
        else:
            await message.reply("لم أجد رسالة بهذا الرقم.")
    except Exception as e:
        await message.reply(f"حدث خطأ: {e}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
