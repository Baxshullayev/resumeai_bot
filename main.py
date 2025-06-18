import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, ConversationHandler, filters
)
from resume_generator import generate_resume_docx

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

NAME, EMAIL, PHONE, SKILLS, EXPERIENCE = range(5)
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Salom! Men sizga rezyume tuzishda yordam beraman.\n\nIsmingizni kiriting:")
    return NAME

async def name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data["name"] = update.message.text
    await update.message.reply_text("✉️ Email manzilingizni kiriting:")
    return EMAIL

async def email_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data["email"] = update.message.text
    await update.message.reply_text("📞 Telefon raqamingizni kiriting:")
    return PHONE

async def phone_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data["phone"] = update.message.text
    await update.message.reply_text("🛠 Ko‘nikmalaringizni yozing:")
    return SKILLS

async def skills_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data["skills"] = update.message.text
    await update.message.reply_text("💼 Ish tajribangiz haqida yozing:")
    return EXPERIENCE

async def experience_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data["experience"] = update.message.text
    filename = generate_resume_docx(user_data)
    await update.message.reply_document(open(filename, "rb"))
    os.remove(filename)
    await update.message.reply_text("✅ Rezyume tayyor! Yana rezyume yaratish uchun /start buyrug‘ini bosing.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Jarayon bekor qilindi.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name_handler)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email_handler)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone_handler)],
            SKILLS: [MessageHandler(filters.TEXT & ~filters.COMMAND, skills_handler)],
            EXPERIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, experience_handler)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
