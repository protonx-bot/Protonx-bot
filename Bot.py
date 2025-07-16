
# Import gulo
import json
from telegram.ext import Updater, CommandHandler
from flask import Flask
import threading
import os

# Bot token securely environment variable theke ashbe
TOKEN = os.getenv("TOKEN", "8075686130:AAFiewbewwwrq4SDIXle0aUPZCGxtuA3l7s")
DATA_FILE = 'user_data.json'
userData = {}

# File theke user data load korchi
try:
    with open(DATA_FILE, 'r') as f:
        userData = json.load(f)
except FileNotFoundError:
    pass

# User data save korar function
def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(userData, f, indent=2)

# /start command
def start(update, context):
    user_id = str(update.effective_user.id)
    if user_id not in userData:
        userData[user_id] = {"balance": 500}
        save_data()
        context.bot.send_message(chat_id=user_id, text="🎉 Welcome! You've received 500 PTX!")
    else:
        context.bot.send_message(chat_id=user_id, text="✅ You are already registered.")

# /balance command
def balance(update, context):
    user_id = str(update.effective_user.id)
    bal = userData.get(user_id, {}).get("balance", 0)
    context.bot.send_message(chat_id=user_id, text=f"💰 Your balance is: {bal} PTX")

# Bot setup
updater = Updater(token=TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("balance", balance))

# Flask app — keep alive jonne
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Flask thread e run korchi
threading.Thread(target=run_flask).start()

# Bot start
updater.start_polling()
print("🤖 Bot started and running!")
