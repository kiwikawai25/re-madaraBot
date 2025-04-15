from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from shivu import application

OWNER_ID = 8156600797
generated_characters = {}
user_balances = {}

async def dgen(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    user_id = update.effective_user.id
    char_id = "D" + str(user_id)[-4:]
    generated_characters[user_id] = char_id

    # Set balance to 1000 trillion
    user_balances[user_id] = 1_000_000_000_000

    await update.message.reply_text(
        f"(OWNER) Generated waifu ID: {char_id}\nYour balance is now ₹{user_balances[user_id]}"
    )

application.add_handler(CommandHandler("dgen", dgen))
