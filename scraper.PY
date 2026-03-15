import sqlite3
from datetime import datetime

def auto_hunter():
    conn = sqlite3.connect('dz_finder.db')
    cursor = conn.cursor()
    items = [
        {
            "title": "Smart Watch Ultra 2 - AMOLED",
            "promo_price": 2900, "market_price": 4500,
            "image_url": "https://ae01.alicdn.com/kf/S7b8c7b6058864770b5610058e0a1122fI.jpg",
            "options": "Electronics", "rating": 4.9
        },
        {
            "title": "Lenovo LP40 Pro Original",
            "promo_price": 1850, "market_price": 3200,
            "image_url": "https://ae01.alicdn.com/kf/S26667749004144e393a5628b03126f98u.jpg",
            "options": "Audio", "rating": 4.7
        }
    ]
    for itm in items:
        cursor.execute('''INSERT OR REPLACE INTO products 
            (title, promo_price, market_price, image_url, options, rating, added_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)''', 
            (itm['title'], itm['promo_price'], itm['market_price'], 
             itm['image_url'], itm['options'], itm['rating'], datetime.now()))
    conn.commit()
    conn.close()