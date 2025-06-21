import logging
import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputFile
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
)
from resume_generator import generate_resume_docx
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Bosqichlar
(
    NAME,
    EMAIL,
    PHONE,
    OBJECTIVE,
    EDUCATION,
    EXPERIENCE,
    SKILLS,
    LANGUAGES,
    OFFICE,
    PHOTO_DECISION,
    PHOTO_UPLOAD
) = range(11)

# Ma’lumotlar
USER_DATA = {}
PHOTO_PATHS = {}

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 Rezyume yaratish uchun ismingizni kiriting:")
    USER_DATA[update.effective_chat.id] = {}
    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    USER_DATA[update.effective_chat.id]["name"] = update.message.text
    await update.message.reply_text("✉️ Email manzilingizni kiriting:")
    return EMAIL


async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    USER_DATA[update.effective_chat.id]["email"] = update.message.text
    await update.message.reply_text("📞 Telefon raqamingizni kiriting:")
    return PHONE


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    USER_DATA[update.effective_chat.id]["phone"] = update.message.text
    await update.message.reply_text("🎯 Maqsadingizni yozing:")
    return OBJECTIVE


async def get_objective(update: Update, context: ContextTypes.DEFAULT_TYPE):
    USER_DATA[update.effective_chat.id]["objective"] = update.message.text
    await update.message.reply_text("🎓 Ta’lim ma’lumotlaringizni yozing (yiliga ajratib):")
    return EDUCATION


async def get_education(update: Update, context: ContextTypes.DEFAULT_TYPE):
    USER_DATA[update.effective_chat.id]["education"] = update.message.text
    await update.message.reply_text("💼 Ish tajribangizni yozing:\n\nMasalan: Kompaniya, 2020-2023, Lavozim")
    return EXPERIENCE


async def get_experience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    USER_DATA[update.effective_chat.id]["experience"] = update.message.text
    await update.message.reply_text("🛠 Ko‘nikmalaringizni yozing (vergul bilan):")
    return SKILLS


async def get_skills(update: Update, context: ContextTypes.DEFAULT_TYPE):
    USER_DATA[update.effective_chat.id]["skills"] = update.message.text
    await update.message.reply_text("🌐 Qaysi tillarni bilasiz? (yangi qatorda yozing):")
    return LANGUAGES


async def get_languages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    USER_DATA[update.effective_chat.id]["languages"] = update.message.text
    await update.message.reply_text("📊 Office dasturlari bilan ishlash tajribangizni yozing (vergul bilan):")
    return OFFICE


async def get_office(update: Update, context: ContextTypes.DEFAULT_TYPE):
    USER_DATA[update.effective_chat.id]["office"] = update.message.text

    keyboard = [
        [
            InlineKeyboardButton("🖼 Rasm yuklayman", callback_data="yes_photo"),
            InlineKeyboardButton("🚫 Rasmsiz davom etaman", callback_data="no_photo")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("3x4 rasmni qo‘shmoqchimisiz?", reply_markup=reply_markup)
    return PHOTO_DECISION


async def photo_decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "yes_photo":
        await query.edit_message_text("📸 Iltimos, 3x4 rasmni yuboring:")
        return PHOTO_UPLOAD
    else:
        return await generate_resume(query.message.chat_id, context)


async def photo_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    photo_file = await update.message.photo[-1].get_file()
    photo_path = f"{chat_id}_photo.jpg"
    await photo_file.download_to_drive(photo_path)
    PHOTO_PATHS[chat_id] = photo_path
    return await generate_resume(chat_id, context)


async def generate_resume(chat_id, context):
    user_data = USER_DATA.get(chat_id, {})
    photo_path = PHOTO_PATHS.get(chat_id)

    resume_file = generate_resume_docx(user_data, photo_path)
    await context.bot.send_document(chat_id=chat_id, document=InputFile(resume_file))
    await context.bot.send_message(chat_id=chat_id, text="✅ Sizning rezyume tayyor!")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Jarayon bekor qilindi.")
    return ConversationHandler.END


def main():
    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            OBJECTIVE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_objective)],
            EDUCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_education)],
            EXPERIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_experience)],
            SKILLS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_skills)],
            LANGUAGES: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_languages)],
            OFFICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_office)],
            PHOTO_DECISION: [CallbackQueryHandler(photo_decision)],
            PHOTO_UPLOAD: [MessageHandler(filters.PHOTO, photo_upload)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(conv)
    app.run_polling()


if __name__ == "__main__":
    main()
