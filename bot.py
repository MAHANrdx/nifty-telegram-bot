import requests
import time
from datetime import datetime

BOT_TOKEN = "8690830864:AAEbijHNw5RIoEY4eailqjPk_C_3aS0N4Ig"
CHAT_ID = "6687877810"

last_update_id = None
trade_count = 0
MAX_TRADES = 5

def send_message(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def get_updates():
    global last_update_id
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    response = requests.get(url).json()

    if "result" in response:
        for update in response["result"]:
            update_id = update["update_id"]

            if last_update_id is None or update_id > last_update_id:
                last_update_id = update_id

                if "message" in update and "text" in update["message"]:
                    return update["message"]["text"]
    return None

def generate_signal():
    global trade_count

    now = datetime.now()
    hour = now.hour

    if trade_count >= MAX_TRADES:
        return "⛔ Trade limit reached (5/day)"

    if hour < 9 or hour > 15:
        return "⛔ Market Closed"

    if 9 <= hour < 11:
        trade_count += 1
        return f"🚀 BUY CE\nEntry: Market Price\nSL: 20 pts\nTarget: 40 pts\nTrades used: {trade_count}/5"

    elif 11 <= hour < 13:
        return "⚠️ No Trade Zone (Avoid sideways)"

    elif 13 <= hour < 15:
        trade_count += 1
        return f"📉 BUY PE\nEntry: Market Price\nSL: 20 pts\nTarget: 40 pts\nTrades used: {trade_count}/5"

    else:
        return "⚠️ Avoid Late Trades"

def process_command(cmd):
    if cmd == "/check":
        signal = generate_signal()
        send_message(f"📊 NIFTY SIGNAL\n\n{signal}")

    elif cmd == "/status":
        send_message(f"📈 Trades used today: {trade_count}/5")

    elif cmd == "/start":
        send_message("🤖 Bot Active!\nUse /check for signal")

def reset_trades_daily():
    global trade_count
    now = datetime.now()
    if now.hour == 0 and now.minute == 0:
        trade_count = 0

while True:
    cmd = get_updates()

    if cmd:
        process_command(cmd)

    reset_trades_daily()
    time.sleep(2)
