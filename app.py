import streamlit as st
import sqlite3
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="Global Deals Hub", layout="wide", page_icon="🛍️")

# 2. كود Pinterest
st.markdown('<head><meta name="p:domain_verify" content="5de1caac797abccd2cd0b92e1cc47217"/></head>', unsafe_allow_html=True)

# 3. قاعدة بيانات جديدة تماماً (بإسم جديد لتجاوز أي خطأ قديم)
def init_db():
    # غيرنا الإسم هنا باش السيرفر يفتح ملف جديد نظيف
    conn = sqlite3.connect('shop_v1.db', check_same_thread=False)
    conn.execute('''CREATE TABLE IF NOT EXISTS products 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT, promo_price REAL, image_url TEXT, 
                    affiliate_link TEXT, platform TEXT, added_at DATETIME)''')
    conn.commit()
    conn.close()

def get_products():
    conn = sqlite3.connect('shop_v1.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        res = conn.execute("SELECT * FROM products ORDER BY added_at DESC").fetchall()
    except:
        res = []
    conn.close()
    return res

init_db()

# 4. الواجهة الرئيسية
st.title("🌍 Global Deals Hub")
st.write("### Discover Viral Gadgets: Amazon, AliExpress & Temu")
st.divider()

products = get_products()

if not products:
    st.info("👋 السيت راهو واجد ونظيف. عمر أول سلعة من الـ Sidebar!")
else:
    cols = st.columns(3)
    for i, row in enumerate(products):
        with cols[i % 3]:
            st.image(row['image_url'], use_container_width=True)
            st.subheader(row['title'])
            st.markdown(f"## ${row['promo_price']:.2f}")
            plat = row['platform'] if row['platform'] else "AliExpress"
            st.link_button(f"Buy on {plat}", row['affiliate_link'], use_container_width=True)
            st.write("---")

# 5. لوحة التحكم
with st.sidebar:
    st.header("🔐 Admin Panel")
    pwd = st.text_input("Password", type="password")
    if pwd == "dz2026":
        st.success("Access Granted!")
        with st.form("add_form", clear_on_submit=True):
            t = st.text_input("Product Title")
            p = st.number_input("Price ($)", min_value=0.01)
            img = st.text_input("Image URL")
            aff = st.text_input("Affiliate Link")
            plat = st.selectbox("Platform", ["AliExpress", "Amazon", "Temu", "eBay"])
            submit = st.form_submit_button("Publish Now")
            
            if submit and t and img:
                try:
                    conn = sqlite3.connect('shop_v1.db', check_same_thread=False)
                    conn.execute("INSERT INTO products (title, promo_price, image_url, affiliate_link, platform, added_at) VALUES (?, ?, ?, ?, ?, ?)",
                                 (t, p, img, aff, plat, datetime.now()))
                    conn.commit()
                    conn.close()
                    st.success("✅ Published!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")