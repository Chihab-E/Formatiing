from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes,
    ConversationHandler, filters
)
from dotenv import load_dotenv
import os
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Validate token
if not TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables!")

# Steps of the conversation
PRODUCT_NAME, FULL_NAME, PRICE, LINK = range(4)

def format_product(product_name, full_name, price, link):
    """Format the product information into a message"""
    return f"""تخفييض رائع ل {product_name} 🤯🛞  
✅ {full_name}  
✅ بسعر : {price}$ 😍  
🔗 الرابط : {link}  
🔰 للحصول على أفضل التخفيضات على منتجات محددة، استخدم البوت ⬇️:  
https://t.me/Chihabcoinsbot 🤖"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the conversation and ask for product name"""
    try:
        await update.message.reply_text(
            "مرحباً! لننشئ منشور منتج جديد! 🛍️\n\n"
            "ما هو *الاسم المختصر* للمنتج؟",
            parse_mode='Markdown'
        )
        return PRODUCT_NAME
    except Exception as e:
        logger.error(f"Error in start: {e}")
        await update.message.reply_text("حدث خطأ. حاول مرة أخرى.")
        return ConversationHandler.END

async def get_product_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get the product name and ask for full name"""
    try:
        product_name = update.message.text.strip()
        if not product_name:
            await update.message.reply_text("يرجى إدخال اسم المنتج.")
            return PRODUCT_NAME
            
        context.user_data["product_name"] = product_name
        await update.message.reply_text(
            "ممتاز! الآن أرسل لي *الاسم الكامل* للمنتج.",
            parse_mode='Markdown'
        )
        return FULL_NAME
    except Exception as e:
        logger.error(f"Error in get_product_name: {e}")
        await update.message.reply_text("حدث خطأ. حاول مرة أخرى.")
        return ConversationHandler.END

async def get_full_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get the full name and ask for price"""
    try:
        full_name = update.message.text.strip()
        if not full_name:
            await update.message.reply_text("يرجى إدخال الاسم الكامل للمنتج.")
            return FULL_NAME
            
        context.user_data["full_name"] = full_name
        await update.message.reply_text(
            "رائع! 👌 الآن أخبرني *السعر* (الرقم فقط).",
            parse_mode='Markdown'
        )
        return PRICE
    except Exception as e:
        logger.error(f"Error in get_full_name: {e}")
        await update.message.reply_text("حدث خطأ. حاول مرة أخرى.")
        return ConversationHandler.END

async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get the price and ask for link"""
    try:
        price_text = update.message.text.strip()
        if not price_text:
            await update.message.reply_text("يرجى إدخال السعر.")
            return PRICE
            
        # Validate price is numeric
        try:
            float(price_text.replace('$', '').replace(',', ''))
        except ValueError:
            await update.message.reply_text(
                "يرجى إدخال سعر صحيح (أرقام فقط).\n"
                "مثال: 29.99"
            )
            return PRICE
            
        context.user_data["price"] = price_text
        await update.message.reply_text(
            "تقريباً انتهينا! أرسل لي *الرابط* للمنتج.",
            parse_mode='Markdown'
        )
        return LINK
    except Exception as e:
        logger.error(f"Error in get_price: {e}")
        await update.message.reply_text("حدث خطأ. حاول مرة أخرى.")
        return ConversationHandler.END

async def get_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get the link and finish the conversation"""
    try:
        link = update.message.text.strip()
        if not link:
            await update.message.reply_text("يرجى إدخال الرابط.")
            return LINK
            
        # Basic URL validation
        if not (link.startswith('http://') or link.startswith('https://')):
            await update.message.reply_text(
                "يرجى إدخال رابط صحيح يبدأ بـ http:// أو https://"
            )
            return LINK
            
        context.user_data["link"] = link
        
        # Build and send the formatted message
        formatted_msg = format_product(
            context.user_data["product_name"],
            context.user_data["full_name"],
            context.user_data["price"],
            context.user_data["link"]
        )
        
        await update.message.reply_text("✅ تم إنشاء المنشور بنجاح!")
        await update.message.reply_text(formatted_msg)
        
        # Clear user data
        context.user_data.clear()
        
        return ConversationHandler.END
        
    except Exception as e:
        logger.error(f"Error in get_link: {e}")
        await update.message.reply_text("حدث خطأ أثناء إنشاء المنشور.")
        return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the conversation"""
    try:
        await update.message.reply_text("❌ تم إلغاء إنشاء المنشور.")
        context.user_data.clear()
        return ConversationHandler.END
    except Exception as e:
        logger.error(f"Error in cancel: {e}")
        return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message"""
    help_text = """
🤖 مرحباً بك في بوت إنشاء منشورات المنتجات!

الأوامر المتاحة:
/post - إنشاء منشور منتج جديد
/cancel - إلغاء العملية الحالية
/help - عرض هذه الرسالة

للبدء، استخدم الأمر /post واتبع التعليمات!
    """
    await update.message.reply_text(help_text)

def main():
    """Main function to run the bot"""
    try:
        # Create application
        app = ApplicationBuilder().token(TOKEN).build()
        
        # Create conversation handler
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("post", start)],
            states={
                PRODUCT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_product_name)],
                PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_price)],
                LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_link)],
            },
            fallbacks=[CommandHandler("cancel", cancel)],
        )
        
        # Add handlers
        app.add_handler(conv_handler)
        app.add_handler(CommandHandler("help", help_command))
        
        # Start the bot
        logger.info("Bot is starting...")
        app.run_polling()
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
