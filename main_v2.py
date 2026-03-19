import streamlit as st
import pandas as pd
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="Global Sourcing Hub DZ", page_icon="📦", layout="wide")

# 2. تصميم CSS
st.markdown("""
    <style>
    .product-card {
        background: white; border-radius: 15px; padding: 20px;
        border: 1px solid #eee; text-align: center; height: 100%;
        transition: 0.3s ease; position: relative;
    }
    .product-card:hover { transform: translateY(-10px); box-shadow: 0 12px 25px rgba(0,0,0,0.1); }
    .price-usd { color: #27ae60; font-weight: bold; font-size: 1.4rem; margin: 5px 0; }
    .price-dzd { color: #7f8c8d; font-size: 0.95rem; font-weight: 500; margin-bottom: 10px; }
    .title { font-size: 0.85rem; font-weight: 600; height: 45px; overflow: hidden; color: #333; line-height: 1.2; }
    .badge { position: absolute; top: 15px; left: 15px; padding: 4px 10px; border-radius: 5px; color: white; font-size: 0.7rem; font-weight: bold; background: #ff6a00; }
    </style>
    """, unsafe_allow_html=True)

EXCHANGE_RATE = 240 

if 'inventory' not in st.session_state:
    st.session_state['inventory'] = None

# 3. لوحة التحكم
with st.sidebar:
    st.title("🛡️ Admin Panel")
    if st.text_input("Security Key", type="password") == "dz2026":
        uploaded_file = st.file_uploader("Upload Scraped File", type=['xlsx', 'csv'])
        if uploaded_file:
            try:
                df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
                df.columns = df.columns.astype(str).str.strip()

                # --- المابينج الجديد بناءً على صورة الإكسل تاعك ---
                mapping = {
                    'tp-w-fu': 'Image',      # العمود الأول اللي فيه رابط الصورة
                    'product': 'Title',      # العمود اللي فيه اسم السلعة (Casque, Module...)
                    'tp-inlin': 'Price',     # العمود اللي فيه السعر (248,00 , 886,95...)
                    'tp-text-': 'MOQ'        # العمود اللي فيه الكمية
                }
                
                # إذا كانت الأسماء تختلف قليلاً، نحاول حلاً احتياطياً
                df = df.rename(columns=mapping)
                
                # تصحيح الروابط: إذا كان رابط المنتج موجود في عمود آخر
                if 'tp-w-6' in df.columns:
                    df = df.rename(columns={'tp-w-6': 'Link'})
                
                st.session_state['inventory'] = df
                st.sidebar.success("✅ تم قراءة ملف علي بابا بنجاح!")
            except Exception as e:
                st.sidebar.error(f"Error: {e}")

# 4. الواجهة الرئيسية
st.title("🌍 Global Sourcing Hub - Algeria")

if st.session_state['inventory'] is not None:
    df = st.session_state['inventory']
    cols = st.columns(4)
    
    for i, (idx, row) in enumerate(df.iterrows()):
        with cols[i % 4]:
            # جلب البيانات من الأعمدة "الغريبة"
            title = str(row.get('Title', 'No Title'))
            price_val = str(row.get('Price', '0'))
            img = str(row.get('Image', ''))
            lnk = str(row.get('Link', '#'))

            # تنظيف السعر (تحويل 248,00 إلى رقم)
            try:
                p_str = price_val.replace(',', '.').replace('$', '').strip()
                p_clean = float(re.findall(r'\d+\.?\d*', p_str)[0])
            except:
                p_clean = 0.0

            # تصحيح الصورة
            if not img.startswith('http'): img = "https://via.placeholder.com/200?text=Check+Link"

            st.markdown(f'''
                <div class="product-card">
                    <div class="badge">WHOLESALE</div>
                    <img src="{img}" style="width:100%; border-radius:12px; margin-top:20px; height:180px; object-fit:contain;">
                    <div class="title">{title}</div>
                    <div class="price-usd">${p_clean:.2f}</div>
                    <div class="price-dzd">≈ {int(p_clean * EXCHANGE_RATE):,} DA</div>
                </div>
            ''', unsafe_allow_html=True)
            st.link_button("🤝 View on Alibaba", lnk, use_container_width=True)
            st.write("")
else:
    st.info("ارفع ملف الإكسل من القائمة الجانبية (Admin) باش تبدأ.")
