from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from shivu import application
from shivu.modules.storage import generated_codes, used_codes, user_balances

async def redeem(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text("Please provide a redeem code.\nUsage: /redeem <code>")
        return

    code = context.args[0].upper()

    # Check if code was already used
    if code in used_codes:
        await update.message.reply_text("This code has already been used.")
        return

    # Check if code is valid
    valid = False
    for owner_id, codes in generated_codes.items():
        if code in codes:
            valid = True
            break

    if not valid:
        await update.message.reply_text("Invalid redeem code.")
        return

    # Mark code as used
    used_codes.add(code)

    # Add balance
    user_balances[user_id] = user_balances.get(user_id, 0) + 400

    await update.message.reply_text(
        f"✅ Code redeemed successfully!\n₹400 added to your balance.\nYour new balance: ₹{user_balances[user_id]}"
    )

application.add_handler(CommandHandler("redeem", redeem))
