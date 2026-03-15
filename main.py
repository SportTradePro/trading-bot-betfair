from flask import Flask
import os
import threading
import asyncio
from telegram.ext import Application, CommandHandler
from telegram import Update
import time

app = Flask(__name__)

# Telegram BOT REALE
async def start(update: Update, context):
    await update.message.reply_text('🚀 Trading Bot Betfair LIVE ✅')

async def main():
    token = os.getenv('TG_TOKEN')
    if not token:
        print("❌ TG_TOKEN mancante")
        return
        
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

def run_telegram():
    asyncio.run(main())

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return '🚀 Trading Bot Betfair LIVE ✅'

@app.route('/health')
def health():
    return 'OK'

if __name__ == '__main__':
    print("🚀 Avvio bot...")
    # Telegram in thread
    telegram_thread = threading.Thread(target=run_telegram, daemon=True)
    telegram_thread.start()
    time.sleep(2)  # Aspetta bot
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
