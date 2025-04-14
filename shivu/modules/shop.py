from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler
from shivu import application

# Rarity-wise prices
RARITY_DETAILS = {
    "1": ("⚪ Common", 100),
    "2": ("🟣 Rare", 250),
    "3": ("🟢 Medium", 500),
    "4": ("🟡 Legendary", 1000),
    "5": ("💮 Special Edition", 2500),
    "6": ("🔮 Limited Edition", 5000),
    "7": ("🎐 Celestial Beauty", 10000),
    "8": ("🪽 Divine Edition", 25000),
    "9": ("💦 Wet Elegance", 50000),
    "10": ("🎴 Cosplay", 100000)
}

# /shop command
async def shop(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(f"{info[0]} - ₹{info[1]}", callback_data=f"rarity_{key}")]
        for key, info in RARITY_DETAILS.items()
    ]
    await update.message.reply_text(
        "**Welcome to the Waifu Shop!**\nSelect a rarity to buy a waifu:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# callback for button click
async def handle_rarity_click(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    rarity_id = query.data.split("_")[1]
    rarity_name, price = RARITY_DETAILS.get(rarity_id, ("Unknown", 0))
    await query.message.reply_text(
        f"You selected *{rarity_name}* (Price: ₹{price})\n\nSend the character ID using /buy `<id>`",
        parse_mode="Markdown"
    )

# Register handlers
application.add_handler(CommandHandler("shop", shop))
application.add_handler(CallbackQueryHandler(handle_rarity_click, pattern=r"^rarity_\d+$"))
