from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import os
from openai import OpenAI

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

async def handle_image_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_prompt = update.message.text

    try:
        # Запрашиваем изображение через DALL·E 3
        response = client.images.generate(
            model="dall-e-3",  # или "dall-e-2"
            prompt=user_prompt,
            n=1,
            size="1024x1024"
        )

        image_url = response.data[0].url
        await update.message.reply_photo(photo=image_url)

    except Exception as e:
        await update.message.reply_text(f"Ошибка генерации изображения:\n{e}")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_image_prompt))
app.run_polling()
