import streamlit as st
import sqlite3
import urllib.parse

# إعدادات الصفحة
st.set_page_config(page_title="DzTrend | Intelligence Portal", layout="wide")

# --- CSS الاحترافي والمودارن ---
st.markdown("""
    <style>
    .stApp { background-color: #f7f9fc; }
    .modern-card {
        background: white; border-radius: 18px; padding: 15px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.04);
        border: 1px solid #f0f0f0; text-align: center;
        transition: transform 0.3s ease; position: relative;
    }
    .modern-card:hover { transform: translateY(-8px); box-shadow: 0 15px 30px rgba(0,0,0,0.08); }
    .discount-badge {
        position: absolute; top: 12px; left: 12px;
        background: linear-gradient(45deg, #ff4b2b, #ff416c);
        color: white; padding: 3px 10px; border-radius: 10px;
        font-weight: bold; font-size: 11px;
    }
    .product-img { width: 100%; height: 140px; object-fit: contain; margin-bottom: 12px; }
    .product-title { font-size: 13px; font-weight: 600; color: #333; height: 38px; overflow: hidden; }
    .rating { color: #f1c40f; font-size: 11px; margin-bottom: 8px; }
    .price-old { color: #a0a0a0; text-decoration: line-through; font-size: 10px; }
    .price-new { color: #2ecc71; font-size: 19px; font-weight: 800; margin: 4px 0; }
    .profit-info { background: #e3f2fd; color: #1976d2; font-size: 10px; font-weight: bold; padding: 2px 8px; border-radius: 6px; display: inline-block; }
    
    /* ستايل الأزرار */
    div.stButton > button {
        background: linear-gradient(to right, #2193b0, #6dd5ed);
        color: white; border: none; border-radius: 10px;
        font-weight: bold; width: 100%; height: 40px;
    }
    </style>
    """, unsafe_allow_html=True)

def load_data():
    try:
        conn = sqlite3.connect('dz_finder.db')
        conn.row_factory = sqlite3.Row
        data = conn.execute('SELECT * FROM products ORDER BY added_at DESC').fetchall()
        conn.close()
        return data
    except: return []

# الهيدر
st.markdown("<h1 style='text-align: center; color: #2c3e50;'>🛍️ DzTrend <span style='color: #2ecc71;'>Finder</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d; font-size: 14px;'>همزات حصرية تحت 2000 دج محسوبة بذكاء</p>", unsafe_allow_html=True)

products = load_data()

if not products:
    st.warning("⚠️ يرجى تشغيل سكريبت scraper.PY أولاً لتعبئة البيانات.")
else:
    cols = st.columns(6)
    for i, row in enumerate(products):
        # --- خوارزمية الفايدة الديناميكية ---
        mkt_p = row['market_price']
        prm_p = row['promo_price']
        
        # التوفير الحقيقي
        saving = mkt_p - prm_p
        discount_pct = int((saving / mkt_p) * 100)
        
        # الفايدة: 40% من قيمة التوفير (تزيد بزيادة البرومو)
        profit = int(saving * 0.40)
        
        # السعر النهائي للزبون
        final_price = int(prm_p + profit)

        with cols[i % 6]:
            with st.container():
                st.markdown(f'''
                    <div class="modern-card">
                        <div class="discount-badge">-{discount_pct}%</div>
                        <img src="{row['image_url']}" class="product-img" onerror="this.src='https://via.placeholder.com/150'">
                        <div class="product-title">{row['title']}</div>
                        <div class="rating">⭐ {row['rating']} ({row['reviews_count']})</div>
                        <div class="price-old">{mkt_p} DA</div>
                        <div class="price-new">{final_price} DA</div>
                        <div class="profit-info">💰 ربحك الصافي: +{profit} DA</div>
                    </div>
                ''', unsafe_allow_html=True)
                
                # زر الواتساب
                msg = f"سلام محمد، حاب نطلب: {row['title']}\nالسعر النهائي: {final_price} DA"
                wa_url = f"https://wa.me/213600000000?text={urllib.parse.quote(msg)}"
                st.link_button("🚀 اطلب الآن", wa_url)

st.divider()
st.caption("© 2026 DzTrend Intelligence - نظام الوساطة الذكي")