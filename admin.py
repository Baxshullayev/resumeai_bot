
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import os
from database import get_all_users

ADMIN_ID = int(os.getenv("ADMIN_ID"))

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Sizda ruxsat yo‘q.")
        return

    if not context.args:
        await update.message.reply_text("ℹ️ Foydalanish: /broadcast xabar matni")
        return

    text = ' '.join(context.args)
    users = get_all_users()

    count = 0
    for user_id in users:
        try:
            await context.bot.send_message(chat_id=user_id, text=text)
            count += 1
        except Exception:
            continue

    await update.message.reply_text(f"✅ Xabar {count} foydalanuvchiga yuborildi.")

admin_commands = [CommandHandler("broadcast", broadcast)]
