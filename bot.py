from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import os
import openai

# Загружаем ключи из переменных среды
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Создаём клиента OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Обработчик всех сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    # === Если пользователь просит изображение ===
    if user_input.lower().startswith("/img "):
        prompt = user_input[5:]

        try:
            image_response = client.images.generate(
                model="dall-e-2",  # Можно заменить на "dall-e-3" при наличии доступа
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            image_url = image_response.data[0].url
            await update.message.reply_photo(photo=image_url)

        except Exception as e:
            await update.message.reply_text(f"Ошибка при генерации изображения:\n{e}")

    # === Обычный GPT-ответ ===
    else:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_input}]
            )
            await update.message.reply_text(response.choices[0].message.content)

        except Exception as e:
            await update.message.reply_text(f"Ошибка при обращении к GPT:\n{e}")

# Запускаем бота
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
