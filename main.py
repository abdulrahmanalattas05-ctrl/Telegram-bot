import os
import logging
import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# إعداد المفاتيح
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# إعداد السجل
logging.basicConfig(level=logging.INFO)

# دالة الترحيب
def start(update: Update, context: CallbackContext):
    welcome_message = (
        "🤖 أهلاً بك!\n"
        "أنا نموذج ذكاء اصطناعي تم تطويري باستخدام OpenAI.\n"
        "طُوّر هذا البوت بواسطة عبدالرحمن جمال عبدالرب العطاس.\n"
        "يمكنك سؤالي أي شيء ✨"
    )
    update.message.reply_text(welcome_message)

# الرد على الرسائل
def handle_message(update: Update, context: CallbackContext):
    user_input = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response["choices"][0]["message"]["content"]
        update.message.reply_text(reply)
    except Exception as e:
        update.message.reply_text("حدث خطأ، الرجاء المحاولة لاحقًا.")
        logging.error(e)

# تشغيل البوت
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
