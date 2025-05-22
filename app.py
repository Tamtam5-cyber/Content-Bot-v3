import os
from flask import Flask, request, render_template
import telegram

app = Flask(__name__)
bot = telegram.Bot(token=os.environ.get("BOT_TOKEN"))

@app.route("/webhook", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    if update.message:
        chat_id = update.message.chat.id
        if update.message.text == "/start":
            bot.sendMessage(chat_id=chat_id, text="Chào mừng bạn! Hãy đăng ký kênh trước khi sử dụng bot.")
    return "OK", 200

@app.route("/")
def welcome():
    return render_template("welcome.html")

if __name__ == "__main__":
    bot.setWebhook("https://content-bot-v3.onrender.com/webhook")
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
