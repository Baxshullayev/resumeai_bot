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

# Conversation states
NAME, EMAIL, PHONE, SKILLS, EXPERIENCE = range(5)
user_data = {}

# Boshlash
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📝 Rezyume yaratish"],
        ["ℹ️ Info", "📞 Kontakt"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👋 Salom! Men sizga rezyume tuzishda yordam beraman.\n\nIsmingizni kiriting:",
        reply_markup=reply_markup
    )
    return NAME

# Info tugmasi yoki /info
async def info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Bu bot sizga professional rezyume (.docx formatda) yaratishda yordam beradi.\n"
        "Boshlash uchun 📝 Rezyume yaratish tugmasini bosing yoki /start yozing."
    )

# Kontakt tugmasi yoki /contact
async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 Bog‘lanish uchun:\n"
        "Admin: @yourusername\n"
        "Email: resumeai@example.com"
    )

# Har bir qadam uchun handlerlar:
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
    await update.message.reply_text("🛠 Ko‘nikmalaringizni vergul bilan yozing:\nMasalan: Python, Django, Git")
    return SKILLS

async def skills_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data["skills"] = update.message.text
    await update.message.reply_text(
        "💼 Ish tajribangizni kiriting.\n"
        "Format: Kompaniya, Yil-Yil, Lavozim\n"
        "Masalan:\nAsaxiy, 2022-2023, Python Developer\nMediapark, 2023-2024, Team Lead"
    )
    return EXPERIENCE

async def experience_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data["experience"] = update.message.text
    filename = generate_resume_docx(user_data)
    await update.message.reply_document(open(filename, "rb"))
    os.remove(filename)
    await update.message.reply_text("✅ Rezyume tayyor! Yana yaratish uchun /start buyrug‘ini bosing.")
    return ConversationHandler.END

# Bekor qilish
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Jarayon bekor qilindi.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# Asosiy
def main():
    app = Application.builder().token(TOKEN).build()

    # Rezyume yaratish uchun suhbat
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
