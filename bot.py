import os
import requests
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

# ===== CONFIG =====
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Railway env variable
API_KEY = "DEMO"  # Yaha apni real API key daal sakte ho

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("📱 Number Info", callback_data="number"),
            InlineKeyboardButton("🚗 Vehicle Info", callback_data="vehicle"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "✨ Stylish Lookup Bot ✨\n\n"
        "Neeche option select karo 👇\n\n"
        "👨‍💻 Devloper :- Alok Yadav",
        reply_markup=reply_markup
    )

# ===== BUTTON =====
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "number":
        context.user_data["mode"] = "number"
        await query.edit_message_text(
            "📱 Mobile number bhejo lookup ke liye\n\n"
            "👨‍💻 Devloper :- Alok Yadav"
        )

    elif query.data == "vehicle":
        context.user_data["mode"] = "vehicle"
        await query.edit_message_text(
            "🚗 Vehicle number bhejo lookup ke liye\n\n"
            "👨‍💻 Devloper :- Alok Yadav"
        )

# ===== LOADING =====
async def loading(msg):
    frames = ["⚡ Data fetch ho raha hai...",
              "⚡ Thoda wait karo...",
              "⚡ Almost done..."]
    for frame in frames:
        await msg.edit_text(frame)
        await asyncio.sleep(0.7)

# ===== HANDLE =====
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    mode = context.user_data.get("mode")

    if not mode:
        await update.message.reply_text("❗ Pehle /start dabao aur option select karo.")
        return

    msg = await update.message.reply_text("🚀 Lookup start ho raha hai...")
    await loading(msg)

    try:
        if mode == "number":
            url = f"https://devil-api.elementfx.com/api/num-info.php?key={API_KEY}&phone={text}"

        elif mode == "vehicle":
            url = f"https://devil-api.elementfx.com/api/vehicle.php?key={API_KEY}&vehicle={text}"

        response = requests.get(url, timeout=10)
        result = response.text

        await msg.edit_text(
            f"📊 RESULT 👇\n\n`json\n{result}\n```\n\n"
            "👨‍💻 Devloper :- Alok Yadav",
            parse_mode="Markdown"
        )

    except Exception as e:
        await msg.edit_text(
            "❌ Data fetch nahi ho paya.\n\n"
            "👨‍💻 Devloper :- Alok Yadav"
        )

# ===== RUN =====
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("✅ Bot Railway pe chal raha hai...")
app.run_polling()
