import requests
from bs4 import BeautifulSoup
import sqlite3

def clean_image_url(url):
    """هاد الدالة تصلح الروابط الناقصة"""
    if not url:
        return "https://via.placeholder.com/200?text=No+Photo"
    if url.startswith('//'):
        return 'https:' + url
    return url

def save_to_db(product):
    conn = sqlite3.connect('dz_finder.db')
    cursor = conn.cursor()
    # تأكد من أن الجدول موجود
    cursor.execute('''CREATE TABLE IF NOT EXISTS products 
                     (title TEXT, price TEXT, image_url TEXT, url TEXT, platform TEXT)''')
    
    cursor.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?)", 
                   (product['title'], product['price'], product['image_url'], product['url'], product['platform']))
    conn.commit()
    conn.close()

def scrape_data():
    # هذا مثال فقط، عدل الروابط حسب واش راك تسكرابي
    url = "https://example.com/products" 
    headers = {"User-Agent": "Mozilla/5.0"}
    
    # هنا تبدأ عملية السكرابينغ (تأكد من الـ selectors تاعك)
    # ... كود السكرابينغ تاعك هنا ...
    
    # مثال كيفاش تريڨل رابط الصورة قبل ما تخزنو
    raw_img = "//img.alicdn.com/example.jpg" # مثال لرابط ناقص
    final_img = clean_image_url(raw_img)
    
    product_data = {
        'title': 'Product Name',
        'price': '10.50',
        'image_url': final_img,
        'url': 'https://example.com/p1',
        'platform': '1688'
    }
    save_to_db(product_data)

if __name__ == "__main__":
    scrape_data()
    print("✅ تم جلب البيانات وتصليح روابط الصور!")