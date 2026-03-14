import sqlite3

def init_db():
    conn = sqlite3.connect('dz_finder.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS products')
    cursor.execute('CREATE TABLE products (title TEXT, price TEXT, image_url TEXT, url TEXT, platform TEXT)')
    conn.commit()
    conn.close()

def populate():
    # سلع مع روابط صور مضمونة (Amazon CDN) باش يبانوا دايما
    items = [
        ('Smart Watch Ultra 9 Pro', '3,500 DA', 'https://m.media-amazon.com/images/I/71u0O6A7SXL._AC_SL1500_.jpg', 'https://aliexpress.com', 'AliExpress'),
        ('Écouteurs F9 TWS Bluetooth', '1,400 DA', 'https://m.media-amazon.com/images/I/61NfU10XfTL._AC_SL1000_.jpg', 'https://aliexpress.com', 'AliExpress'),
        ('Souris Gamer RGB Pro', '2,200 DA', 'https://m.media-amazon.com/images/I/61lXG-G294L._AC_SL1500_.jpg', 'https://aliexpress.com', 'AliExpress'),
        ('Mini Projecteur Portable HD', '12,500 DA', 'https://m.media-amazon.com/images/I/61-A76e27sL._AC_SL1500_.jpg', 'https://aliexpress.com', 'AliExpress'),
        ('Console de Jeux R36S Retrogaming', '9,800 DA', 'https://m.media-amazon.com/images/I/710S9xXF-1L._AC_SL1500_.jpg', 'https://aliexpress.com', 'AliExpress')
    ]
    conn = sqlite3.connect('dz_finder.db')
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?)", items)
    conn.commit()
    conn.close()
    print("✅ قاعدة البيانات تم تحديثها بنجاح مع الصور!")

if __name__ == "__main__":
    init_db()
    populate()