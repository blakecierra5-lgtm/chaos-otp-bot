import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Load chaos messages from secret file or fallback
def load_chaos_messages():
    try:
        with open("/etc/secrets/chaos_messages.txt") as f:
            return f.read().splitlines()
    except Exception:
        return [
            "Wrong! The shadows see you.",
            "Nope. Try again or face the chaos.",
            "Access denied. Your vibes are off.",
            "Enter the right code or suffer the consequences.",
        ]

chaos_messages = load_chaos_messages()

# Dictionary to store OTPs temporarily (in-memory)
otp_storage = {}

# Generate random OTP (for demo purposes)
def generate_otp():
    return str(random.randint(100000, 999999))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the chaos OTP bot! Use /login to get started.")

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    otp = generate_otp()
    otp_storage[user_id] = otp
    await update.message.reply_text(f"Your OTP is: {otp} (don’t share this!)")

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in otp_storage:
        await update.message.reply_text("You need to /login first!")
        return

    entered_otp = update.message.text.strip()
    correct_otp = otp_storage[user_id]

    if entered_otp == correct_otp:
        await update.message.reply_text("OTP verified! Welcome to chaos.")
        del otp_storage[user_id]  # Remove used OTP
    else:
        # Reply with a random chaos message on wrong OTP
        await update.message.reply_text(random.choice(chaos_messages))

def main():
    bot_token = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("login", login))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), verify))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
