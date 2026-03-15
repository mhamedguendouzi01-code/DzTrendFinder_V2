import sqlite3
from datetime import datetime

def auto_hunter():
    conn = sqlite3.connect('dz_finder.db')
    cursor = conn.cursor()
    
    # سلع حقيقية بأسعارها وصورها
    real_deals = [
        {
            "title": "Smart Watch Ultra 2 - AMOLED Screen",
            "promo_price": 2950,
            "market_price": 4800,
            "image_url": "https://ae01.alicdn.com/kf/S7b8c7b6058864770b5610058e0a1122fI.jpg",
            "options": "Electronics",
            "rating": 4.9
        },
        {
            "title": "Lenovo LP40 Pro Original Earbuds",
            "promo_price": 1800,
            "market_price": 3500,
            "image_url": "https://ae01.alicdn.com/kf/S26667749004144e393a5628b03126f98u.jpg",
            "options": "Audio",
            "rating": 4.8
        },
        {
            "title": "Magnetic 3 in 1 Fast Charger",
            "promo_price": 650,
            "market_price": 1200,
            "image_url": "https://ae01.alicdn.com/kf/S728f7311749548f0a026e6f1a8302066P.jpg",
            "options": "Mobile Accessories",
            "rating": 4.5
        }
    ]

    for item in real_deals:
        cursor.execute('''INSERT OR REPLACE INTO products 
            (title, promo_price, market_price, image_url, options, rating, added_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)''', 
            (item['title'], item['promo_price'], item['market_price'], 
             item['image_url'], item['options'], item['rating'], datetime.now()))
    
    conn.commit()
    conn.close()