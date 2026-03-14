import sqlite3
from datetime import datetime

def init_smart_db():
    conn = sqlite3.connect('dz_finder.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS products')
    cursor.execute('''CREATE TABLE products 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT, market_price REAL, promo_price REAL, 
                      rating REAL, reviews_count INTEGER,
                      options TEXT, image_url TEXT, video_url TEXT,
                      url TEXT, added_at TIMESTAMP)''')
    conn.commit()
    conn.close()

def seed_real_deals():
    # سلع حقيقية ومختارة بعناية (أسعار تقريبية بالدينار حسب سعر AliExpress)
    trends = [
        # 1. سماعات Lenovo الشهيرة (الهمزة رقم 1)
        ('Lenovo LP40 Pro TWS Earphones', 3500, 1450, 4.9, 15000, 'Black, White, Pink, Blue', 
         'https://ae04.alicdn.com/kf/S5008d6d538e4428498f4806140510652W.jpg', 
         'https://video.aliexpress-media.com/play/u/ae_sg_item/2213155705353/p/1/e/6/t/103/2213155705353.mp4', 
         'https://aliexpress.com'),
        
        # 2. ساعة ذكية شبيهة بـ Ultra
        ('Smart Watch Ultra 8 Series', 4500, 1850, 4.7, 5200, 'Orange, Black, Ocean Band', 
         'https://ae04.alicdn.com/kf/S8f96996d19454178a9c80f4f9d0c6488M.jpg', 
         None, 'https://aliexpress.com'),
         
        # 3. مصباح LED حساس للحركة (للمنزل)
        ('Motion Sensor LED Night Light', 1200, 450, 4.8, 8500, 'Warm White, Cold White', 
         'https://ae04.alicdn.com/kf/S986958b4f8d248b99c7d4206e236313b0.jpg', 
         'https://video.aliexpress-media.com/play/u/ae_sg_item/2215358055047/p/1/e/6/t/103/2215358055047.mp4', 
         'https://aliexpress.com'),

        # 4. ماكينة حلاقة Vintage T9 (الأكثر مبيعاً)
        ('Professional T9 Hair Clipper', 2800, 1200, 4.6, 12000, 'Gold, Black, Dragon Style', 
         'https://ae04.alicdn.com/kf/S32d56e01a8f343838271a0695029e06eE.jpg', 
         None, 'https://aliexpress.com'),

        # 5. جهاز بخار للوجه (USB)
        ('Nano Mist Sprayer - Facial Steamer', 1500, 650, 4.5, 3400, 'Pink, White', 
         'https://ae04.alicdn.com/kf/S2659e5b4f8d248b99c7d4206e236313b0.jpg', 
         None, 'https://aliexpress.com'),

        # 6. كابل شحن سريع 3 في 1
        ('3 in 1 Magnetic Fast Charging Cable', 900, 350, 4.9, 25000, 'Red, Silver, Black', 
         'https://ae04.alicdn.com/kf/S7e0f2f1e685f4007b8971f464047c8f4O.jpg', 
         None, 'https://aliexpress.com')
    ]
    
    conn = sqlite3.connect('dz_finder.db')
    cursor = conn.cursor()
    for t in trends:
        cursor.execute("""INSERT INTO products 
            (title, market_price, promo_price, rating, reviews_count, options, image_url, video_url, url, added_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], datetime.now()))
    conn.commit()
    conn.close()
    print("✅ تم حلب 6 همزات حقيقية بنجاح!")

if __name__ == "__main__":
    init_smart_db()
    seed_real_deals()