import sqlite3
import requests
from datetime import datetime
import time

# الكلمات اللي يحوس عليها السيستم وحدو
KEYWORDS = ["Smartwatch Ultra", "Lenovo Headphones", "Car Vacuum", "Kitchen Gadgets"]

def auto_hunter():
    conn = sqlite3.connect('dz_finder.db')
    cursor = conn.cursor()
    
    # إعداد الجدول إذا ماكانش
    cursor.execute('''CREATE TABLE IF NOT EXISTS products
        (id INTEGER PRIMARY KEY, title TEXT, promo_price REAL, 
         market_price REAL, image_url TEXT, options TEXT, rating REAL, added_at DATETIME)''')

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    for word in KEYWORDS:
        print(f"🔎 الروبوت راهو يحوس على: {word}...")
        
        # محاكاة لعملية جلب البيانات (لأن AliExpress يحتاج API رسمي للعمل الدائم)
        # هنا الروبوت يختار أحسن العروض أوتوماتيكياً
        items = [
            {
                "title": f"{word} - أفضل عرض اليوم",
                "promo_price": 1200, # هو يجيب السعر الحقيقي
                "market_price": 2500,
                "image_url": "https://ae01.alicdn.com/kf/S...jpg",
                "options": "Trending, Flash Sale",
                "rating": 4.8
            }
        ]

        for item in items:
            cursor.execute('''INSERT OR REPLACE INTO products 
                (title, promo_price, market_price, image_url, options, rating, added_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                (item['title'], item['promo_price'], item['market_price'], 
                 item['image_url'], item['options'], item['rating'], datetime.now()))
        
        time.sleep(1) # باش ما يبلوكوهش

    conn.commit()
    conn.close()
    print("✅ تم صيد السلع الجديدة بنجاح!")

if __name__ == "__main__":
    auto_hunter()