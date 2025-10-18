import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from googletrans import Translator

translator = Translator()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_id = update.message.chat_id
    user_lang = translator.detect(user_message).lang

    # Step 1: translate to English
    if user_lang != "en":
        translated_text = translator.translate(user_message, dest="en").text
        await update.message.reply_text(f"🗣️ {update.message.from_user.first_name} said (in English):\n{translated_text}")
    else:
        # Step 2: translate your English reply back to user's language
        if update.message.reply_to_message:
            original_message = update.message.reply_to_message.text
            detected_lang = translator.detect(original_message).lang
            if detected_lang != "en":
                back_translation = translator.translate(user_message, dest=detected_lang).text
                await context.bot.send_message(chat_id=chat_id, text=f"💬 Your message (translated):\n{back_translation}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
