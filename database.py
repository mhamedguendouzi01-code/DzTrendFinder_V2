import sqlite3

def init_db():
    conn = sqlite3.connect('dz_finder.db')
    cursor = conn.cursor()
    
    # جدول الرادار (الهمزات اللي نلقاوهم برا)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS global_radar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            source_site TEXT,
            country TEXT,
            price_original REAL,
            currency TEXT,
            price_dzd REAL,
            url TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # جدول التتبع والمخزن (السلع اللي شريتها)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            buy_price_dzd REAL,
            tracking_no TEXT,
            current_location TEXT,
            shipping_status TEXT,
            order_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ تم تحديث قاعدة البيانات بنجاح!")

if __name__ == "__main__":
    init_db()