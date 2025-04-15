from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from shivu import application, user_collection
from shivu.modules.shop import generated_characters  # Import generated waifu codes

# Store which user redeemed which code (in memory)
redeemed_codes = {}

async def redeem(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    if not context.args:
        return await update.message.reply_text("Please provide a code to redeem. Usage: `/redeem <code>`", parse_mode="Markdown")

    code = context.args[0]

    # Check if code was generated
    valid_codes = list(generated_characters.values())
    if code not in valid_codes:
        return await update.message.reply_text("❌ Invalid or expired code.")

    # Check if already redeemed
    if code in redeemed_codes:
        return await update.message.reply_text("❌ This code has already been redeemed.")

    # Add balance
    bonus = 400 if not str(code).startswith("D") else 1_000_000_000_000  # Normal vs dgen
    await user_collection.update_one(
        {'id': user_id},
        {'$inc': {'balance': bonus}},
        upsert=True
    )

    redeemed_codes[code] = user_id
    await update.message.reply_text(f"✅ Code redeemed! You received ₹{bonus}.")

application.add_handler(CommandHandler("redeem", redeem))
