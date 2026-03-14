import streamlit as st
import sqlite3
import urllib.parse

# إعداد الصفحة
st.set_page_config(page_title="DzTrend | المتجر الذكي", layout="wide")

# --- CSS الأزرار المودارن ---
st.markdown("""
    <style>
    /* أزرار التصنيفات الدائرية */
    .quick-btn-container {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-bottom: 25px;
        flex-wrap: wrap;
    }
    .quick-btn {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 25px;
        padding: 10px 20px;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        transition: 0.3s;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .quick-btn:hover {
        background: #191919;
        color: white;
        transform: scale(1.05);
    }
    
    /* ستايل كرت AliExpress */
    .ali-card {
        background: white; border-radius: 12px; padding: 0; margin-bottom: 20px;
    }
    .ali-img { width: 100%; aspect-ratio: 1/1; object-fit: cover; border-radius: 12px; }
    .ali-price { font-size: 18px; font-weight: bold; color: #191919; }
    .shock-tag { background: #ffeded; color: #ff4747; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: bold; }
    
    /* زر الواتساب العائم */
    .floating-wa {
        position: fixed; bottom: 20px; right: 20px;
        background: #25d366; color: white; padding: 15px;
        border-radius: 50%; box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        z-index: 1000; font-size: 20px; text-decoration: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- واجهة المستخدم ---

# 1. شريط البحث والأزرار العلوية
st.markdown("""
    <div class="quick-btn-container">
        <button class="quick-btn">🔥 الأكثر مبيعاً</button>
        <button class="quick-btn">🚗 سيارات</button>
        <button class="quick-btn">🎧 إلكترونيات</button>
        <button class="quick-btn">🏠 منزل</button>
        <button class="quick-btn">⚽ رياضة</button>
    </div>
    """, unsafe_allow_html=True)

# 2. جلب البيانات (مع خوارزمية الفايدة)
def get_products():
    conn = sqlite3.connect('dz_finder.db')
    conn.row_factory = sqlite3.Row
    data = conn.execute("SELECT * FROM products ORDER BY (market_price - promo_price) DESC").fetchall()
    conn.close()
    return data

products = get_products()
cols = st.columns(6)

for i, row in enumerate(products):
    # حساب الفايدة المخفية (40% من التوفير)
    saving = row['market_price'] - row['promo_price']
    final_price = int(row['promo_price'] + (saving * 0.40))
    discount = int((saving / row['market_price']) * 100)

    with cols[i % 6]:
        # تصميم AliExpress النقي
        st.markdown(f'''
            <div class="ali-card">
                <img src="{row['image_url']}" class="ali-img">
                <div style="font-size:12px; margin-top:8px; height:35px; overflow:hidden;">{row['title']}</div>
                <div class="ali-price">{final_price} DA</div>
                <div style="color:#999; text-decoration:line-through; font-size:11px;">{int(row['market_price'])} DA</div>
                <div class="shock-tag">⚡ بري شوك! -{discount}%</div>
            </div>
        ''', unsafe_allow_html=True)
        
        # بوطونة الطلب تحت الكرت
        msg = f"سلام محمد، حاب نطلب: {row['title']} بسعر {final_price} DA"
        wa_url = f"https://wa.me/213600000000?text={urllib.parse.quote(msg)}"
        st.link_button("🚀 اطلب الآن", wa_url)

# 3. زر الواتساب العائم (Floating Action Button)
st.markdown(f'''
    <a href="https://wa.me/213600000000" class="floating-wa" target="_blank">
        💬
    </a>
    ''', unsafe_allow_html=True)