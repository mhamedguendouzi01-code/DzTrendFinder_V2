import sqlite3
from datetime import datetime
import random

def init_smart_db():
    conn = sqlite3.connect('dz_finder.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS products')
    cursor.execute('''CREATE TABLE products 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT, market_price REAL, promo_price REAL, 
                      rating REAL, reviews_count INTEGER,
                      options TEXT, image_url TEXT, url TEXT, 
                      added_at TIMESTAMP)''')
    conn.commit()
    conn.close()

def auto_generate_trends():
    # محاكاة لجلب سلع تراند حقيقية من AliExpress تحت 2000 دج
    trends = [
        ('Écouteurs Bluetooth Pro F9', 2900, 1350, 4.8, 4520, 'Black, White, Blue', 'https://ae01.alicdn.com/kf/H98363765181b4d089886295325565360f.jpg'),
        ('Souris Gamer RGB Silent', 3200, 1850, 4.7, 850, 'RGB Edition, Matte Black', 'https://ae01.alicdn.com/kf/S32d56e01a8f343838271a0695029e06eE.jpg'),
        ('Mini Projecteur LED USB', 4500, 1950, 4.5, 120, 'Silver, Gold', 'https://ae01.alicdn.com/kf/S518c069b247a4690859664599557a552I.jpg'),
        ('Câble Magnetic 3-in-1 Fast', 1500, 650, 4.9, 12500, 'Red, Black, Purple', 'https://ae01.alicdn.com/kf/S7e0f2f1e685f4007b8971f464047c8f4O.jpg'),
        ('Support Tablette Flexible', 2400, 1100, 4.6, 340, 'Universal Size', 'https://ae01.alicdn.com/kf/S2659e5b4f8d248b99c7d4206e236313b0.jpg'),
        ('Humidificateur d''air USB', 2100, 1450, 4.4, 2100, 'White, Pink, Mint', 'https://ae01.alicdn.com/kf/S986958b4f8d248b99c7d4206e236313b0.jpg'),
        ('Lampe de Bureau Tactile', 2800, 1750, 4.7, 560, 'Warm White, Cool White', 'https://ae01.alicdn.com/kf/S62d56e01a8f343838271a0695029e06eE.jpg'),
        ('Kit Nettoyage Airpods/Phone', 1200, 450, 4.8, 9800, 'Standard Kit', 'https://ae01.alicdn.com/kf/Sc9a2b7f87a8b4b1a8f4c549646459955F.jpg')
    ]
    
    conn = sqlite3.connect('dz_finder.db')
    cursor = conn.cursor()
    for t in trends:
        cursor.execute("""INSERT INTO products 
            (title, market_price, promo_price, rating, reviews_count, options, image_url, url, added_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (t[0], t[1], t[2], t[3], t[4], t[5], t[6], 'https://aliexpress.com', datetime.now()))
    
    conn.commit()
    conn.close()
    print(f"✅ تم تفعيل {len(trends)} همزة تراند في المنصة!")

if __name__ == "__main__":
    init_smart_db()
    auto_generate_trends()