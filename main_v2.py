import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="Global Deals Hub", page_icon="🌍", layout="wide")

# 2. تصميم CSS عصري (تنظيم البطاقات وتصغير الصور)
st.markdown("""
    <style>
    .product-card {
        background-color: white;
        border-radius: 15px;
        padding: 10px;
        border: 1px solid #efefef;
        text-align: center;
        margin-bottom: 20px;
    }
    .stImage > img {
        border-radius: 10px;
        max-height: 180px;
        object-fit: contain;
    }
    .price {
        color: #1a73e8;
        font-weight: bold;
        font-size: 1.3rem;
    }
    .title {
        font-size: 0.9rem;
        font-weight: 600;
        height: 45px;
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar (لوحة التحكم)
with st.sidebar:
    st.title("🔐 Admin Panel")
    pwd = st.text_input("Password", type="password")
    if pwd == "dz2026":
        st.success("Access Granted!")
        uploaded_file = st.file_uploader("Upload Excel", type=['xlsx'])
        if uploaded_file:
            df = pd.read_excel(uploaded_file)
            # تنظيف أسماء الأعمدة من الفراغات (أهم خطوة)
            df.columns = df.columns.str.strip()
            st.session_state['data'] = df
            st.success(f"Loaded {len(df)} Products!")

# 4. الواجهة الرئيسية
st.title("🌍 Global Deals Hub")
st.write("Viral Gadgets from Amazon, AliExpress & Temu")

if 'data' in st.session_state:
    df = st.session_state['data']
    
    # محرك البحث
    search = st.text_input("🔍 Search products...", "")
    if search:
        df = df[df['Product Title'].str.contains(search, case=False, na=False)]

    st.divider()
    
    # عرض السلع في 4 أعمدة
    cols = st.columns(4)
    for index, row in df.iterrows():
        with cols[index % 4]:
            with st.container():
                # جلب البيانات مع تنظيف الروابط
                img_url = str(row.get('Image URL', '')).strip()
                aff_link = str(row.get('Affiliate Link', '#')).strip()
                
                # عرض الصورة
                if img_url and img_url != 'nan' and img_url.startswith('http'):
                    st.image(img_url, use_container_width=True)
                else:
                    st.image("https://via.placeholder.com/150?text=Check+Image+Link", use_container_width=True)
                
                # العنوان والسعر
                st.markdown(f"<div class='title'>{row.get('Product Title', 'No Title')[:45]}...</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='price'>${row.get('Price', '0.00')}</div>", unsafe_allow_html=True)
                st.caption(f"📍 {row.get('Platform', 'Shop')}")
                
                # البوطونة
                st.link_button("🔥 View Deal", aff_link, use_container_width=True)
                st.write("") 
else:
    st.info("👋 Welcome! Please upload your Excel file from the Admin Panel.")
