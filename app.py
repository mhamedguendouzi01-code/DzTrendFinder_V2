import streamlit as st
import sqlite3
import urllib.parse

# إعداد الصفحة
st.set_page_config(page_title="DzTrend | متجر الهمزات", layout="wide")

# --- CSS الاحترافي (AliExpress Style) ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .ali-card { border-radius: 12px; padding: 0px; margin-bottom: 20px; text-align: right; }
    .ali-img { width: 100%; aspect-ratio: 1/1; object-fit: cover; border-radius: 12px; background-color: #f5f5f5; cursor: pointer; }
    .ali-title { font-size: 13px; color: #191919; margin: 8px 0 4px 0; height: 36px; overflow: hidden; line-height: 1.4; }
    .ali-price-main { font-size: 18px; font-weight: 700; color: #191919; }
    .shock-badge { background: #ffeded; color: #ff4747; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: bold; }
    .fire-tag { color: #ff4747; font-size: 11px; font-weight: bold; margin-bottom: 2px; }
    div.stButton > button { border-radius: 20px; font-size: 12px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- دالات قاعدة البيانات ---
def load_products():
    conn = sqlite3.connect('dz_finder.db')
    conn.row_factory = sqlite3.Row
    data = conn.execute("SELECT * FROM products ORDER BY (market_price - promo_price) DESC").fetchall()
    conn.close()
    return data

def get_product(p_id):
    conn = sqlite3.connect('dz_finder.db')
    conn.row_factory = sqlite3.Row
    data = conn.execute("SELECT * FROM products WHERE id = ?", (p_id,)).fetchone()
    conn.close()
    return data

# --- إدارة الحالة (Session State) ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_id' not in st.session_state:
    st.session_state.selected_id = None

# --- الصفحة الرئيسية (المتجر) ---
if st.session_state.page == 'home':
    st.markdown("<h2 style='text-align: center;'>Pour vous | من أجلك 🔥</h2>", unsafe_allow_html=True)
    
    products = load_products()
    cols = st.columns(6)
    
    for i, row in enumerate(products):
        saving = row['market_price'] - row['promo_price']
        profit = int(saving * 0.40) # فايدتك مخفية
        final_price = int(row['promo_price'] + profit)
        discount_pct = int((saving / row['market_price']) * 100)
        
        with cols[i % 6]:
            st.markdown(f'''
                <div class="ali-card">
                    <img src="{row['image_url']}" class="ali-img">
                    <div class="ali-title">{row['title']}</div>
                    <div class="ali-price-main">{final_price} DA</div>
                    <div class="shock-badge">⚡ بري شوك! -{discount_pct}%</div>
                </div>
            ''', unsafe_allow_html=True)
            
            if st.button("تفاصيل المنتج 🔎", key=f"view_{row['id']}"):
                st.session_state.selected_id = row['id']
                st.session_state.page = 'detail'
                st.rerun()

# --- صفحة تفاصيل المنتج (Detail Page) ---
elif st.session_state.page == 'detail':
    p = get_product(st.session_state.selected_id)
    
    if st.button("⬅️ العودة للمتجر"):
        st.session_state.page = 'home'
        st.rerun()
        
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.image(p['image_url'], use_container_width=True)
        if p['video_url']:
            st.markdown("#### 🎥 فيديو المنتج")
            st.video(p['video_url'])
            
    with col_right:
        st.header(p['title'])
        st.write(f"⭐ التقييم: {p['rating']} | 📦 المبيعات: {p['reviews_count']}+")
        st.divider()
        
        saving = p['market_price'] - p['promo_price']
        final_price = int(p['promo_price'] + (saving * 0.40))
        
        st.markdown(f"## السعر: {final_price} DA")
        st.markdown(f"<p style='color:grey; text-decoration:line-through;'>السعر الأصلي: {int(p['market_price'])} DA</p>", unsafe_allow_html=True)
        
        st.write("---")
        st.markdown("### 🎨 اختر اللون / المقاس:")
        option = st.selectbox("المتوفر حالياً:", p['options'].split(','))
        
        st.write("---")
        msg = f"سلام محمد، حاب نطلب: {p['title']}\nالخيار: {option}\nالسعر: {final_price} DA"
        wa_url = f"https://wa.me/213600000000?text={urllib.parse.quote(msg)}"
        st.link_button("✅ تأكيد الطلب عبر واتساب", wa_url)

# --- لوحة التحكم (مخفي للمدير) ---
with st.sidebar:
    st.divider()
    if st.checkbox("🔑 دخول المدير"):
        st.title("📊 أرباحك الصافية")
        products = load_products()
        for r in products:
            sv = r['market_price'] - r['promo_price']
            prf = int(sv * 0.40)
            st.write(f"**{r['title'][:20]}...**")
            st.success(f"الربح: +{prf} DA")
            st.divider()