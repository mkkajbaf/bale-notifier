import os
from flask import Flask, request, jsonify
from telegram import Bot
import asyncio
import logging

# تنظیمات
BOT_TOKEN = os.environ.get('BOT_TOKEN', '1752261074:j5rgthcAR14epmyhNCmccuN74Na953lFSns')
YOUR_CHAT_ID = int(os.environ.get('YOUR_CHAT_ID', '1286421845'))
BASE_URL = "https://tapi.bale.ai/bot"

bot = Bot(token=BOT_TOKEN, base_url=BASE_URL)
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# تابع هوشمندسازی پیام
def make_message(data):
    order_id = data.get("order_id", "نامشخص")
    name = data.get("name", "بدون نام")
    phone = data.get("phone", "-")
    product = data.get("product", "نامشخص")
    amount = data.get("amount", "نامشخص")
    
    if int(str(amount).replace(",", "").replace(" ", "")) > 1500000:
        vip = "🚨 سفارش VIP – مبلغ بالا!"
    else:
        vip = "سفارش جدید"
    
    text = f"""
{vip}

شماره سفارش: {order_id}
نام مشتری: {name}
تلفن: {phone}
محصول: {product}
مبلغ: {amount} تومان

لینک Trickle: https://trickle.so/project/proj_243aH9Ytrlx
"""
    return text.strip()

# ارسال پیام به بله
async def send_to_bale(order_data):
    msg = make_message(order_data)
    try:
        await bot.send_message(chat_id=YOUR_CHAT_ID, text=msg)
        logging.info("نوتیفیکیشن ارسال شد ✅")
    except Exception as e:
        logging.error(f"خطا در ارسال: {e}")

# Webhook برای سفارش‌ها
@app.route('/new-order', methods=['POST'])
def webhook():
    data = request.get_json(silent=True) or {}
    logging.info(f"داده دریافت شد: {data}")
    asyncio.run(send_to_bale(data))
    return jsonify({"status": "ok", "message": "نوتیفیکیشن ارسال شد"}), 200

# صفحه اصلی برای تست (برای جلوگیری از 404)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    return "<h1>ربات نوتیفیکیشن بله فعاله ✅</h1><p>Webhook: /new-order</p><p>سفارشاتت رو از دست نده!</p>"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)