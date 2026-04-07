import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8344010103:AAFRJHcm1BfI3TEWf4emhN9_y3AE8O1YaL0"
CHATBOT_API = "https://api.affiliateplus.xyz/api/chatbot?message={msg}&botname=AI&ownername=UserAs_live"
IMAGE_API = "https://api.affiliateplus.xyz/api/imagegen?text={msg}&type=neon"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("नमस्ते! मुझसे बात करें या 'image: टेक्स्ट' लिखकर इमेज जनरेट करें।")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    chat_id = update.message.chat_id

    if text.lower().startswith("image:"):
        query = text[6:].strip()
        image_url = IMAGE_API.format(msg=requests.utils.quote(query))
        await context.bot.send_photo(chat_id=chat_id, photo=image_url)
    else:
        url = CHATBOT_API.format(msg=requests.utils.quote(text))
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            reply = data.get("message", "माफ़ करें, जवाब नहीं मिला।")
            await update.message.reply_text(reply)
        else:
            await update.message.reply_text("सर्वर से जवाब नहीं मिला, कृपया बाद में प्रयास करें।")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot चालू है...")
    app.run_polling()
