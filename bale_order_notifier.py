from telegram import Bot
import asyncio
import logging
from flask import Flask, request, jsonify

# تنظیمات ثابت – دیگه هیچی عوض نکن
BOT_TOKEN = "1752261074:j5rgthcAR14epmyhNCmccuN74Na953lFSns"
YOUR_CHAT_ID = 1286421845          # آیدی خودت
BASE_URL = "https://tapi.bale.ai/bot"

bot = Bot(token=BOT_TOKEN, base_url=BASE_URL)
app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')

# تابع هوشمندسازی پیام با یه AI خیلی ساده
def make_message(data):
    order_id = data.get("order_id", "نامشخص")
    name = data.get("name", data.get("customer", "بدون نام"))
    phone = data.get("phone", data.get("mobile", "-"))
    amount = data.get("amount", data.get("price", "نامشخص"))
    product = data.get("product", data.get("item", "نامشخص"))

    if "میلیون" in str(amount) or int(str(amount).replace(",", "").replace(" ", "")) > 1500000:
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

لینک پروژه Trickle:
https://trickle.so/project/proj_243aH9Ytrlx
"""
    return text.strip()

# ارسال پیام به بله
async def send_to_bale(order_data):
    msg = make_message(order_data)
    try:
        await bot.send_message(chat_id=YOUR_CHAT_ID, text=msg)
        print("نوتیفیکیشن با موفقیت به بله ارسال شد ✅")
    except Exception as e:
        print("خطا در ارسال به بله:", e)

# Webhook که Trickle باید بهش POST کنه
@app.route('/new-order', methods=['POST'])
def webhook():
    data = request.get_json(silent=True) or {}
    print("داده دریافت شد:", data)
    
    asyncio.run(send_to_bale(data))
    
    return jsonify({"status": "ok", "message": "نوتیفیکیشن ارسال شد"}), 200

# صفحه تست ساده
@app.route('/')
def home():
    return """
    <h1>ربات نوتیفیکیشن بله فعاله ✅</h1>
    <p>Webhook آدرس: <code>https://آدرس-سرورت/new-order</code></p>
    <p>هر وقت سفارشی بیاد، مستقیم به بله‌ات پیام می‌دم!</p>
    """

if __name__ == "__main__":
    print("ربات بله فعال شد و منتظر سفارش‌هاست...")
    print("Webhook URL تو اینه:")
    print("   http://127.0.0.1:5000/new-order   (برای تست محلی)")
    app.run(host='0.0.0.0', port=5000, debug=False)