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

# /buy command
async def buy(update: Update, context: CallbackContext):
    args = context.args
    if not args:
        await update.message.reply_text("Usage: /buy <id>")
        return
    waifu_id = args[0]
    # Replace this with actual purchase logic if needed
    await update.message.reply_text(f"You bought waifu with ID: {waifu_id}")

# /bal command
async def bal(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    # Dummy balance for now
    balance = 1000
    await update.message.reply_text(f"Your current balance is ₹{balance}")

# /gen command
async def gen(update: Update, context: CallbackContext):
    await update.message.reply_text("Random waifu generated! (This is a placeholder)")

# /dgen command
async def dgen(update: Update, context: CallbackContext):
    await update.message.reply_text("Daily waifu generated! (This is a placeholder)")

# Register handlers
application.add_handler(CommandHandler("shop", shop))
application.add_handler(CallbackQueryHandler(handle_rarity_click, pattern=r"^rarity_\d+$"))
application.add_handler(CommandHandler("buy", buy))
application.add_handler(CommandHandler("bal", bal))
application.add_handler(CommandHandler("gen", gen))
application.add_handler(CommandHandler("dgen", dgen))

# Start the bot
if __name__ == "__main__":
    application.run_polling()
