from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from shivu import application, user_collection
from shivu.modules.storage import user_balances  # Yeh line add ki gayi hai

async def bal(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    # First try from DB
    user = await user_collection.find_one({'id': user_id})
    balance = user.get("balance", 0) if user else 0

    # If storage has updated value (overwritten), show that
    if user_id in user_balances:
        balance = user_balances[user_id]  # Yeh block bhi add kiya gaya hai

    await update.message.reply_text(f"Your WaifuCoin balance: ₹{balance}")

application.add_handler(CommandHandler("bal", bal))
