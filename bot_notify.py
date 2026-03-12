import requests

TOKEN = "8541204652:AAFOHPhAzZ7Y-Lzsr2jA0KC5PDs9kEQ4Cb0"
CHAT_ID = "7740633620"

def notify_me(name, price, img_url):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    caption = f"🔔 **همزة حقيقية!**\n\n📦 المنتج: {name}\n💰 السعر: {price} دج"
    payload = {"chat_id": CHAT_ID, "photo": img_url, "caption": caption, "parse_mode": "Markdown"}
    requests.post(url, json=payload)