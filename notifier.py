import requests
import time

TOKEN = "8541204652:AAFOHPhAzZ7Y-Lzsr2jA0KC5PDs9kEQ4Cb0"
CHAT_ID = "7740633620"

def send_to_telegram(name, price, img_url, retries=3):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    caption = f"🚀 **همزة ترند جديدة!**\n\n📦 **المنتج:** {name}\n💰 **السعر:** {price} دج"
    payload = {"chat_id": CHAT_ID, "photo": img_url, "caption": caption, "parse_mode": "Markdown"}
    
    for i in range(retries):
        try:
            print(f"⏳ محاولة رقم {i+1} للاتصال بتيليغرام...")
            response = requests.post(url, json=payload, timeout=20)
            if response.status_code == 200:
                print(f"✅ تم إرسال التنبيه بنجاح!")
                return True
        except Exception as e:
            print(f"⚠️ فشل في المحاولة {i+1}: {e}")
            if i < retries - 1:
                time.sleep(5) # استراحة 5 ثواني قبل المحاولة الجاية
    print("❌ للأسف، تعذر الاتصال نهائياً. جرب تشغيل VPN أو تغيير الشبكة.")
    return False

if __name__ == "__main__":
    send_to_telegram("SAMSUNG S24 Ultra", 185000, "https://m.media-amazon.com/images/I/71RzaV6iS9L.jpg")