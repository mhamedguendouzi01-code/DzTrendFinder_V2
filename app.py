import streamlit as st
import sqlite3
import urllib.parse

# إعداد الصفحة
st.set_page_config(page_title="DzTrend | Smart Finder", layout="wide")

# نسبة الفائدة تاعك
MY_PROFIT = 0.15

# --- CSS المودارن ---
st.markdown("""
    <style>
    /* خلفية الصفحة */
    .stApp { background-color: #f8f9fa; }
    
    /* تصميم كرت المنتج */
    .modern-card {
        background: white;
        border-radius: 20px;
        padding: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border: 1px solid rgba(0,0,0,0.03);
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
    }
    .modern-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    }
    
    /* شارة التخفيض */
    .discount-badge {
        position: absolute;
        top: 10px;
        left: 10px;
        background: linear-gradient(45deg, #FF4B2B, #FF416C);
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 12px;
        z-index: 10;
    }
    
    /* الصور */
    .product-img {
        width: 100%;
        height: 150px;
        object-fit: contain;
        margin-bottom: 15px;
        border-radius: 10px;
    }
    
    /* النصوص */
    .product-title { font-size: 14px; font-weight: 600; color: #2d3436; height: 40px; overflow: hidden; margin-bottom: 5px; }
    .stars { color: #fdcb6e; font-size: 12px; margin-bottom: 5px; }
    .price-old { color: #b2bec3; text-decoration: line-through; font-size: 11px; }
    .price-new { color: #00b894; font-size: 20px; font-weight: 800; margin: 5px 0; }
    
    /* ستايل أزرار Streamlit */
    div.stButton > button:first-child {
        background: linear-gradient(to right, #00b4db, #0083b0);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 20px;
        font-weight: bold;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background: linear-gradient(to right, #0083b0, #00b4db);
        box-shadow: 0 5px 15px rgba(0,180,219,0.4);
    }
    </style>
    """, unsafe_allow_html=True)

def load_data():
    conn = sqlite3.connect('dz_finder.db')
    conn.row_factory = sqlite3.Row
    data = conn.execute('SELECT * FROM products ORDER BY added_at DESC').fetchall()
    conn.close()
    return data

# --- الهيدر ---
st.markdown("<h1 style='text-align: center; color: #2d3436;'>🛍️ DzTrend <span style='color: #00b894;'>Intelligence</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #636e72;'>أفضل الهمزات المختارة بعناية تحت 2000 دج</p>", unsafe_allow_html=True)

products = load_data()

if products:
    cols = st.columns(6)
    for i, row in enumerate(products):
        # حسابات
        mkt_p = row['market_price']
        prm_p = row['promo_price']
        discount = int(((mkt_p - prm_p) / mkt_p) * 100)
        final_price = int(prm_p * (1 + MY_PROFIT))
        profit = final_price - prm_p

        with cols[i % 6]:
            # عرض الكرت المودارن عبر HTML
            st.markdown(f'''
                <div class="modern-card">
                    <div class="discount-badge">-{discount}%</div>
                    <img src="{row['image_url']}" class="product-img" onerror="this.src='https://via.placeholder.com/150'">
                    <div class="product-title">{row['title']}</div>
                    <div class="stars">⭐ {row['rating']}</div>
                    <div class="price-old">{mkt_p} DA</div>
                    <div class="price-new">{final_price} DA</div>
                    <div style="font-size: 10px; color: #0984e3;">💰 فايدتك: +{profit} DA</div>
                </div>
            ''', unsafe_allow_html=True)
            
            # زر الواتساب (تحت الكرت)
            msg = f"سلام محمد، حاب نطلب: {row['title']}\nالسعر: {final_price} DA"
            wa_url = f"https://wa.me/213600000000?text={urllib.parse.quote(msg)}"
            st.link_button("🚀 اطلبها الآن", wa_url)