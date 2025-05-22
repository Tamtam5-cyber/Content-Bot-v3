import os
import logging
from flask import Flask, request, render_template  # Thêm render_template vào import
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
bot = Client(
    "my_bot",
    api_id=os.environ.get("API_ID"),
    api_hash=os.environ.get("API_HASH"),
    bot_token=os.environ.get("BOT_TOKEN"),
    in_memory=True
)

# Dictionary để lưu trạng thái tham gia kênh
user_channel_status = {}

# Liên kết kênh Telegram
CHANNEL_LINK = "https://t.me/ultimatesmmnews"
CHANNEL_ID = "@ultimatesmmnews"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = bot.parse_update(request.get_json(force=True))
    if update.message:
        chat_id = update.message.chat.id
        message_text = update.message.text
        logging.info(f"Received command: {message_text} from chat_id: {chat_id}")

        # Khởi tạo trạng thái nếu người dùng chưa có
        if chat_id not in user_channel_status:
            user_channel_status[chat_id] = False

        # Xử lý các lệnh
        if not user_channel_status[chat_id] and message_text != "/start":
            bot.send_message(chat_id, "Vui lòng tham gia kênh trước khi sử dụng bot! Gửi /start để bắt đầu.")
            return "OK", 200

        if message_text == "/start":
            if not user_channel_status[chat_id]:
                keyboard = [
                    [InlineKeyboardButton("Tham Gia Kênh", url=CHANNEL_LINK)],
                    [InlineKeyboardButton("Tôi Đã Tham Gia", callback_data="confirm_join")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                bot.send_message(
                    chat_id=chat_id,
                    text="Chào mừng bạn đến với bot! 🎉\n\n"
                         "Để sử dụng bot, bạn cần tham gia kênh của chúng tôi trước. "
                         "Nhấn vào nút bên dưới để tham gia, sau đó nhấn 'Tôi Đã Tham Gia' để xác nhận.",
                    reply_markup=reply_markup
                )

                # Lấy và gửi ảnh avatar của người dùng
                user = update.message.from_user
                photos = bot.get_user_profile_photos(user_id=user.id, limit=1)
                if photos.photos:
                    bot.send_photo(chat_id=chat_id, photo=photos.photos[0][-1].file_id, caption=f"Đây là ảnh đại diện của bạn, {user.first_name}!")
            else:
                bot.send_message(chat_id=chat_id, text="Bạn đã tham gia kênh! Gửi lệnh để sử dụng bot, ví dụ: /help, /download.")

        elif message_text == "/help":
            bot.send_message(chat_id=chat_id, text="Danh sách lệnh:\n/start - Khởi động bot\n/help - Hiển thị trợ giúp\n/download - Tải nội dung từ link\n/batch - Trích xuất hàng loạt\n/login - Đăng nhập\n/logout - Đăng xuất\n/dl - Tải video\n/adl - Tải âm thanh")

        elif message_text == "/download" or message_text == "/dl":
            bot.send_message(chat_id=chat_id, text="Vui lòng gửi link nội dung bạn muốn tải!")

        elif message_text == "/adl":
            bot.send_message(chat_id=chat_id, text="Vui lòng gửi link âm thanh bạn muốn tải!")

        elif message_text == "/batch":
            bot.send_message(chat_id=chat_id, text="Vui lòng gửi danh sách link để trích xuất hàng loạt!")

        elif message_text == "/login":
            bot.send_message(chat_id=chat_id, text="Vui lòng gửi số điện thoại của bạn để đăng nhập!")

        elif message_text == "/logout":
            bot.send_message(chat_id=chat_id, text="Bạn đã đăng xuất thành công!")

        elif message_text == "/status":
            bot.send_message(chat_id=chat_id, text="Bạn đang sử dụng phiên bản miễn phí. Gửi /plan để xem các gói premium!")

        elif message_text == "/plan":
            bot.send_message(chat_id=chat_id, text="Gói Premium:\n- Tải tệp 4GB\n- Tốc độ nhanh hơn\nLiên hệ admin để nâng cấp!")

        else:
            bot.send_message(chat_id=chat_id, text="Lệnh không được hỗ trợ. Gửi /help để xem danh sách lệnh.")

    if update.callback_query:
        query = update.callback_query
        chat_id = query.message.chat.id
        callback_data = query.data

        if callback_data == "confirm_join":
            try:
                member = bot.get_chat_member(CHANNEL_ID, chat_id)
                if member.status in ["member", "administrator", "creator"]:
                    user_channel_status[chat_id] = True
                    bot.send_message(
                        chat_id=chat_id,
                        text="Cảm ơn bạn đã tham gia kênh! 🎉\n"
                             "Bây giờ bạn có thể sử dụng bot. Gửi /help để xem danh sách lệnh!"
                    )
                else:
                    bot.send_message(
                        chat_id=chat_id,
                        text="Bạn chưa tham gia kênh. Vui lòng tham gia và thử lại!"
                    )
            except Exception as e:
                logging.error(f"Error checking channel membership: {e}")
                bot.send_message(
                    chat_id=chat_id,
                    text="Có lỗi xảy ra. Vui lòng thử lại sau!"
                )

        query.answer()

    return "OK", 200

@app.route("/")
def welcome():
    return render_template("welcome.html")

if __name__ == "__main__":
    with bot:
        bot.set_webhook("https://content-bot-v3.onrender.com/webhook")
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
