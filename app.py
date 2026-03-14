import streamlit as st
import sqlite3
import urllib.parse

# 1. إعداد الصفحة (ستايل AliExpress)
st.set_page_config(page_title="DzTrend | الهمزات في دزاير", layout="wide", initial_sidebar_state="collapsed")

# 2. اللمسة الفنية (CSS) - هنا السحر تاع الكليكي على الصورة
st.markdown("""
    <style>
    .stApp { background-color: #f6f6f6; }
    [data-testid="stSidebar"] { display: none; }
    
    /* تنسيق أزرار التصنيفات */
    .stRadio div[role="radiogroup"] {
        display: flex; justify-content: center; gap: 15px;
        background: white; padding: 20px; border-bottom: 1px solid #eee;
    }
    
    /* كرت المنتج */
    .ali-card {
        background: white; border-radius: 15px; overflow: hidden;
        transition: 0.3s; border: 1px solid #eee; position: relative;
    }
    .ali-card:hover { border-color: #ff4747; transform: translateY(-5px); }
    
    .ali-img { width: 100%; aspect-ratio: 1/1; object-fit: cover; }
    
    .info-box { padding: 12px; text-align: right; direction: rtl; }
    .ali-title { font-size: 13px; height: 38px; overflow: hidden; color: #333; margin-bottom: 8px; }
    .ali-price { font-size: 19px; font-weight: bold; color: #191919; }
    .shock-badge { 
        background: #ffeded; color: #ff4747; padding: 3px 8px; 
        border-radius: 6px; font-size: 11px; font-weight: bold; 
    }

    /* جعل البوطونة تغطي الكرت كامل (الخدعة) */
    div.stButton > button[key^="img_"] {
        height: 280px; width: 100%; background: transparent;
        border: none; color: transparent; position: absolute;
        z-index: 100; cursor: pointer;
    }
    div.stButton > button[key^="img_"]:hover { background: rgba(0,0,0,0.03); }
    
    /* بوطونة التفاصيل السفلية */
    div.stButton > button[key^="v_"] {
        width: 100%; border-radius: 20px; font-size: 12px; height: 35px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. جلب البيانات من القاعدة
def get_products(cat="الكل ✨"):
    conn = sqlite3.connect('dz_finder.db')
    conn.row_factory = sqlite3.Row
    if cat == "الكل ✨":
        data = conn.execute("SELECT * FROM products ORDER BY added_at DESC").fetchall()
    else:
        data = conn.execute("SELECT * FROM products WHERE title LIKE ? OR options LIKE ?", (f'%{cat}%', f'%{cat}%')).fetchall()
    conn.close()
    return data

# 4. التحكم في التنقل
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'selected_id' not in st.session_state: st.session_state.selected_id = None

# --- الصفحة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown("<h1 style='text-align:center; color:#ff4747;'>DzTrend Finder 🇩🇿</h1>", unsafe_allow_html=True)
    
    cats = ["الكل ✨", "Electronics", "Watch", "Home", "Auto"]
    selected_cat = st.radio("", cats, horizontal=True)