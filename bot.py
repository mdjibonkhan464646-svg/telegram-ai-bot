import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Setup Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

async def reply_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    user_text = update.message.text
    
    try:
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reply_ai))
    
    print("Bot is running...")
    app.run_polling()
