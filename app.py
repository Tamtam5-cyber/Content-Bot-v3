import os
import logging
import asyncio
from flask import Flask, request, render_template
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Update

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Khởi tạo bot
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

# Hàm xử lý cập nhật từ Telegram
async def handle_update(data):
    update = Update.de_json(data, bot)
    if update.message:
        chat_id = update.message.chat.id
        message_text = update.message.text
        logging.info(f"Received command: {message_text} from chat_id: {chat_id}")

        # Khởi tạo trạng thái nếu người dùng chưa có
        if chat_id not in user_channel_status:
            user_channel_status[chat_id] = False

        # Xử lý các lệnh
        if not user_channel_status[chat_id] and message_text != "/start":
            await bot.send_message(chat_id, "Vui lòng tham gia kênh trước khi sử dụng bot! Gửi /start để bắt đầu.")
            return

        if message_text == "/start":
            if not user_channel_status[chat_id]:
                keyboard = [
                    [InlineKeyboardButton("Tham Gia Kênh", url=CHANNEL_LINK)],
                    [InlineKeyboardButton("Tôi Đã Tham Gia", callback_data="confirm_join")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await bot.send_message(
                    chat_id=chat_id,
                    text="Chào mừng bạn đến với bot! 🎉\n\n"
                         "Để sử dụng bot, bạn cần tham gia kênh của chúng tôi trước. "
                         "Nhấn vào nút bên dưới để tham gia, sau đó nhấn 'Tôi Đã Tham Gia' để xác nhận.",
                    reply_markup=reply_markup
                )

                # Lấy và gửi ảnh avatar của người dùng
                user = update.message.from_user
                photos = await bot.get_user_profile_photos(user_id=user.id, limit=1)
                if photos.photos:
                    await bot.send_photo(chat_id=chat_id, photo=photos.photos[0][-1].file_id, caption=f"Đây là ảnh đại diện của bạn, {user.first_name}!")
            else:
                await bot.send_message(chat_id=chat_id, text="Bạn đã tham gia kênh! Gửi lệnh để sử dụng bot, ví dụ: /help, /download.")

        elif message_text == "/help":
            await bot.send_message(chat_id=chat_id, text="Danh sách lệnh:\n/start - Khởi động bot\n/help - Hiển thị trợ giúp\n/download - Tải nội dung từ link\n/batch - Trích xuất hàng loạt\n/login - Đăng nhập\n/logout - Đăng xuất\n/dl - Tải video\n/adl - Tải âm thanh")

        elif message_text == "/download" or message_text == "/dl":
            await bot.send_message(chat_id=chat_id, text="Vui lòng gửi link nội dung bạn muốn tải!")

        elif message_text == "/adl":
            await bot.send_message(chat_id=chat_id, text="Vui lòng gửi link âm thanh bạn muốn tải!")

        elif message_text == "/batch":
            await bot.send_message(chat_id=chat_id, text="Vui lòng gửi danh sách link để trích xuất hàng loạt!")

        elif message_text == "/login":
            await bot.send_message(chat_id=chat_id, text="Vui lòng gửi số điện thoại của bạn để đăng nhập!")

        elif message_text == "/logout":
            await bot.send_message(chat_id=chat_id, text="Bạn đã đăng xuất thành công!")

        elif message_text == "/status":
            await bot.send_message(chat_id=chat_id, text="Bạn đang sử dụng phiên bản miễn phí. Gửi /plan để xem các gói premium!")

        elif message_text == "/plan":
            await bot.send_message(chat_id=chat_id, text="Gói Premium:\n- Tải tệp 4GB\n- Tốc độ nhanh hơn\nLiên hệ admin để nâng cấp!")

        else:
            await bot.send_message(chat_id=chat_id, text="Lệnh không được hỗ trợ. Gửi /help để xem danh sách lệnh.")

    if update.callback_query:
        query = update.callback_query
        chat_id = query.message.chat.id
        callback_data = query.data

        if callback_data == "confirm_join":
            try:
                member = await bot.get_chat_member(CHANNEL_ID, chat_id)
                if member.status in ["member", "administrator", "creator"]:
                    user_channel_status[chat_id] = True
                    await bot.send_message(
                        chat_id=chat_id,
                        text="Cảm ơn bạn đã tham gia kênh! 🎉\n"
                             "Bây giờ bạn có thể sử dụng bot. Gửi /help để xem danh sách lệnh!"
                    )
                else:
                    await bot.send_message(
                        chat_id=chat_id,
                        text="Bạn chưa tham gia kênh. Vui lòng tham gia và thử lại!"
                    )
            except Exception as e:
                logging.error(f"Error checking channel membership: {e}")
                await bot.send_message(
                    chat_id=chat_id,
                    text="Có lỗi xảy ra. Vui lòng thử lại sau!"
                )

        await query.answer()

@app.route("/webhook", methods=["POST"])
def webhook():
    # Nhận dữ liệu từ Telegram
    data = request.get_json(force=True)
    if not data:
        return "No data received", 400

    try:
        # Tạo một coroutine để xử lý cập nhật
        loop = asyncio.get_event_loop()
        loop.create_task(handle_update(data))
        return "OK", 200
    except Exception as e:
        logging.error(f"Error processing webhook update: {e}")
        return "Error processing update", 500

@app.route("/")
def welcome():
    return render_template("welcome.html")

# Khởi động bot khi ứng dụng chạy
async def start_bot():
    async with bot:
        await bot.start()
        logging.info("Bot started successfully")
        await bot.set_webhook("https://content-bot-v3.onrender.com/webhook")

if __name__ == "__main__":
    # Khởi động bot trước khi chạy Flask
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
