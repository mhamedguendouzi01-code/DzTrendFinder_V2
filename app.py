import streamlit as st
import sqlite3
import urllib.parse

# 1. إعداد الصفحة بستايل عصري
st.set_page_config(
    page_title="DzTrend | Modern Shopping", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. الديزاين المودارن (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Poppins:wght@400;600;800&display=swap');

    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        font-family: 'Cairo', sans-serif;
    }

    [data-testid="stSidebar"] { display: none; }

    /* هيدر الموقع */
    .header-text {
        text-align: center;
        padding: 30px 0;
        background: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
    }

    /* كرت المنتج المودارن */
    .ali-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 28px !important;
        border: 1px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 10px 25px rgba(0,0,0,0.04);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        margin-bottom: 20px;
    }
    .ali-card:hover {
        transform: translateY(-12px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.08);
        border-color: #ff4747;
    }

    .ali-img {
        width: 100%; aspect-ratio: 1/1; object-fit: cover;
        border-radius: 28px 28px 0 0;
        transition: 0.5s;
    }
    
    .info-box { padding: 18px; text-align: right; direction: rtl; }
    .ali-price { 
        font-family: 'Poppins', sans-serif;
        font-size: 24px; font-weight: 800; color: #1a1a1a; margin: 8px 0;
    }
    
    .shock-badge { 
        background: linear-gradient(90deg, #ff4747, #ff7e7e);
        color: white; padding: 4px 12px; border-radius: 12px;
        font-size: 11px; font-weight: bold; display: inline-block;
    }

    /* بوطونة التفاصيل السفلية */
    div.stButton > button {
        width: 100%; border-radius: 15px; border: 1px solid #eee;
        background: white; color: #555; font-weight: 600; height: 42px;
    }
    div.stButton > button:hover {
        background: #1a1a1a; color: white; border-color: #1a1a1a;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. وظائف قاعدة البيانات
def get_products():
    conn = sqlite3.connect('dz_finder.db')
    conn.row_factory = sqlite3.Row
    data = conn.execute("SELECT * FROM products ORDER BY added_at DESC").fetchall()
    conn.close()
    return data

# 4. إدارة الصفحات
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'selected_id' not in st.session_state: st.session_state.selected_id = None

# --- الصفحة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown('<div class="header-text"><h1>🔥 DzTrend Finder</h1><p>أفضل الهمزات الأوتوماتيكية</p></div>', unsafe_allow_html=True)
    
    products = get_products()
    
    if not products:
        st.info("المتجر فارغ حالياً، ادخل للوحة التحكم في الأسفل لصيد سلع جديدة!")
    
    cols = st.columns(5, gap="medium")
    for i, row in enumerate(products):
        discount = int(((row['market_price'] - row['promo_price']) / row['market_price']) * 100)
        
        with cols[i % 5]:
            st.markdown(f'''
                <div class="ali-card">
                    <img src="{row['image_url']}" class="ali-img">
                    <div class="info-box">
                        <div class="shock-badge">تخفيض {discount}%</div>
                        <div class="ali-price">{int(row['promo_price'])} DA</div>
                        <div style="font-size:13px; color:#666; height:40px; overflow:hidden;">{row['title']}</div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            
            if st.button("عرض المنتج 🔍", key=f"v_{row['id']}"):
                st.session_state.selected_id = row['id']
                st.session_state.page = 'detail'
                st.rerun()

# --- صفحة التفاصيل ---
elif st.session_state.page == 'detail':
    conn = sqlite3.connect('dz_finder.db')
    conn.row_factory = sqlite3.Row
    p = conn.execute("SELECT * FROM products WHERE id = ?", (st.session_state.selected_id,)).fetchone()
    conn.close()

    if st.button("⬅️ عودة للمتجر"):
        st.session_state.page = 'home'
        st.rerun()

    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        st.image(p['image_url'], use_container_width=True)
    
    with c2:
        st.markdown(f"""
            <div style="text-align:right; direction:rtl;">
                <h1>{p['title']}</h1>
                <h2 style="color:#ff4747;">السعر الحصري: {int(p['promo_price'])} DA</h2>
                <p style="color:#999; text-decoration:line-through;">السعر القديم: {int(p['market_price'])} DA</p>
                <hr>
                <p>⭐ تقييم المنتج: {p['rating']}/5</p>
                <p>📦 خيارات المنتج: {p['options']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        wa_msg = f"سلام، حاب نطلب المنتج: {p['title']}"
        wa_url = f"https://wa.me/213600000000?text={urllib.parse.quote(wa_msg)}"
        st.link_button("🔥 اطلب عبر واتساب الآن", wa_url)

# --- لوحة التحكم (Admin Panel) ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
with st.expander("🔐 لوحة تحكم المدير (محمد)"):
    pw = st.text_input("كلمة السر", type="password")
    if pw == "dz2026":
        st.success("مرحباً بك يا باطرون!")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 صيد سلع جديدة أوتوماتيكياً"):
                try:
                    import scraper