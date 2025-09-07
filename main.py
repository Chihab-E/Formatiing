from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

def format_product(product_name, full_name, price, link):
    return f"""
تخفييض رائع ل {product_name} 🤯🛞  

✅ {full_name}  
✅ بسعر : {price}$ 😍  

🔗 الرابط : {link}  

🔰  للحصول على أفضل التخفيضات على منتجات محددة، استخدم البوت ⬇️:  
https://t.me/Chihabcoinsbot 🤖
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send /post short_name full_name price link")

async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        product_name = context.args[0]
        full_name = context.args[1]
        price = context.args[2]
        link = context.args[3]

        msg = format_product(product_name, full_name, price, link)
        await update.message.reply_text(msg)
    except Exception as e:
        await update.message.reply_text("Usage: /post short_name full_name price link")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("post", post))

app.run_polling()
