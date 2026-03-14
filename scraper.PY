import sqlite3
from datetime import datetime

def init_smart_db():
    conn = sqlite3.connect('dz_finder.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS products')
    cursor.execute('''CREATE TABLE products 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT, original_price REAL, promo_price REAL, 
                      discount_percent TEXT, image_url TEXT, url TEXT, 
                      added_at TIMESTAMP)''')
    conn.commit()
    conn.close()

def fetch_top_deals():
    # استعملتلك روابط صور من سيرفرات قوية (Amazon/Google) باش نضمنوا يبانوا دكا
    deals = [
        ('Smart Watch Ultra 9 Pro', 8500, 4200, '50%', 'https://m.media-amazon.com/images/I/71u0O6A7SXL._AC_SL1500_.jpg', 'https://aliexpress.com', datetime.now()),
        ('Écouteurs F9 TWS', 3500, 1800, '48%', 'https://m.media-amazon.com/images/I/61NfU10XfTL._AC_SL1000_.jpg', 'https://aliexpress.com', datetime.now()),
        ('Souris Gamer RGB', 4500, 2200, '51%', 'https://m.media-amazon.com/images/I/61lXG-G294L._AC_SL1500_.jpg', 'https://aliexpress.com', datetime.now()),
        ('Mini Projecteur HD', 25000, 14500, '42%', 'https://m.media-amazon.com/images/I/61-A76e27sL._AC_SL1500_.jpg', 'https://aliexpress.com', datetime.now()),
        ('Clavier Mécanique RGB', 12000, 7500, '37%', 'https://m.media-amazon.com/images/I/61pS-f1vEBL._AC_SL1200_.jpg', 'https://aliexpress.com', datetime.now()),
        ('Console Retro R36S', 15000, 9800, '34%', 'https://m.media-amazon.com/images/I/710S9xXF-1L._AC_SL1500_.jpg', 'https://aliexpress.com', datetime.now())
    ]
    conn = sqlite3.connect('dz_finder.db')
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO products (title, original_price, promo_price, discount_percent, image_url, url, added_at) VALUES (?, ?, ?, ?, ?, ?, ?)", deals)
    conn.commit()
    conn.close()
    print("✅ السلع الجديدة جاهزة بالصور المضمونة!")

if __name__ == "__main__":
    init_smart_db()
    fetch_top_deals()