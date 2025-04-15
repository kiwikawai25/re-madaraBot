from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler
from datetime import datetime, timedelta
from shivu import application, user_collection
from shivu.modules.storage import user_balances, last_sell_time

# Rarity-based prices
RARITY_PRICES = {
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

# Step 1: User sends /sell <id>
async def sell(update: Update, context: CallbackContext):
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to the waifu message you want to sell.")
        return

    user_id = update.effective_user.id
    if user_id in last_sell_time:
        last_time = last_sell_time[user_id]
        if datetime.now() - last_time < timedelta(hours=24):
            next_time = last_time + timedelta(hours=24)
            await update.message.reply_text(
                f"You already sold a waifu today.\nNext sell available at: {next_time.strftime('%H:%M:%S')}"
            )
            return

    if len(context.args) != 1:
        await update.message.reply_text("Usage: /sell <character_id>")
        return

    char_id = context.args[0]

    # Store pending sell data temporarily
    context.user_data["pending_sell"] = char_id

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Confirm", callback_data="confirm_sell"),
         InlineKeyboardButton("❌ Cancel", callback_data="cancel_sell")]
    ])
    await update.message.reply_text("Are you sure you want to sell this waifu?", reply_markup=keyboard)

# Step 2: Handle confirmation button
async def handle_sell_confirm(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    char_id = context.user_data.get("pending_sell")

    if not char_id:
        await query.edit_message_text("No waifu to sell.")
        return

    user = await user_collection.find_one({'id': user_id})
    if not user or 'characters' not in user:
        await query.edit_message_text("You don't own any characters.")
        return

    character = next((c for c in user['characters'] if c['id'] == char_id), None)
    if not character:
        await query.edit_message_text("Character not found in your collection.")
        return

    rarity = character['rarity']
    reward = RARITY_PRICES.get(rarity, 0)

    # Add balance and remove character
    user_balances[user_id] = user_balances.get(user_id, 0) + reward
    await user_collection.update_one(
        {'id': user_id},
        {'$pull': {'characters': {'id': char_id}}}
    )
    last_sell_time[user_id] = datetime.now()

    await query.edit_message_text(
        f"✅ Successfully sold `{char_id}` for ₹{reward}!", parse_mode='Markdown'
    )

# Step 3: Handle cancel button
async def handle_sell_cancel(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    context.user_data.pop("pending_sell", None)
    await query.edit_message_text("❌ Sell cancelled.")

# Register handlers
application.add_handler(CommandHandler("sell", sell))
application.add_handler(CallbackQueryHandler(handle_sell_confirm, pattern="^confirm_sell$"))
application.add_handler(CallbackQueryHandler(handle_sell_cancel, pattern="^cancel_sell$"))
