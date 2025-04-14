from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler
from shivu import application

RARITY_BUTTONS = {
    "1": "⚪ Common",
    "2": "🟣 Rare",
    "3": "🟢 Medium",
    "4": "🟡 Legendary",
    "5": "💮 Special Edition",
    "6": "🔮 Limited Edition",
    "7": "🎐 Celestial Beauty",
    "8": "🪽 Divine Edition",
    "9": "💦 Wet Elegance",
    "10": "🎴 Cosplay"
}

# /shop command
async def shop(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(text=rarity, callback_data=f"rarity_{key}")]
        for key, rarity in RARITY_BUTTONS.items()
    ]
    await update.message.reply_text(
        "**Welcome to the Waifu Shop!**\nSelect a rarity to buy a waifu:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# callback for rarity buttons
async def handle_rarity_click(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    rarity_id = query.data.split("_")[1]
    rarity_name = RARITY_BUTTONS.get(rarity_id, "Unknown")
    await query.message.reply_text(f"You selected *{rarity_name}*\n\nSend the character ID using /buy `<id>`", parse_mode="Markdown")

# Register handlers
application.add_handler(CommandHandler("shop", shop))
application.add_handler(CallbackQueryHandler(handle_rarity_click, pattern=r"^rarity_\d+$"))
