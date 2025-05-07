import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# কনফিগারেশন
TOKEN = "6360274044:AAHVbxew7aabVd_APPCmtjTdKhtRy0V3Utw"
DEEPSEEK_API_KEY = "YOUR_DEEPSEEK_API_KEY"  # DeepSeek API কী (প্রয়োজনে রেজিস্টার করুন)
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # অথবা DeepSeek-এর অফিসিয়াল API এন্ডপয়েন্ট

# লগিং সেটআপ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """স্টার্ট কমান্ড হ্যান্ডলার"""
    await update.message.reply_text('হ্যালো! আমি DeepSeek-powered AI অ্যাসিস্ট্যান্ট! 😊')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """হেল্প কমান্ড হ্যান্ডলার"""
    help_text = """
    🤖 *DeepSeek AI Assistant Bot* 🤖
    --------------------------
    - আমাকে যেকোনো প্রশ্ন জিজ্ঞাসা করুন!
    - /start - বট শুরু করুন
    - /help - সাহায্য দেখুন
    """
    await update.message.reply_text(help_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ইউজারের মেসেজ প্রসেস করবে"""
    user_message = update.message.text
    
    try:
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",  # অথবা DeepSeek-এর অন্যান্য মডেল
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_message}
            ]
        }
        
        # DeepSeek API কে রিকোয়েস্ট পাঠানো
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
        response_data = response.json()
        
        ai_response = response_data["choices"][0]["message"]["content"]
        await update.message.reply_text(ai_response)
    except Exception as e:
        logging.error(f"DeepSeek API তে সমস্যা: {e}")
        await update.message.reply_text("⚠️ দুঃখিত, DeepSeek AI-তে কিছু সমস্যা হয়েছে। পরে আবার চেষ্টা করুন!")

def main():
    """বট শুরু করবে"""
    application = Application.builder().token(TOKEN).build()
    
    # কমান্ড হ্যান্ডলার
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # মেসেজ হ্যান্ডলার
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # বট শুরু করুন
    application.run_polling()

if __name__ == "__main__":
    main()