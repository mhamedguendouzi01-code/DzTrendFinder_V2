import streamlit as st
import sqlite3
import urllib.parse

# إعداد الصفحة
st.set_page_config(page_title="DzTrend | AliExpress Style", layout="wide")

# --- CSS للواجهة الاحترافية ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f4f4; }
    
    /* أزرار التصنيفات العلوية */
    .cat-bar {
        display: flex;
        justify-content: center;
        gap: 10px;
        padding: 15px 0;
        overflow-x: auto;
        background: white;
        margin-bottom: 20px;
        border-bottom: 1px solid #ddd;
    }
    .cat-item {
        background: #fdfdfd;
        border: 1px solid #eee;
        padding: 8px 18px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        cursor: pointer;
        white-space: nowrap;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .cat-item:hover { background: #000; color: #fff; border-color: #000; }

    /* كرت المنتج - ستايل AliExpress */
    .ali-card {
        background: white;
        border-radius: 12px;
        padding: 0px;
        margin-bottom: 20px;
        transition: 0.3s;
        border: 1px solid transparent;
    }
    .ali-card:hover { border-color: #ff4747; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
    
    .ali-img {
        width: 100%;
        aspect-ratio: 1/1;
        object-fit: cover;
        border-radius: 12px 12px 0 0;
    }
    .info-box { padding: 10px; text-align: right; }
    .ali-title { font-size: 12px; height: 34px; overflow: hidden; color: #333; margin-bottom: 5px; }
    .ali-price { font-size: 17px; font-weight: bold; color: #191919; }
    .shock-badge { 
        background: #ffeded; color: #ff4747; padding: 2px 6px; 
        border-radius: 4px; font-size: 10px; font-weight: bold; 
        display: inline-block; margin-top: 5px;
    }
    
    /* بوطونة "عرض التفاصيل" السريعة */
    div.stButton > button {
        background: #fff; border: 1px solid #333; color: #333;
        border-radius: 20px; font-size: 11px; height: 32px; font-weight: 600;
    }
    div.stButton > button:hover { background: #000; color: #fff; }
    </style>
    """, unsafe_allow_html=True)

# --- واجهة المستخدم العلوية (الأزرار) ---
st.markdown("""
    <div class="cat-bar">
        <div class="cat-item">✨ Pour vous</div>
        <div class="cat-item">🔥 Meilleures ventes</div>
        <div class="cat-item">🚗 Auto</div>
        <div class="cat-item">🎧 Électronique</div>
        <div class="cat-item">🏠 Maison</div>
        <div class="cat-item">🧸 Jouets</div>
    </div>
    """, unsafe_allow_html=True)

# --- إدارة الصفحات ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'selected_id' not in st.session_state: st.session_state.selected_id = None

# --- جلب البيانات ---
def load_data():
    conn = sqlite3.connect('dz_finder.db')
    conn.row_factory = sqlite3.Row
    data = conn.execute("SELECT * FROM products ORDER BY added_at DESC").fetchall()
    conn.close()
    return data

# --- الصفحة الرئيسية ---
if st.session_state.page == 'home':
    products = load_data()
    cols = st.columns(6) # 6 أعمدة كما في الصورة
    
    for i, row in enumerate(products):
        saving = row['market_price'] - row['promo_price']
        profit = int(saving * 0.40)
        final_price = int(row['promo_price'] + profit)
        discount = int((saving / row['market_price']) * 100)

        with cols[i % 6]:
            st.markdown(f'''
                <div class="ali-card">
                    <img src="{row['image_url']}" class="ali-img">
                    <div class="info-box">
                        <div class="ali-title">{row['title']}</div>
                        <div class="ali-price">{final_price} DA</div>
                        <div style="color:#999; text-decoration:line-through; font-size:11px;">{int(row['market_price'])} DA</div>
                        <div class="shock-badge">⚡ بري شوك! -{discount}%</div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            
            # بوطونة عرض التفاصيل (تحت كل منتج)
            if st.button("عرض المنتج 🔎", key=f"v_{row['id']}"):
                st.session_state.selected_id = row['id']
                st.session_state.page = 'detail'
                st.rerun()

# --- صفحة تفاصيل المنتج (Detail Page) ---
elif st.session_state.page == 'detail':
    conn = sqlite3.connect('dz_finder.db')
    conn.row_factory = sqlite3.Row
    p = conn.execute("SELECT * FROM products WHERE id = ?", (st.session_state.selected_id,)).fetchone()
    conn.close()

    if st.button("⬅️ العودة للرئيسية"):
        st.session_state.page = 'home'
        st.rerun()

    c1, c2 = st.columns([1, 1])
    with c1:
        st.image(p['image_url'], use_container_width=True)
        if p['video_url']: st.video(p['video_url'])
    with c2:
        st.header(p['title'])
        saving = p['market_price'] - p['promo_price']
        final_p = int(p['promo_price'] + (saving * 0.40))
        st.subheader(f"السعر: {final_p} DA")
        st.markdown(f"**الخيارات:** {p['options']}")
        
        msg = f"سلام محمد، حاب نطلب: {p['title']} بسعر {final_p} DA"
        wa_url = f"https://wa.me/213600000000?text={urllib.parse.quote(msg)}"
        st.link_button("✅ اطلب الآن عبر واتساب", wa_url)