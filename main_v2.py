import streamlit as st
import pandas as pd
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="Global Sourcing Hub DZ", page_icon="🌍", layout="wide")

# 2. تصميم CSS احترافي (منظم للجزائريين)
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

# سعر السكوار
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
                # قراءة الملف وتنظيف أسماء الأعمدة من الفراغات
                df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
                df.columns = df.columns.astype(str).str.strip()

                # --- القاموس الذكي بناءً على "صورتك" المبعوثة ---
                # لاحظت في صورتك أن:
                # 'product' هو العنوان
                # 'tp-inlin' هو السعر
                # 'tp-w-fu' هو الصورة
                # 'tp-w-6' هو الرابط
                mapping = {
                    'product': 'Title',
                    'tp-inlin': 'Price',
                    'tp-w-fu': 'Image',
                    'tp-w-6': 'Link',
                    'tp-text-': 'MOQ'
                }
                
                df = df.rename(columns=mapping)
                st.session_state['inventory'] = df
                st.sidebar.success(f"✅ تم تحميل {len(df)} سلعة بنجاح!")
            except Exception as e:
                st.sidebar.error(f"Error: {e}")

# 4. الواجهة الرئيسية
st.title("🌍 Global Sourcing Hub - Algeria")

if st.session_state['inventory'] is not None:
    df = st.session_state['inventory']
    cols = st.columns(4)
    
    for i, (idx, row) in enumerate(df.iterrows()):
        with cols[i % 4]:
            # جلب البيانات (مع معالجة القيم الفارغة)
            title = str(row.get('Title', 'No Title'))
            price_val = str(row.get('Price', '0'))
            img = str(row.get('Image', ''))
            lnk = str(row.get('Link', '#'))

            # تنظيف السعر (علي بابا يكتبه بالفواصل مثل 248,00)
            try:
                # نحول الفاصلة لنقطة وننزع أي رموز
                p_str = price_val.replace(',', '.').replace(' ', '').replace('$', '').strip()
                p_clean = float(re.findall(r'\d+\.?\d*', p_str)[0])
            except:
                p_clean = 0.0

            # تصحيح روابط صور علي بابا
            if img.startswith('//'): img = 'https:' + img
            if not img.startswith('http'): img = "https://via.placeholder.com/200?text=Check+Alibaba"

            st.markdown(f'''
                <div class="product-card">
                    <div class="badge">WHOLESALE</div>
                    <img src="{img}" style="width:100%; border-radius:12px; margin-top:20px; height:180px; object-fit:contain;">
                    <div class="title">{title}</div>
                    <div class="price-usd">${p_clean:,.2f}</div>
                    <div class="price-dzd">≈ {int(p_clean * EXCHANGE_RATE):,} DA</div>
                </div>
            ''', unsafe_allow_html=True)
            st.link_button("🤝 View on Alibaba", lnk, use_container_width=True)
            st.write("")
else:
    st.info("👋 يا محمد، ارفع ملف الإكسل اللي هبطته من علي بابا في القائمة الجانبية.")
