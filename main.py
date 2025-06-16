
import logging, os
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters,
    ConversationHandler, ContextTypes
)
from resume_generator import generate_resume_pdf
from database import save_user
from admin import admin_commands
from dotenv import load_dotenv

load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Steps
NAME, EMAIL, PHONE, SKILLS, EXPERIENCE = range(5)

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 Rezyume tayyorlash uchun ismingizni kiriting:")
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
    await update.message.reply_text("💡 Ko‘nikmalaringizni kiriting (vergul bilan):")
    return SKILLS

async def skills_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data["skills"] = update.message.text
    await update.message.reply_text("💼 Ish tajribangizni qisqacha yozing:")
    return EXPERIENCE

async def experience_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data["experience"] = update.message.text
    pdf_file = generate_resume_pdf(user_data)

    await update.message.reply_document(pdf_file, caption="✅ Rezyume tayyor bo‘ldi.")
    save_user(update.effective_user.id)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Jarayon bekor qilindi.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(os.getenv("BOT_TOKEN")).build()

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

    app.add_handlers(admin_commands)
    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
