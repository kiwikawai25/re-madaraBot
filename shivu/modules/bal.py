from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from shivu import application, user_collection

async def bal(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user = await user_collection.find_one({'id': user_id})
    balance = user.get("balance", 0) if user else 0
    await update.message.reply_text(f"Your WaifuCoin balance: ₹{balance}")

application.add_handler(CommandHandler("bal", bal))
