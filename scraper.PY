import sqlite3
from datetime import datetime

def init_smart_db():
    conn = sqlite3.connect('dz_finder.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS products')
    cursor.execute('''CREATE TABLE products 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT, 
                      market_price REAL, -- السعر الأصلي في السوق
                      promo_price REAL,   -- السعر في AliExpress
                      rating REAL, 
                      reviews_count INTEGER,
                      options TEXT, 
                      image_url TEXT, 
                      url TEXT, 
                      added_at TIMESTAMP)''')
    conn.commit()
    conn.close()

def auto_generate_trends():
    # سلع تجريبية حقيقية تحت 2000 دج
    trends = [
        ('Écouteurs Bluetooth Pro F9', 3200, 1350, 4.8, 4520, 'Black, White', 'https://ae01.alicdn.com/kf/H98363765181b4d089886295325565360f.jpg', 'https://aliexpress.com'),
        ('Souris Gamer RGB Silent', 3800, 1750, 4.7, 850, 'RGB Edition', 'https://ae01.alicdn.com/kf/S32d56e01a8f343838271a0695029e06eE.jpg', 'https://aliexpress.com'),
        ('Mini Projecteur LED USB', 4800, 1950, 4.5, 120, 'Silver, Gold', 'https://ae01.alicdn.com/kf/S518c069b247a4690859664599557a552I.jpg', 'https://aliexpress.com'),
        ('Câble Magnetic 3-in-1', 1200, 450, 4.9, 12500, 'Red, Black', 'https://ae01.alicdn.com/kf/S7e0f2f1e685f4007b8971f464047c8f4O.jpg', 'https://aliexpress.com'),
        ('Support Tablette Pro', 2200, 1100, 4.6, 340, 'Universal Size', 'https://ae01.alicdn.com/kf/S2659e5b4f8d248b99c7d4206e236313b0.jpg', 'https://aliexpress.com'),
        ('Humidificateur USB LED', 2600, 1400, 4.4, 2100, 'White, Pink', 'https://ae01.alicdn.com/kf/S986958b4f8d248b99c7d4206e236313b0.jpg', 'https://aliexpress.com')
    ]
    
    conn = sqlite3.connect('dz_finder.db')
    cursor = conn.cursor()
    for t in trends:
        cursor.execute("""INSERT INTO products 
            (title, market_price, promo_price, rating, reviews_count, options, image_url, url, added_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], datetime.now()))
    
    conn.commit()
    conn.close()
    print("✅ تم تحديث قاعدة البيانات بنجاح!")

if __name__ == "__main__":
    init_smart_db()
    auto_generate_trends()