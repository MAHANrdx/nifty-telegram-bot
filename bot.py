import requests
import time

BOT_TOKEN = "8690830864:AAEbijHNw5RIoEY4eailqjPk_C_3aS0N4Ig"
CHAT_ID = "6687877810"

def send_message(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def strategy():
    send_message("🚀 Bot is LIVE! Waiting for signals...")

while True:
    strategy()
    time.sleep(300)
