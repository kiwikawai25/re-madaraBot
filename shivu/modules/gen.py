from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from shivu import application, user_collection
from shivu.modules.storage import cooldowns, generated_codes

import random
from datetime import datetime, timedelta

def generate_code(length=6):
    return ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=length))

async def gen(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    now = datetime.now()

    if user_id not in cooldowns:
        cooldowns[user_id] = []

    # Filter out timestamps older than 24 hours
    cooldowns[user_id] = [t for t in cooldowns[user_id] if now - t < timedelta(hours=24)]

    if len(cooldowns[user_id]) >= 2:
        last_time = cooldowns[user_id][-1]
        if now - last_time < timedelta(hours=5):
            next_time = last_time + timedelta(hours=5)
            await update.message.reply_text(
                f"You've reached your limit. Next /gen available at {next_time.strftime('%H:%M:%S')}."
            )
            return

    # Generate code and store it
    code = generate_code()
    generated_codes[user_id] = generated_codes.get(user_id, []) + [code]

    # Add balance
    await user_collection.update_one(
        {'id': user_id},
        {'$inc': {'balance': 400}},
        upsert=True
    )

    cooldowns[user_id].append(now)

    await update.message.reply_text(
        f"Here is your redeem code: `{code}`\n\n₹400 has been added to your balance!",
        parse_mode='Markdown'
    )

application.add_handler(CommandHandler("gen", gen))
