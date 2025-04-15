from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, CallbackContext
from datetime import datetime, timedelta
from shivu import application, user_collection

# Rarity-wise reward
RARITY_REWARDS = {
    "⚪ Common": 100,
    "🟣 Rare": 250,
    "🟢 Medium": 500,
    "🟡 Legendary": 1000,
    "💮 Special Edition": 2500,
    "🔮 Limited Edition": 5000,
    "🎐 Celestial Beauty": 10000,
    "🪽 Divine Edition": 25000,
    "💦 Wet Elegance": 50000,
    "🎴 Cosplay": 100000
}

last_sell_time = {}

async def sell(update: Update, context: CallbackContext):
    if not update.message.reply_to_message or len(context.args) < 1:
        return await update.message.reply_text("Reply to a waifu message with `/sell <id>`", parse_mode="Markdown")

    user_id = update.effective_user.id
    now = datetime.now()

    # Cooldown check (24h)
    if user_id in last_sell_time and now - last_sell_time[user_id] < timedelta(hours=24):
        next_time = last_sell_time[user_id] + timedelta(hours=24)
        return await update.message.reply_text(f"You already sold a waifu. Try again after: {next_time.strftime('%Y-%m-%d %H:%M:%S')}")

    char_id = context.args[0]

    user_data = await user_collection.find_one({'id': user_id})
    if not user_data or 'characters' not in user_data:
        return await update.message.reply_text("You don't own any waifus.")

    character = next((c for c in user_data['characters'] if c['id'] == char_id), None)
    if not character:
        return await update.message.reply_text("Waifu not found in your harem.")

    reward = RARITY_REWARDS.get(character['rarity'], 100)

    # Confirm button
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Yes, Sell", callback_data=f"confirm_sell_{char_id}")]
    ])
    await update.message.reply_text(
        f"Are you sure you want to sell {character['name']} (Rarity: {character['rarity']}) for ₹{reward}?",
        reply_markup=keyboard
    )

async def confirm_sell_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    char_id = query.data.split("_")[-1]

    user_data = await user_collection.find_one({'id': user_id})
    character = next((c for c in user_data['characters'] if c['id'] == char_id), None)
    if not character:
        return await query.edit_message_text("Character not found in your collection.")

    reward = RARITY_REWARDS.get(character['rarity'], 100)

    # Remove character & add balance
    await user_collection.update_one(
        {'id': user_id},
        {
            '$pull': {'characters': {'id': char_id}},
            '$inc': {'balance': reward}
        }
    )
    last_sell_time[user_id] = datetime.now()
    await query.edit_message_text(f"You sold {character['name']} for ₹{reward}!")

application.add_handler(CommandHandler("sell", sell))
application.add_handler(CallbackQueryHandler(confirm_sell_callback, pattern=r'^confirm_sell_'))
