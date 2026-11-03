import os
import nest_asyncio
from dotenv import load_dotenv
from telegram import (
    Update, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ConversationHandler, ContextTypes
)

# Load env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Token missing!")
# State
LANGUAGE = range(1)


# /start → Language Selection
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Please select your preferred language:\n\n🇬🇧 English\n🇮🇳 हिन्दी",
        reply_markup=ReplyKeyboardMarkup(
            [['English', 'हिन्दी']],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )
    return LANGUAGE


# Language selected → Show full menu with MiniApp buttons
async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang_text = update.message.text.lower()
    lang = "hi" if "hi" in lang_text or "हिन्दी" in lang_text else "en"
    context.user_data["lang"] = lang

    # MAIN MENU WITH MINI APPS
    menu = ReplyKeyboardMarkup([
        [KeyboardButton("PARLAY 22 🎯", web_app=WebAppInfo(
            url="https://www.parlay22.com/"
        )), KeyboardButton("PARLAY 44 🎯", web_app=WebAppInfo(
            url="https://www.parlay44.com/"
        ))],
        ["Help 🏠"],
        ["Share Contact 💸", "Visit Channel 📢"]
    ], resize_keyboard=True)

    if lang == "hi":
        await update.message.reply_text(
            "✔ भाषा चुनी गई: हिन्दी\n\nकृपया नीचे दिए गए विकल्प चुनें 👇",
            reply_markup=menu
        )
    else:
        await update.message.reply_text(
            "✔ Language Selected: English\n\nChoose an option below 👇",
            reply_markup=menu
        )

    return ConversationHandler.END


# Menu Buttons Handler
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""

    if "Help" in text:
        await update.message.reply_text("🏠 Help & Support:\n👉 @ankitparlay")

    elif "Share Contact" in text:
        await update.message.reply_text("📩 Contact Us:\n👉 @ankitparlay")

    elif "Visit Channel" in text:
        await update.message.reply_text("📢 Join our official channel:\n👉 https://t.me/+lbBysqeI3H83OTc9")

    else:
        await update.message.reply_text("❗ Invalid choice. Please choose from menu.")


# Cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Session ended. Type /start to begin again.")
    return ConversationHandler.END


# BOT MAIN
if __name__ == "__main__":
    nest_asyncio.apply()
    app = ApplicationBuilder().token(TOKEN).build()

    # Conversation for language
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_language)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True
    )

    app.add_handler(conv_handler)

    # Menu Handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))

    print("🚀 FastPayz Mini App Bot is running…")
    app.run_polling()
