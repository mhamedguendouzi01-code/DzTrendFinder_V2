import sqlite3

def clean_database():
    conn = sqlite3.connect('dz_finder.db')
    cursor = conn.cursor()
    # مسح كل السلع القديمة
    cursor.execute("DELETE FROM products")
    conn.commit()
    conn.close()
    print("✅ Database cleaned! Ready for global products.")

if __name__ == "__main__":
    clean_database()