import requests
import time
from datetime import datetime

BOT_TOKEN = "8690830864:AAEbijHNw5RIoEY4eailqjPk_C_3aS0N4Ig"
CHAT_ID = "6687877810"

def send_message(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def generate_signal():
    now = datetime.now()
    hour = now.hour

    if hour < 9 or hour > 15:
        return "⛔ Market Closed"

    if 9 <= hour < 11:
        return "🚀 BUY CE\nEntry: Market Price\nSL: 20 pts\nTarget: 40 pts"

    elif 11 <= hour < 13:
        return "⚠️ No Trade Zone"

    elif 13 <= hour < 15:
        return "📉 BUY PE\nEntry: Market Price\nSL: 20 pts\nTarget: 40 pts"

    else:
        return "⚠️ Avoid Late Trades"

def run_bot():
    signal = generate_signal()
    send_message(f"📊 NIFTY SIGNAL\n\n{signal}")

last_run = 0

while True:
    current_time = time.time()

    if current_time - last_run > 300:
        run_bot()
        last_run = current_time

    time.sleep(5)
