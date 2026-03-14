import sqlite3
from datetime import datetime, timedelta

def init_smart_db():
    conn = sqlite3.connect('dz_finder.db')
    cursor = conn.cursor()
    # إنشاء جدول مطور يدعم نظام الـ 24 ساعة والبرومو
    cursor.execute('DROP TABLE IF EXISTS products')
    cursor.execute('''CREATE TABLE products 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT, 
                      original_price REAL, 
                      promo_price REAL, 
                      discount_percent TEXT,
                      image_url TEXT, 
                      url TEXT, 
                      coins_eligible INTEGER,
                      added_at TIMESTAMP)''')
    conn.commit()
    conn.close()

def fetch_top_deals():
    # هنا محاكاة لجلب سلع فيها تخفيض كبير (في المستقبل نربطوها بـ API)
    # الـ Coins تزيد تنقص في السومة
    deals = [
        ('SAMSUNG Galaxy Watch 6', 45000, 28000, '38%', 'https://m.media-amazon.com/images/I/61S985V5tBL._AC_SL1500_.jpg', 'https://aliexpress.com', 1, datetime.now()),
        ('Baseus GaN5 Pro Charger', 8500, 4200, '50%', 'https://m.media-amazon.com/images/I/51p6oT129PL._AC_SL1500_.jpg', 'https://aliexpress.com', 1, datetime.now()),
        ('Xiaomi Mi Band 8', 12000, 6500, '45%', 'https://m.media-amazon.com/images/I/51Y0yO0pSXL._AC_SL1000_.jpg', 'https://aliexpress.com', 1, datetime.now()),
        ('SSD Kingston 1TB', 15000, 9500, '36%', 'https://m.media-amazon.com/images/I/71u0O6A7SXL._AC_SL1500_.jpg', 'https://aliexpress.com', 1, datetime.now()),
        ('Drone Mini 3 Pro', 180000, 135000, '25%', 'https://m.media-amazon.com/images/I/61-A76e27sL._AC_SL1500_.jpg', 'https://aliexpress.com', 1, datetime.now())
    ]
    
    conn = sqlite3.connect('dz_finder.db')
    cursor = conn.cursor()
    cursor.executemany('''INSERT INTO products 
                         (title, original_price, promo_price, discount_percent, image_url, url, coins_eligible, added_at) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', deals)
    conn.commit()
    conn.close()
    print(f"✅ تم صيد {len(deals)} همزة بنجاح!")

if __name__ == "__main__":
    init_smart_db()
    fetch_top_deals()