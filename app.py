import streamlit as st
import sqlite3
import urllib.parse
from datetime import datetime

# 1. إعداد الصفحة
st.set_page_config(page_title="DzTrend | أفضل الهمزات", layout="wide", initial_sidebar_state="collapsed")

# 2. الديزاين المودارن (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Poppins:wght@600;800&display=swap');
    .stApp { background-color: #f8f9fa; font-family: 'Cairo', sans-serif; }
    
    .ali-card { 
        background: white; border-radius: 20px; padding: 15px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); text-align: center; 
        transition: 0.3s; margin-bottom: 20px; border: 1px solid #eee;
    }
    .ali-card:hover { transform: translateY(-10px); border-color: #ff4747; }
    .ali-img { width: 100%; border-radius: 15px; aspect-ratio: 1/1; object-fit: cover; }
    
    /* تنسيق الأسعار */
    .price-container { margin: 10px 0; }
    .new-price { font-family: 'Poppins'; font-size: 22px; font-weight: 800; color: #ff4747; display: block; }
    .old-price { font-family: 'Poppins'; font-size: 14px; color: #999; text-decoration: line-through; display: block; }
    
    .shock-badge { 
        background: #ff4747; color: white; padding: 4px 10px; 
        border-radius: 8px; font-weight: bold; font-size: 11px; margin-top: 5px; display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

def get_products():
    conn = sqlite3.connect('dz_finder.db')
    conn.row_factory = sqlite3.Row
    data = conn.execute("SELECT * FROM products ORDER BY added_at DESC").fetchall()
    conn.close()
    return data

if 'page' not in st.session_state: st.session_state.page = 'home'

# --- الصفحة الرئيسية ---
if st.session_state.page == 'home':
    st.title("🔥 DzTrend Finder")
    products = get_products()
    
    cols = st.columns(5)
    for i, row in enumerate(products):
        # حساب نسبة التخفيض
        discount = int(((row['market_price'] - row['promo_price']) / row['market_price']) * 100)
        with cols[i % 5]:
            st.markdown(f'''
                <div class="ali-card">
                    <img src="{row['image_url']}" class="ali-img">
                    <div style="font-size:13px; height:35px; overflow:hidden; margin-top:10px;">{row['title']}</div>
                    <div class="price-container">
                        <span class="old-price">{int(row['market_price'])} DA</span>
                        <span class="new-price">{int(row['promo_price'])} DA</span>
                    </div>
                    <div class="shock-badge">تخفيض {discount}% 🔥</div>
                </div>
            ''', unsafe_allow_html=True)
            if st.button("تفاصيل الهمزة 🔍", key=f"btn_{row['id']}"):
                st.session_state.selected_id = row['id']
                st.session_state.page = 'detail'
                st.rerun()

# --- صفحة التفاصيل ---
elif st.session_state.page == 'detail':
    if st.button("⬅️ رجوع للمتجر"):
        st.session_state.page = 'home'
        st.rerun()
    
    conn = sqlite3.connect('dz_finder.db')
    conn.row_factory = sqlite3.Row
    p = conn.execute("SELECT * FROM products WHERE id = ?", (st.session_state.selected_id,)).fetchone()
    conn.close()

    if p:
        c1, c2 = st.columns(2)
        with c1:
            st.image(p['image_url'], use_container_width=True)
        with c2:
            st.markdown(f"""
                <div style="text-align:right; direction:rtl;">
                    <h1>{p['title']}</h1>
                    <p style="font-size: 20px; color: #777; text-decoration: line-through;">السعر الأصلي: {int(p['market_price'])} DA</p>
                    <h2 style="color: #ff4747; font-size: 40px;">السعر الجديد: {int(p['promo_price'])} DA</h2>
                    <hr>
                    <p>✅ ضمان الجودة</p>
                    <p>⭐ التقييم العالمي: {p['rating']}/5</p>
                </div>
            """, unsafe_allow_html=True)
            msg = urllib.parse.quote(f"سلام، حاب نطلب هاد المنتج: {p['title']}")
            st.link_button("🔥 اطلب دكا عبر واتساب", f"https://wa.me/213600000000?text={msg}")

# لوحة التحكم السرية
st.markdown("<br><hr>", unsafe_allow_html=True)
with st.expander("🔐 لوحة تحكم محمد"):
    if st.text_input("كلمة السر", type="password") == "dz2026":
        if st.button("🚀 صيد همزات حقيقية"):
            import scraper