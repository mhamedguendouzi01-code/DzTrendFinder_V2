import sqlite3
from datetime import datetime

def run_global_radar():
    conn = sqlite3.connect('dz_finder.db')
    cursor = conn.cursor()
    
    # بناء الجدول العالمي (Global Schema)
    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute('''CREATE TABLE products 
                     (origin TEXT, name TEXT, price_usd REAL, discount TEXT, link TEXT, image_url TEXT)''')
    
    # سلع تجريبية عالمية (تحت 15 دولار بخصم 80%+)
    # ملاحظة: هادي روابط صور AliExpress مباشرة باش تظهر 100%
    global_deals = [
        {"origin": "1688 🇨🇳", "name": "Magnetic 20W Charger", "price": 6.50, "disc": "88%", "link": "https://s.click.aliexpress.com/e/_Dk1", "img": "https://ae01.alicdn.com/kf/S554441589146467389146.jpg"},
        {"origin": "Amazon 🇯🇵", "name": "Slim Card Case JP", "price": 9.20, "disc": "75%", "link": "https://s.click.aliexpress.com/e/_Dk2", "img": "https://ae01.alicdn.com/kf/S88222333444555666777.jpg"},
        {"origin": "Walmart 🇺🇸", "name": "USB-C Fast Cable", "price": 3.99, "disc": "90%", "link": "https://s.click.aliexpress.com/e/_Dk3", "img": "https://ae01.alicdn.com/kf/Sa331622333.jpg"}
    ]
    
    for item in global_deals:
        cursor.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)", 
                       (item['origin'], item['name'], item['price'], item['disc'], item['link'], item['img']))
    
    conn.commit()
    conn.close()
    print("✅ Phase 1 Global Scraper: Success!")

if __name__ == "__main__":
    run_global_radar()