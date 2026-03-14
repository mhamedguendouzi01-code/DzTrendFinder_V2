import sqlite3
from datetime import datetime

def init_smart_db():
    conn = sqlite3.connect('dz_finder.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS products')
    cursor.execute('''CREATE TABLE products 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT, 
                      market_price REAL, 
                      promo_price REAL, 
                      rating REAL, 
                      reviews_count INTEGER,
                      options TEXT, 
                      image_url TEXT, 
                      video_url TEXT,
                      url TEXT, 
                      added_at TIMESTAMP)''')
    conn.commit()
    conn.close()

def seed_data():
    # سلع تجريبية احترافية
    trends = [
        ('Smart Watch Ultra 9 Pro', 8500, 3800, 4.9, 1250, 'Orange, Black, Grey', 
         'https://ae01.alicdn.com/kf/S518c069b247a4690859664599557a552I.jpg', 
         'https://www.w3schools.com/html/mov_bbb.mp4', 'https://aliexpress.com'),
        
        ('Écouteurs F9 TWS Wireless', 2800, 1250, 4.8, 8900, 'Noir, Blanc, Bleu', 
         'https://ae01.alicdn.com/kf/H98363765181b4d089886295325565360f.jpg', 
         None, 'https://aliexpress.com'),
         
        ('Mini Projecteur LED HD', 9500, 4200, 4.7, 320, 'Silver, White', 
         'https://ae01.alicdn.com/kf/S32d56e01a8f343838271a0695029e06eE.jpg', 
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
    print("✅ قاعدة البيانات جاهزة بالسلع والفيديوهات!")

if __name__ == "__main__":
    init_smart_db()
    seed_data()