import os
import time
import requests
from flask import Flask, request

app = Flask(__name__)

# استبدل هذا بتوكن بوتك الحقيقي أو ضعه في Environment Variables في Render
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "ضع_توكن_البوت_هنا")

@app.route('/')
def home():
    return "BingX Bot & Radar is live 24/7!"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()
    if data and 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')
        
        if text == '/start':
            send_welcome_menu(chat_id)
            
    elif data and 'callback_query' in data:
        chat_id = data['callback_query']['message']['chat']['id']
        callback_data = data['callback_query']['data']
        
        if callback_data == 'btc_analysis':
            send_btc_analysis(chat_id)
        elif callback_data == 'main_menu':
            send_welcome_menu(chat_id)
            
    return 'ok', 200

def send_message(chat_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(url, json=payload)

def send_welcome_menu(chat_id):
    keyboard = {
        "inline_keyboard": [
            [{"text": "📊 تحليل السوق الشامل", "callback_data": "market_analysis"}],
            [{"text": "🪙 Bitcoin (BTC)", "callback_data": "btc_analysis"},
             {"text": "💎 Ethereum (ETH)", "callback_data": "eth_analysis"}],
            [{"text": "⚡ Solana (SOL)", "callback_data": "sol_analysis"},
             {"text": "📈 S&P 500 Index", "callback_data": "sp500"}]
        ]
    }
    text = (
        "🤖 مرحباً بك مجدداً في مركز القيادة والتحليل الذكي\n\n"
        "اختر من الأزرار بالأسفل لمتابعة السوق أو فحص العملات بدقة:"
    )
    send_message(chat_id, text, reply_markup=keyboard)

def send_btc_analysis(chat_id):
    keyboard = {
        "inline_keyboard": [
            [{"text": "💰 بيع العملة", "callback_data": "sell"},
             {"text": "🚀 شراء فوري 5$", "callback_data": "buy"}],
            [{"text": "🔄 تحديث التحليل", "callback_data": "btc_analysis"},
             {"text": "🔙 القائمة الرئيسية", "callback_data": "main_menu"}]
        ]
    }
    text = (
        "⚙️ *تحليل العملة: (BTC-USDT)*\n\n"
        "💵 السعر الحالي: 92400.0 USDT\n"
        "📊 التغير (24س): 0.5%+\n"
        "📉 مؤشر RSI: 50.0\n"
        "📌 الحالة الفنية: ⚖️ في منطقة استقرار\n\n"
        "👉 اختر الإجراء التنفيذي أو عد للقائمة:"
    )
    send_message(chat_id, text, reply_markup=keyboard)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
