import random
import string
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from shivu import application

OWNER_ID = 8156600797
generated_codes = {}

def generate_code(length=12):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

async def dgen(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    code = generate_code()
    amount = 1_000_000_000_000  # 1000 trillion
    generated_codes[code] = amount

    await update.message.reply_text(
        f"(OWNER) Generated redeem code: `{code}`\nAmount: ₹{amount}",
        parse_mode="Markdown"
    )

application.add_handler(CommandHandler("dgen", dgen))
