import streamlit as st
import sqlite3
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="Global Trend Finder", layout="wide")

# تصميم CSS خفيف ومودارن
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .card { background: white; border-radius: 15px; padding: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; }
    .price { color: #ff4b4b; font-size: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# دالة لجلب البيانات
def get_data():
    conn = sqlite3.connect('dz_finder.db')
    conn.row_factory = sqlite3.Row
    res = conn.execute("SELECT * FROM products ORDER BY added_at DESC").fetchall()
    conn.close()
    return res

st.title("🌍 Global Trend Finder")
st.write("Best Verified Deals from AliExpress")

products = get_data()
cols = st.columns(3)

for i, row in enumerate(products):
    with cols[i % 3]:
        with st.container():
            st.markdown(f'<div class="card">', unsafe_allow_html=True)
            st.image(row['image_url'], use_container_width=True)
            st.subheader(row['title'])
            # تحويل السعر للدولار (نقسم على 200 مثلاً)
            price_usd = row['promo_price'] / 200
            st.markdown(f'<p class="price">${price_usd:.2f}</p>', unsafe_allow_html=True)
            st.link_button("View Deal", "https://s.click.aliexpress.com/e/_xxxxx") # هنا تحط رابطك مبعد
            st.markdown('</div>', unsafe_allow_html=True)
            st.write("")

# لوحة التحكم (Admin)
with st.sidebar:
    st.header("🔐 Admin Panel")
    if st.text_input("Password", type="password") == "dz2026":
        if st.button("Refresh Deals"):
            import scraper
            scraper.auto_hunter()
            st.success("Updated!")
            st.rerun()