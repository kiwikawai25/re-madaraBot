from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from shivu import application
from shivu.modules.storage import generated_codes, user_balances

import random

OWNER_ID = 8156600797

def generate_code(length=6):
    return ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=length))

async def dgen(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    if user_id != OWNER_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    code = generate_code()

    # Store generated code
    generated_codes[user_id] = generated_codes.get(user_id, []) + [code]

    # Add balance
    user_balances[user_id] = user_balances.get(user_id, 0) + 1_000_000_000_000

    await update.message.reply_text(
        f"(OWNER) Redeem Code: `{code}`\nYour balance is now ₹{user_balances[user_id]}",
        parse_mode='Markdown'
    )

application.add_handler(CommandHandler("dgen", dgen))
