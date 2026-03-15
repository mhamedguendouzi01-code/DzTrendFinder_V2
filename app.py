import streamlit as st
import sqlite3
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="Global Trend Finder", layout="wide", page_icon="🌍")

# 2. كود Pinterest
st.markdown('<head><meta name="p:domain_verify" content="5de1caac797abccd2cd0b92e1cc47217"/></head>', unsafe_allow_html=True)

# 3. إدارة قاعدة البيانات
def init_db():
    conn = sqlite3.connect('dz_finder.db', check_same_thread=False)
    conn.execute('''CREATE TABLE IF NOT EXISTS products 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT, promo_price REAL, image_url TEXT, affiliate_link TEXT, added_at DATETIME)''')
    conn.commit()
    conn.close()

def get_products():
    conn = sqlite3.connect('dz_finder.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        res = conn.execute("SELECT * FROM products ORDER BY added_at DESC").fetchall()
    except:
        res = []
    conn.close()
    return res

init_db()

# 4. الواجهة الرئيسية
st.title("🌍 Global Trend Finder")
products = get_products()

if not products:
    st.info("👋 الموقع فارغ حالياً. أضف سلعاً من القائمة الجانبية.")
else:
    cols = st.columns(3)
    for i, row in enumerate(products):
        with cols[i % 3]:
            st.image(row['image_url'], use_container_width=True)
            st.subheader(row['title'])
            st.write(f"### ${row['promo_price']}")
            link = row['affiliate_link'] if row['affiliate_link'] else "https://s.click.aliexpress.com"
            st.link_button("🎁 Get Deal", link, use_container_width=True)

# 5. لوحة التحكم (هنا صرا الخطأ وسقمناه)
with st.sidebar:
    st.header("🔐 Admin Panel")
    pwd = st.text_input("Password", type="password")
    
    if pwd == "dz2026":
        st.success("Access Granted!")
        with st.form("add_form", clear_on_submit=True):
            t = st.text_input("Product Name")
            p = st.number_input("Price ($)", min_value=0.01)
            img = st.text_input("Image URL")
            aff = st.text_input("Affiliate Link")
            submit = st.form_submit_button("Publish Now")
            
            if submit:
                if t and img:
                    try:
                        conn = sqlite3.connect('dz_finder.db', check_same_thread=False)
                        # السطر اللي تحت راهو مكتوب بطريقة صحيحة 100%
                        sql = "INSERT INTO products (title, promo_price, image_url, affiliate_link, added_at) VALUES (?, ?, ?, ?, ?)"
                        conn.execute(sql, (t, p, img, aff, datetime.now()))
                        conn.commit()
                        conn.close()
                        st.success("✅ Published!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")