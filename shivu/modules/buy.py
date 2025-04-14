from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from shivu import application, collection, user_collection

# Rarity prices
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

async def buy(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not context.args:
        return await update.message.reply_text("Please provide a character ID to buy. Usage: `/buy 02`", parse_mode='Markdown')

    char_id = context.args[0]

    # Find character
    character = await collection.find_one({"id": char_id})
    if not character:
        return await update.message.reply_text(
            "*Sorry This Character Is Not Uploaded if You Want This Character then msg @Botsaller69*",
            parse_mode="Markdown"
        )

    # Fetch user
    user = await user_collection.find_one({"id": user_id})
    if not user:
        return await update.message.reply_text("You need to /gen and /redeem first to get some balance.")

    balance = user.get("balance", 0)
    rarity = character["rarity"]
    price = RARITY_PRICES.get(rarity, 1000)

    if balance < price:
        return await update.message.reply_text("Bro You Don't Have Minimum Balance For Buy That Waifu!")

    # Add character and deduct balance
    await user_collection.update_one(
        {"id": user_id},
        {
            "$push": {"characters": character},
            "$inc": {"balance": -price}
        }
    )

    await update.message.reply_text(
        f"✅ You successfully bought *{character['name']}* from *{character['anime']}*.\nRemaining balance: ₹{balance - price}",
        parse_mode="Markdown"
    )

# Register handler
application.add_handler(CommandHandler("buy", buy))
