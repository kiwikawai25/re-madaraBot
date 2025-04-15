from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler
from shivu import application, collection, user_collection
from shivu.modules.storage import user_balances, generated_characters, generated_codes, used_codes, cooldowns
import random
from datetime import datetime, timedelta

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

OWNER_ID = 8156600797

# /shop
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

# callback
async def handle_rarity_click(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    rarity_id = query.data.split("_")[1]
    rarity_name, price = RARITY_DETAILS.get(rarity_id, ("Unknown", 0))
    await query.message.reply_text(
        f"You selected *{rarity_name}* (Price: ₹{price})\n\nSend the character ID using /buy <id>",
        parse_mode="Markdown"
    )

# /buy
async def buy(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    args = context.args
    if not args:
        await update.message.reply_text("Usage: /buy <id>")
        return

    waifu_id = args[0]
    character = await collection.find_one({'id': waifu_id})
    if not character:
        await update.message.reply_text("Bro ID Invalid cuz... Not Uploaded")
        return

    rarity_label = character['rarity']
    price = None
    for key, (label, value) in RARITY_DETAILS.items():
        if rarity_label == label:
            price = value
            break
    if price is None:
        await update.message.reply_text("Error in character rarity.")
        return

    user = await user_collection.find_one({'id': user_id})
    balance = user.get("balance", 0) if user else 0
    if user_id in user_balances:
        balance = user_balances[user_id]

    if balance < price:
        await update.message.reply_text(f"Not enough balance. You need ₹{price}, but you have ₹{balance}")
        return

    user_balances[user_id] = balance - price
    await user_collection.update_one({'id': user_id}, {'$push': {'characters': character}}, upsert=True)
    await user_collection.update_one({'id': user_id}, {'$set': {'balance': user_balances[user_id]}}, upsert=True)

    await update.message.reply_text(f"Waifu {character['name']} bought for ₹{price}!")

# /bal
async def bal(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user = await user_collection.find_one({'id': user_id})
    balance = user.get("balance", 0) if user else 0
    if user_id in user_balances:
        balance = user_balances[user_id]
    await update.message.reply_text(f"Your WaifuCoin balance: ₹{balance}")

# /gen
def generate_code(length=12):
    return ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=length))

async def gen(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    now = datetime.now()

    if user_id not in cooldowns:
        cooldowns[user_id] = []

    cooldowns[user_id] = [t for t in cooldowns[user_id] if now - t < timedelta(hours=24)]

    if len(cooldowns[user_id]) >= 2:
        last_time = cooldowns[user_id][-1]
        if now - last_time < timedelta(hours=5):
            next_time = last_time + timedelta(hours=5)
            await update.message.reply_text(
                f"You've reached your limit. Next /gen available at {next_time.strftime('%H:%M:%S')}."
            )
            return

    code = generate_code()
    generated_codes[code] = 400
    cooldowns[user_id].append(now)

    await update.message.reply_text(
        f"Here is your redeem code: `{code}`\n\n₹400 has been added to the code!",
        parse_mode='Markdown'
    )

# /dgen
async def dgen(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    code = generate_code()
    generated_codes[code] = 1_000_000_000_000
    await update.message.reply_text(f"(OWNER) Generated waifu code: `{code}`", parse_mode='Markdown')

# /sell
async def sell(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text("Usage: /sell <id>")
        return

    char_id = context.args[0]
    user = await user_collection.find_one({'id': user_id})
    if not user or 'characters' not in user:
        await update.message.reply_text("No characters found.")
        return

    character = next((c for c in user['characters'] if c['id'] == char_id), None)
    if not character:
        await update.message.reply_text("You don't own this character.")
        return

    rarity_label = character['rarity']
    price = None
    for key, (label, value) in RARITY_DETAILS.items():
        if rarity_label == label:
            price = value
            break
    if price is None:
        await update.message.reply_text("Error in character rarity.")
        return

    await user_collection.update_one({'id': user_id}, {'$pull': {'characters': {'id': char_id}}})
    user_balances[user_id] = user_balances.get(user_id, user.get("balance", 0)) + price
    await user_collection.update_one({'id': user_id}, {'$set': {'balance': user_balances[user_id]}})
    await update.message.reply_text(f"Sold character {character['name']} for ₹{price}!")

# /redeem
async def redeem(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text("Usage: /redeem <code>")
        return

    code = context.args[0].upper()
    if code in used_codes:
        await update.message.reply_text("Code already used.")
        return

    if code not in generated_codes:
        await update.message.reply_text("Invalid redeem code.")
        return

    value = generated_codes[code]
    used_codes.add(code)
    user_balances[user_id] = user_balances.get(user_id, 0) + value
    await user_collection.update_one({'id': user_id}, {'$set': {'balance': user_balances[user_id]}})
    await update.message.reply_text(f"Code redeemed! ₹{value} added to your balance.")

# Register handlers
application.add_handler(CommandHandler("shop", shop))
application.add_handler(CommandHandler("buy", buy))
application.add_handler(CommandHandler("bal", bal))
application.add_handler(CommandHandler("gen", gen))
application.add_handler(CommandHandler("dgen", dgen))
application.add_handler(CommandHandler("sell", sell))
application.add_handler(CommandHandler("redeem", redeem))
application.add_handler(CallbackQueryHandler(handle_rarity_click, pattern=r"^rarity_\d+$"))
