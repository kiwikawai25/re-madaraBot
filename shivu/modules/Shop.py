from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

RARITY_LABELS = {
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

@Client.on_message(filters.command("shop"))
async def shop_command(client, message):
    buttons = []
    for key, label in RARITY_LABELS.items():
        buttons.append([InlineKeyboardButton(text=label, callback_data=f"rarity_{key}")])

    await message.reply(
        "**Choose Your Waifu Rarity**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
