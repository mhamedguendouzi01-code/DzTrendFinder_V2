import sqlite3
from datetime import datetime

def auto_hunter():
    conn = sqlite3.connect('dz_finder.db')
    cursor = conn.cursor()
    
    # سلع تجريبية بالإنجليزية
    items = [
        {
            "title": "Baseus 65W GaN Fast Charger",
            "promo_price": 6000, 
            "market_price": 10000, 
            "image_url": "https://ae01.alicdn.com/kf/S728f7311749548f0a026e6f1a8302066P.jpg",
            "options": "Electronics"
        },
        {
            "title": "RGB Mechanical Wireless Keyboard",
            "promo_price": 9000, 
            "market_price": 15000,
            "image_url": "https://ae01.alicdn.com/kf/S26667749004144e393a5628b03126f98u.jpg",
            "options": "Gaming"
        }
    ]

    for itm in items:
        cursor.execute('''INSERT OR REPLACE INTO products 
            (title, promo_price, market_price, image_url, options, added_at)
            VALUES (?, ?, ?, ?, ?, ?)''', 
            (itm['title'], itm['promo_price'], itm['market_price'], 
             itm['image_url'], itm['options'], datetime.now()))
    
    conn.commit()
    conn.close()