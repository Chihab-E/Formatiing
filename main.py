from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes,
    ConversationHandler, filters
)
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Steps of the conversation
PRODUCT_NAME, FULL_NAME, PRICE, LINK = range(4)

def format_product(product_name, full_name, price, link):
    return f"""
تخفييض رائع ل {product_name} 🤯🛞  

✅ {full_name}  
✅ بسعر : {price}$ 😍  

🔗 الرابط : {link}  

🔰 للحصول على أفضل التخفيضات على منتجات محددة، استخدم البوت ⬇️:  
https://t.me/Chihabcoinsbot 🤖
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Let's create a product post!\n\nWhat is the *short name* of the product?")
    return PRODUCT_NAME

async def get_product_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["product_name"] = update.message.text
    await update.message.reply_text("Great! Now send me the *full name* of the product.")
    return FULL_NAME

async def get_full_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["full_name"] = update.message.text
    await update.message.reply_text("Perfect 👌. Now tell me the *price* (just the number).")
    return PRICE

async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["price"] = update.message.text
    await update.message.reply_text("Almost done! Send me the *link* to the product.")
    return LINK

async def get_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["link"] = update.message.text

    # Build the message
    msg = format_product(
        context.user_data["product_name"],
        context.user_data["full_name"],
        context.user_data["price"],
        context.user_data["link"]
    )
    await update.message.reply_text(msg)

    # End conversation
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Post creation cancelled.")
    return ConversationHandler.END

app = ApplicationBuilder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("post", start)],
    states={
        PRODUCT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_product_name)],
        FULL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_full_name)],
        PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_price)],
        LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_link)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(conv_handler)

app.run_polling()
