import streamlit as st
import sqlite3
import urllib.parse

# 1. إعداد الصفحة بستايل عصري
st.set_page_config(
    page_title="DzTrend | Modern Shopping", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. الديزاين المودارن (CSS) - "اللمسة الاحترافية"
st.markdown("""
    <style>
    /* استيراد خطوط جوجل المودارن */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Poppins:wght@400;600;800&display=swap');

    /* خلفية متدرجة فخمة */
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

    /* أزرار التصنيفات (Pills Style) */
    .stRadio div[role="radiogroup"] {
        display: flex; justify-content: center; gap: 12px;
        background: transparent; padding: 10px; margin-bottom: 30px;
    }
    .stRadio div[role="radiogroup"] label {
        background: white !important;
        border: 1px solid #eee !important;
        padding: 10px 22px !important;
        border-radius: 50px !important; /* شكل الحبة */
        font-weight: 600 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        transition: 0.3s;
    }

    /* كرت المنتج المودارن (Glassmorphism) */
    .ali-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 28px !important; /* حواف مدورة بزاف */
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

    /* الصورة مع أنيميشن */
    .ali-img {
        width: 100%; aspect-ratio: 1/1; object-fit: cover;
        border-radius: 28px 28px 0 0;
        transition: 0.5s;
    }
    .ali-card:hover .ali-img { transform: scale(1.08); }

    /* معلومات المنتج */
    .info-box { padding: 18px; text-align: right; direction: rtl; }
    .ali-title { 
        font-size: 14px; font-weight: 600; color: #333; 
        height: 40px; overflow: hidden; line-height: 1.4;
    }
    .ali-price { 
        font-family: 'Poppins', sans-serif;
        font-size: 24px; font-weight: 800; color: #1a1a1a; margin: 8px 0;
    }
    
    /* شارة التخفيض (Modern Badge) */
    .shock-badge { 
        background: linear-gradient(90deg, #ff4747, #ff7e7e);
        color: white; padding: 4px 12px; border-radius: 12px;
        font-size: 11px; font-weight: bold; display: inline-block;
    }

    /* إخفاء بوطونة الصورة الشفافة */
    div.stButton > button[key^="img_"] {
        height: 320px; width: 100%; background: transparent;
        border: none; color: transparent; position: absolute;
        top: 0; z-index: 10; cursor: pointer;
    }

    /* بوطونة التفاصيل السفلية */
    div.stButton > button[key^="v_"] {
        width: 100%; border-radius: 15px; border: 1px solid #eee;
        background: white; color: #555; font-weight: 600; height: 42px;
    }
    div.stButton > button[key^="v_"]:hover {
        background: #1a1a1a; color: white; border-color: #1a1a1a;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. جلب البيانات
def get_products(cat="الكل ✨"):
    conn = sqlite3.connect('dz_finder.db')
    conn.row_factory = sqlite3.Row
    if cat == "الكل ✨":
        data = conn.execute("SELECT * FROM products ORDER BY added_at DESC").fetchall()
    else:
        data = conn.execute("SELECT * FROM products WHERE title LIKE ? OR options LIKE ?", (f'%{cat}%', f'%{cat}%')).fetchall()
    conn.close()
    return data

# 4. التحكم في الصفحات
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'selected_id' not in st.session_state: st.session_state.selected_id = None

# --- الصفحة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown('<div class="header-text"><h1>🔥 DzTrend Finder</h1><p>أفضل الهمزات المختارة بعناية</p></div>', unsafe_allow_html=True)
    
    cats = ["الكل ✨", "Electronics", "Watch", "Home", "Auto"]
    selected_cat = st.radio("", cats, horizontal=True)
    
    products = get_products(selected_cat)
    
    cols = st.columns(6, gap="medium")
    for i, row in enumerate(products):
        saving = row['market_price'] - row['promo_price']
        final_price = int(row['promo_price'] + (saving * 0.40))
        discount = int((saving / row['market_price']) * 100)
        
        with cols[i % 6]:
            # كليكي على الصورة (شفاف)
            if st.button(" ", key=f"img_{row['id']}"):
                st.session_state.selected_id = row['id']
                st.session_state.page = 'detail'
                st.rerun()
            
            # الكرت المودارن
            st.markdown(f'''
                <div class="ali-card">
                    <img src="{row['image_url']}" class="ali-img">
                    <div class="info-box">
                        <div class="shock-badge">تخفيض {discount}%</div>
                        <div class="ali-price">{final_price} DA</div>
                        <div class="ali-title">{row['title']}</div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            
            if st.button("التفاصيل", key=f"v_{row['id']}"):
                st.session_state.selected_id = row['id']
                st.session_state.page = 'detail'
                st.rerun()

# --- صفحة التفاصيل المودارن ---
elif st.session_state.page == 'detail':
    conn = sqlite3.connect('dz_finder.db')
    conn.row_factory = sqlite3.Row
    p = conn.execute("SELECT * FROM products WHERE id = ?", (st.session_state.selected_id,)).fetchone()
    conn.close()

    st.markdown(f"""
        <div style="background:white; padding:15px; border-radius:20px; margin-bottom:20px; display:flex; align-items:center; gap:10px;">
             <h3 style="margin:0;">{p['title']}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("⬅️ عودة للمتجر"):
        st.session_state.page = 'home'
        st.rerun()

    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        st.markdown(f'<img src="{p["image_url"]}" style="width:100%; border-radius:30px; box-shadow:0 20px 40px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
        if p['video_url']: st.video(p['video_url'])
    
    with c2:
        final_p = int(p['promo_price'] + ((p['market_price'] - p['promo_price']) * 0.40))
        st.markdown(f"""
            <div style="text-align:right; padding:30px; background:white; border-radius:30px; border:1px solid #eee;">
                <h1 style="color:#ff4747; font-family:'Poppins';">{final_p} DA</h1>
                <p style="color:#999; text-decoration:line-through;">{int(p['market_price'])} DA</p>
                <hr style="opacity:0.1;">
                <p style="font-size:18px;"><b>الخيارات المتوفرة:</b><br>{p['options']}</p>
                <p>⭐ تقييم المنتج: {p['rating']}/5</p>
            </div>
        """, unsafe_allow_html=True)
        
        msg = f"سلام، مهتم بمنتج {p['title']} بسعر {final_p} DA"
        wa_url = f"https://wa.me/213600000000?text={urllib.parse.quote(msg)}"
        st.link_button("🔥 اطلب الآن عبر واتساب", wa_url, use_container_width=True)