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

(
    NAME, EMAIL, PHONE,
    SKILLS, EXPERIENCE,
    EDUCATION, LANGUAGES, OBJECTIVE
) = range(8)

user_data = {}

# /start yoki tugma
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["📝 Rezyume yaratish"], ["ℹ️ Info", "📞 Kontakt"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("👋 Salom! Rezyume yaratish uchun ismingizni yozing:", reply_markup=reply_markup)
    return NAME

# Info / Contact
async def info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ℹ️ Bu bot professional .docx rezyume yaratadi. /start bosib sinab ko‘ring.")

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📞 Aloqa: @yourusername")

# Qadamlar
async def name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data["name"] = update.message.text
    await update.message.reply_text("✉️ Email manzilingiz?")
    return EMAIL

async def email_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data["email"] = update.message.text
    await update.message.reply_text("📞 Telefon raqamingiz?")
    return PHONE

async def phone_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data["phone"] = update.message.text
    await update.message.reply_text("🛠 Ko‘nikmalaringizni vergul bilan yozing:")
    return SKILLS

async def skills_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data["skills"] = update.message.text
    await update.message.reply_text("💼 Ish tajribangiz (kompaniya, yillar, lavozim):")
    return EXPERIENCE

async def experience_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data["experience"] = update.message.text
    await update.message.reply_text("🎓 Ta’lim (Universitet, yillar, yo‘nalish):")
    return EDUCATION

async def education_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data["education"] = update.message.text
    await update.message.reply_text("🌐 Biladigan tillaringiz (til — daraja):")
    return LANGUAGES

async def language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data["languages"] = update.message.text
    await update.message.reply_text("🎯 Maqsadingizni yozing:")
    return OBJECTIVE

async def objective_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data["objective"] = update.message.text
    filename = generate_resume_docx(user_data)
    await update.message.reply_document(open(filename, "rb"))
    os.remove(filename)
    await update.message.reply_text("✅ Rezyume tayyor! /start buyrug‘ini qayta bosishingiz mumkin.")
    return ConversationHandler.END

# Bekor qilish
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Bekor qilindi.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(filters.Regex("^(📝 Rezyume yaratish)$"), start)
        ],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name_handler)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email_handler)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone_handler)],
            SKILLS: [MessageHandler(filters.TEXT & ~filters.COMMAND, skills_handler)],
            EXPERIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, experience_handler)],
            EDUCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, education_handler)],
            LANGUAGES: [MessageHandler(filters.TEXT & ~filters.COMMAND, language_handler)],
            OBJECTIVE: [MessageHandler(filters.TEXT & ~filters.COMMAND, objective_handler)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("info", info_handler))
    app.add_handler(CommandHandler("contact", contact_handler))
    app.add_handler(MessageHandler(filters.Regex("^(ℹ️ Info)$"), info_handler))
    app.add_handler(MessageHandler(filters.Regex("^(📞 Kontakt)$"), contact_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
