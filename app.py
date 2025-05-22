import os
from flask import Flask, render_template

# Khởi tạo app trước khi sử dụng
app = Flask(__name__)

# Định nghĩa route sau khi app đã được khởi tạo
@app.route("/")
def welcome():
    return render_template("welcome.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
