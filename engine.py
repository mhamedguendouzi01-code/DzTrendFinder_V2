import sqlite3
from datetime import datetime

# دالة ذكية تنشئ الجداول إذا كانت غائبة لتفادي الأخطاء
def auto_init_db():
    conn = sqlite3.connect('dz_finder.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS global_radar 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, source_site TEXT, country TEXT, 
         price_original REAL, currency TEXT, price_usd REAL, url TEXT, image_url TEXT, date_added TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS sales_history 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, product_name TEXT, buy_price_usd REAL, 
         sell_price_usd REAL, profit_usd REAL, sale_date TEXT)''')
    conn.commit()
    conn.close()

def add_to_radar(name, site, country, price, currency, url, image_url=""):
    auto_init_db()
    rates = {"USD": 1.0, "EUR": 1.08, "CNY": 0.14, "JPY": 0.0067, "DZD": 0.0044}
    price_in_usd = price * rates.get(currency, 1.0)
    # صورة افتراضية إذا كان الرابط فارغ
    img = image_url if image_url else "https://img.icons8.com/nolan/512/globe.png"

    try:
        conn = sqlite3.connect('dz_finder.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO global_radar 
            (name, source_site, country, price_original, currency, price_usd, url, image_url, date_added)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            (name, site, country, price, currency, price_in_usd, url, img, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
    except Exception as e: print(f"Error: {e}")

def record_sale(item_id, sell_price_usd):
    auto_init_db()
    try:
        conn = sqlite3.connect('dz_finder.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, price_usd FROM global_radar WHERE id=?", (item_id,))
        item = cursor.fetchone()
        if item:
            profit = sell_price_usd - item[1]
            cursor.execute("INSERT INTO sales_history (product_name, buy_price_usd, sell_price_usd, profit_usd, sale_date) VALUES (?, ?, ?, ?, ?)",
                (item[0], item[1], sell_price_usd, profit, datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
        conn.close()
    except Exception as e: print(f"Error: {e}")