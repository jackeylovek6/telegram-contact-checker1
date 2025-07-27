import os
import asyncio
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
QUEUE_FILE = "queue.txt"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def enqueue_number(number: str):
    with open(QUEUE_FILE, "a", encoding="utf-8") as f:
        f.write(number.strip() + "\n")

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Gửi lệnh:\n"
        "/loc\n+84901234567\n+84345678901\n"
        "để kiểm tra số Telegram. Mỗi số 1 dòng."
    )

async def loc_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    lines = message.split("\n")[1:]

    if not lines:
        await update.message.reply_text("❗ Vui lòng nhập số điện thoại.")
        return

    valid = []
    for line in lines:
        phone = line.strip()
        if phone.startswith("+") or phone.isdigit():
            valid.append(phone)

    for number in valid:
        enqueue_number(number)

    await update.message.reply_text(f"✅ Đã thêm {len(valid)} số vào hàng đợi.")


def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("loc", loc_handler))
    logger.info("🤖 Bot đang chạy...")
    app.run_polling()

if __name__ == "__main__":
    run_bot()

