from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from shivu import application, user_collection
import random
from datetime import datetime, timedelta

cooldowns = {}

async def gen(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    now = datetime.now()

    # Check cooldown
    if user_id in cooldowns:
        last_used = cooldowns[user_id]
        if now - last_used < timedelta(hours=12):
            next_time = last_used + timedelta(hours=12)
            await update.message.reply_text(f"You can use /gen again at {next_time.strftime('%H:%M:%S')}")
            return

    # Generate random 12-character code
    code = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=12))

    # Store code and update balance
    await user_collection.update_one(
        {'id': user_id},
        {'$inc': {'balance': 400}},
        upsert=True
    )

    cooldowns[user_id] = now

    await update.message.reply_text(f"Here is your redeem code: `{code}`\n\n₹400 has been added to your balance!", parse_mode='Markdown')

application.add_handler(CommandHandler("gen", gen))
