# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

import os
from flask import Flask, render_template
from flask import Flask, request
import telegram

app = Flask(__name__)
bot = telegram.Bot(token="YOUR_BOT_TOKEN")

@app.route("/webhook", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    if update.message:
        chat_id = update.message.chat.id
        bot.sendMessage(chat_id=chat_id, text="Hello! Bot is running.")
    return "OK", 200

if __name__ == "__main__":
    bot.setWebhook(f"https://content-bot-v3.onrender.com/webhook")
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
app = Flask(__name__)

@app.route("/")
def welcome():
    # Render the welcome page with animated "Team SPY" text
    return render_template("welcome.html")

if __name__ == "__main__":
    # Default to port 5000 if PORT is not set in the environment
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
