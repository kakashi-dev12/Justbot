import telebot
from flask import Flask, request

API_TOKEN = 'YOUR_BOT_TOKEN'

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route(f'/{API_TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'OK', 200

@bot.message_handler(func=lambda m: True)
def reply_hi(message):
    bot.send_message(message.chat.id, "hi")

# Set webhook when deployed
import os
if 'RENDER' in os.environ:
    bot.remove_webhook()
    bot.set_webhook(url=f'https://YOUR_RENDER_URL/{API_TOKEN}')
else:
    # For local testing
    bot.polling()
