import sqlite3

def init_db():
    conn = sqlite3.connect('dz_finder.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS products')
    cursor.execute('CREATE TABLE products (title TEXT, price TEXT, image_url TEXT, url TEXT, platform TEXT)')
    conn.commit()
    conn.close()

def populate():
    # سلع AliExpress حقيقية
    items = [
        ('Smart Watch Ultra 9 Pro', '3,500 DA', 'https://ae01.alicdn.com/kf/S518c069b247a4690859664599557a552I.jpg', 'https://aliexpress.com', 'AliExpress'),
        ('Écouteurs F9 TWS Bluetooth', '1,400 DA', 'https://ae01.alicdn.com/kf/H98363765181b4d089886295325565360f.jpg', 'https://aliexpress.com', 'AliExpress'),
        ('Souris Gamer RGB Pro', '2,200 DA', 'https://ae01.alicdn.com/kf/S32d56e01a8f343838271a0695029e06eE.jpg', 'https://aliexpress.com', 'AliExpress'),
        ('Mini Projecteur Portable HD', '12,500 DA', 'https://ae01.alicdn.com/kf/S986958b4f8d248b99c7d4206e236313b0.jpg', 'https://aliexpress.com', 'AliExpress')
    ]
    conn = sqlite3.connect('dz_finder.db')
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?)", items)
    conn.commit()
    conn.close()
    print("✅ قاعدة البيانات تحديث بنجاح!")

if __name__ == "__main__":
    init_db()
    populate()