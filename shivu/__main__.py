import importlib
import time
import random
import re
import asyncio
from html import escape

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, filters, CallbackQueryHandler

from shivu import (
    collection, top_global_groups_collection, group_user_totals_collection,
    user_collection, user_totals_collection, shivuu, application,
    SUPPORT_CHAT, UPDATE_CHAT, db, LOGGER
)
from shivu.modules import (
    shop, upload, trade, start, ping, leaderboard,
    inlinequery, harem, changetime
)

locks = {}
message_counters = {}
spam_counters = {}
last_characters = {}
sent_characters = {}
first_correct_guesses = {}
message_counts = {}
last_user = {}
warned_users = {}

def escape_markdown(text):
    escape_chars = r'\*_`\\~>#+-=|{}.!'
    return re.sub(r'([%s])' % re.escape(escape_chars), r'\\\1', text)

async def message_counter(update: Update, context: CallbackContext) -> None:
    chat_id = str(update.effective_chat.id)
    user_id = update.effective_user.id

    if chat_id not in locks:
        locks[chat_id] = asyncio.Lock()
    lock = locks[chat_id]

    async with lock:
        chat_frequency = await user_totals_collection.find_one({'chat_id': chat_id})
        message_frequency = chat_frequency.get('message_frequency', 100) if chat_frequency else 100

        if chat_id in last_user and last_user[chat_id]['user_id'] == user_id:
            last_user[chat_id]['count'] += 1
            if last_user[chat_id]['count'] >= 10:
                if user_id in warned_users and time.time() - warned_users[user_id] < 600:
                    return
                await update.message.reply_text(f"⚠️ Don't Spam {update.effective_user.first_name}...\nYour Messages Will be ignored for 10 Minutes...")
                warned_users[user_id] = time.time()
                return
        else:
            last_user[chat_id] = {'user_id': user_id, 'count': 1}

        message_counts[chat_id] = message_counts.get(chat_id, 0) + 1

        if message_counts[chat_id] % message_frequency == 0:
            await send_image(update, context)
            message_counts[chat_id] = 0

async def send_image(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    all_characters = list(await collection.find({}).to_list(length=None))

    if chat_id not in sent_characters:
        sent_characters[chat_id] = []

    if len(sent_characters[chat_id]) == len(all_characters):
        sent_characters[chat_id] = []

    character = random.choice([c for c in all_characters if c['id'] not in sent_characters[chat_id]])
    sent_characters[chat_id].append(character['id'])
    last_characters[chat_id] = character

    if chat_id in first_correct_guesses:
        del first_correct_guesses[chat_id]

    await context.bot.send_photo(
        chat_id=chat_id,
        photo=character['img_url'],
        caption=f"""A New {character['rarity']} Character Appeared...\n/guess Character Name and add in Your Harem""",
        parse_mode='Markdown'
    )

async def guess(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if chat_id not in last_characters:
        return

    if chat_id in first_correct_guesses:
        await update.message.reply_text('❌️ Already Guessed By Someone.. Try Next Time Bruhh ')
        return

    guess = ' '.join(context.args).lower() if context.args else ''

    if "()" in guess or "&" in guess.lower():
        await update.message.reply_text("Nahh You Can't use This Types of words in your guess..❌️")
        return

    name_parts = last_characters[chat_id]['name'].lower().split()

    if sorted(name_parts) == sorted(guess.split()) or any(part == guess for part in name_parts):
        first_correct_guesses[chat_id] = user_id
        user = await user_collection.find_one({'id': user_id})
        if user:
            await user_collection.update_one({'id': user_id}, {'$push': {'characters': last_characters[chat_id]}})
        else:
            await user_collection.insert_one({
                'id': user_id,
                'username': update.effective_user.username,
                'first_name': update.effective_user.first_name,
                'characters': [last_characters[chat_id]],
            })
        await update.message.reply_text(f"You guessed right and received {last_characters[chat_id]['name']}")

async def fav(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text('Please provide Character id...')
        return

    character_id = context.args[0]
    user = await user_collection.find_one({'id': user_id})
    if not user:
        await update.message.reply_text('You have not Guessed any characters yet....')
        return

    character = next((c for c in user['characters'] if c['id'] == character_id), None)
    if not character:
        await update.message.reply_text('This Character is Not In your collection')
        return

    user['favorites'] = [character_id]
    await user_collection.update_one({'id': user_id}, {'$set': {'favorites': user['favorites']}})
    await update.message.reply_text(f'Character {character["name"]} has been added to your favorite...')

def main() -> None:
    application.add_handler(CommandHandler(["guess", "protecc", "collect", "grab", "hunt"], guess))
    application.add_handler(CommandHandler("fav", fav))
    
    # Shop and game-related commands
    application.add_handler(CommandHandler("shop", shop.shop))
    application.add_handler(CommandHandler("buy", shop.buy))
    application.add_handler(CommandHandler("bal", shop.bal))
    application.add_handler(CommandHandler("gen", shop.gen))
    application.add_handler(CommandHandler("dgen", shop.dgen))
    application.add_handler(CommandHandler("sell", shop.sell))
    application.add_handler(CommandHandler("redeem", shop.redeem))
    application.add_handler(CallbackQueryHandler(shop.handle_rarity_click, pattern=r"^rarity_\d+$"))

    # Extra modules
    application.add_handler(CommandHandler("upload", upload.upload))
    application.add_handler(CommandHandler("delete", upload.delete))
    application.add_handler(CommandHandler("update", upload.update))

    application.add_handler(CommandHandler("trade", trade.trade))
    application.add_handler(CommandHandler("accept", trade.accept))
    application.add_handler(CommandHandler("decline", trade.decline))

    application.add_handler(CommandHandler("start", start.start))
    application.add_handler(CommandHandler("ping", ping.ping))

    application.add_handler(CommandHandler("leaderboard", leaderboard.leaderboard))
    application.add_handler(CommandHandler("top", leaderboard.top))
    application.add_handler(CommandHandler("gtop", leaderboard.gtop))

    application.add_handler(CommandHandler("harem", harem.harem))
    application.add_handler(CommandHandler("collection", harem.collection))
    application.add_handler(CallbackQueryHandler(harem.harem_callback, pattern=r"^harem_"))

    application.add_handler(MessageHandler(filters.ALL, message_counter))

    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    shivuu.start()
    LOGGER.info("Bot started")
    main()
