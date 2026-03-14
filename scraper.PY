import sqlite3
from datetime import datetime

def init_smart_db():
    conn = sqlite3.connect('dz_finder.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS products')
    cursor.execute('''CREATE TABLE products 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT, price REAL, 
                      image_url TEXT, url TEXT, 
                      added_at TIMESTAMP)''')
    conn.commit()
    conn.close()

def fetch_top_deals():
    # سلع حقيقية برومو وتحت 2000 دج
    deals = [
        ('Écouteurs F9 TWS (Promo)', 1450, 'https://ae01.alicdn.com/kf/H98363765181b4d089886295325565360f.jpg', 'https://aliexpress.com', datetime.now()),
        ('Souris Gamer RGB (Deal)', 1850, 'https://ae01.alicdn.com/kf/S32d56e01a8f343838271a0695029e06eE.jpg', 'https://aliexpress.com', datetime.now()),
        ('Câble USB-C Fast Charge', 650, 'https://ae01.alicdn.com/kf/S7e0f2f1e685f4007b8971f464047c8f4O.jpg', 'https://aliexpress.com', datetime.now()),
        ('Support Téléphone Auto', 1200, 'https://ae01.alicdn.com/kf/S518c069b247a4690859664599557a552I.jpg', 'https://aliexpress.com', datetime.now()),
        ('Adaptateur Bluetooth 5.3', 950, 'https://ae01.alicdn.com/kf/Sc9a2b7f87a8b4b1a8f4c549646459955F.jpg', 'https://aliexpress.com', datetime.now()),
        ('Mini Lampe LED USB', 450, 'https://ae01.alicdn.com/kf/S986958b4f8d248b99c7d4206e236313b0.jpg', 'https://aliexpress.com', datetime.now())
    ]
    # فلتر إضافي للتأكد (فقط أقل من 2000 دج)
    filtered_deals = [d for d in deals if d[1] <= 2000]
    
    conn = sqlite3.connect('dz_finder.db')
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO products (title, price, image_url, url, added_at) VALUES (?, ?, ?, ?, ?)", filtered_deals)
    conn.commit()
    conn.close()
    print(f"✅ تم تسجيل {len(filtered_deals)} منتجات تحت 2000 دج!")

if __name__ == "__main__":
    init_smart_db()
    fetch_top_deals()