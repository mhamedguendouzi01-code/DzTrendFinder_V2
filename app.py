import streamlit as st
import sqlite3
import urllib.parse
from datetime import datetime

# 1. إعداد الصفحة
st.set_page_config(page_title="DzTrend Finder", layout="wide", initial_sidebar_state="collapsed")

# 2. الديزاين المودارن (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Poppins:wght@600;800&display=swap');
    .stApp { background-color: #f8f9fa; font-family: 'Cairo', sans-serif; }
    .header-box { text-align: center; padding: 20px; background: white; border-radius: 0 0 30px 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 30px; }
    .ali-card { background: white; border-radius: 20px; padding: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); text-align: center; transition: 0.3s; margin-bottom: 20px; border: 1px solid #eee; }
    .ali-card:hover { transform: translateY(-10px); border-color: #ff4747; }
    .ali-img { width: 100%; border-radius: 15px; aspect-ratio: 1/1; object-fit: cover; }
    .ali-price { font-family: 'Poppins'; font-size: 22px; font-weight: 800; color: #1a1a1a; margin: 5px 0; }
    .old-price { text-decoration: line-through; color: #999; font-size: 14px; }
    .shock-badge { background: #fff0f0; color: #ff4747; padding: 5px 10px; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block; }
    div.stButton > button { border-radius: 12px; font-weight: bold; width: 100%; background: white; border: 1px solid #ddd; height: 45px; }
    div.stButton > button:hover { background: #1a1a1a; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 3. وظائف جلب البيانات
def get_products():
    conn = sqlite3.connect('dz_finder.db')
    conn.row_factory = sqlite3.Row
    data = conn.execute("SELECT * FROM products ORDER BY added_at DESC").fetchall()
    conn.close()
    return data

if 'page' not in st.session_state: st.session_state.page = 'home'

# --- الصفحة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown('<div class="header-box"><h1>🔥 DzTrend Finder</h1><p>أفضل الهمزات في الجزائر</p></div>', unsafe_allow_html=True)
    products = get_products()
    if not products:
        st.info("المتجر فارغ، ادخل للوحة التحكم في الأسفل لصيد سلع جديدة.")
    
    cols = st.columns(5)
    for i, row in enumerate(products):
        discount = int(((row['market_price'] - row['promo_price']) / row['market_price']) * 100)
        with cols[i % 5]:
            st.markdown(f"""
                <div class="ali-card">
                    <img src="{row['image_url']}" class="ali-img">
                    <div style="font-size:13px; height:40px; overflow:hidden; margin-top:10px;">{row['title']}</div>
                    <div class="ali-price">{int(row['promo_price'])} DA</div>
                    <div class="old-price">{int(row['market_price'])} DA</div>
                    <div class="shock-badge">⚡ -{discount}%</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("عرض المنتج 🔍", key=f"btn_{row['id']}"):
                st.session_state.selected_id = row['id']
                st.session_state.page = 'detail'
                st.rerun()

# --- صفحة التفاصيل ---
elif st.session_state.page == 'detail':
    if st.button("⬅️ عودة للمتجر"):
        st.session_state.page = 'home'
        st.rerun()
    
    conn = sqlite3.connect('dz_finder.db')
    conn.row_factory = sqlite3.Row
    p = conn.execute("SELECT * FROM products WHERE id