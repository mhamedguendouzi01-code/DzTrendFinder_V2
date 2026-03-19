import streamlit as st
import pandas as pd
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="مركز التوريد العالمي - الجزائر", page_icon="🌍", layout="wide")

# 2. تصميم CSS احترافي (عربي)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [data-testid="stSidebar"], .main { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .product-card {
        background: white; border-radius: 15px; padding: 20px;
        border: 1px solid #eee; text-align: center; height: 100%;
        transition: 0.3s ease; position: relative; display: flex; flex-direction: column;
    }
    .product-card:hover { transform: translateY(-10px); box-shadow: 0 12px 25px rgba(0,0,0,0.1); }
    .price-usd { color: #27ae60; font-weight: bold; font-size: 1.3rem; margin: 5px 0; }
    .price-dzd { color: #7f8c8d; font-size: 0.9rem; font-weight: 500; margin-bottom: 10px; }
    .title { font-size: 0.85rem; font-weight: 600; height: 50px; overflow: hidden; color: #333; margin-bottom: 10px; line-height: 1.4; }
    .badge { position: absolute; top: 15px; right: 15px; padding: 4px 10px; border-radius: 5px; color: white; font-size: 0.7rem; font-weight: bold; background: #ff6a00; z-index: 10; }
    img { max-height: 180px; object-fit: contain; margin-bottom: 15px; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

EXCHANGE_RATE = 240 

if 'inventory' not in st.session_state:
    st.session_state['inventory'] = None

# 3. لوحة التحكم
with st.sidebar:
    st.title("🛡️ لوحة التحكم")
    if st.text_input("كود الأمان", type="password") == "dz2026":
        uploaded_file = st.file_uploader("ارفع ملف الإكسل", type=['xlsx', 'csv'])
        if uploaded_file:
            try:
                df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
                df.columns = df.columns.astype(str).str.strip()

                # القاموس الشامل بناءً على تحليلي لملفاتك
                mapping = {
                    'product-title-text': 'Title', 'product': 'Title',
                    'tp-inline-block': 'Price', 'tp-inlin': 'Price',
                    'product-title-text src': 'Image', 'tp-h-full src': 'Image_Alt', 'tp-w-fu': 'Image_Alt2',
                    'tp-me-1 href': 'Link', 'tp-text-sm href': 'Link_Alt', 'tp-w-6': 'Link_Alt2'
                }
                df = df.rename(columns=mapping)
                st.session_state['inventory'] = df
                st.sidebar.success(f"✅ تم تحميل {len(df)} سلعة!")
            except Exception as e:
                st.sidebar.error(f"خطأ: {e}")

# 4. الواجهة الرئيسية
st.title("🌍 مركز التوريد العالمي - الجزائر")

if st.session_state['inventory'] is not None:
    df = st.session_state['inventory']
    cols = st.columns(4)
    
    for i, (idx, row) in enumerate(df.iterrows()):
        with cols[i % 4]:
            # جلب البيانات
            title = str(row.get('Title', 'بدون عنوان'))
            price_val = str(row.get('Price', '0'))
            
            # صياد الصور الذكي (يحاول في 3 أعمدة مختلفة)
            img = str(row.get('Image', row.get('Image_Alt', row.get('Image_Alt2', ''))))
            lnk = str(row.get('Link', row.get('Link_Alt', row.get('Link_Alt2', '#'))))

            # تنظيف السعر
            try:
                p_str = price_val.replace(',', '.').replace(' ', '').replace('$', '').strip()
                p_clean = float(re.findall(r'\d+\.?\d*', p_str)[0])
            except:
                p_clean = 0.0

            # تصحيح الصورة
            if img.startswith('//'): img = 'https:' + img
            if not img.startswith('http'): img = "https://via.placeholder.com/200?text=Check+Alibaba"

            st.markdown(f'''
                <div class="product-card">
                    <div class="badge">بيع بالجملة</div>
                    <img src="{img}">
                    <div class="title">{title}</div>
                    <div class="price-usd">{p_clean:,.2f} دولار</div>
                    <div class="price-dzd">≈ {int(p_clean * EXCHANGE_RATE):,} دج</div>
                </div>
            ''', unsafe_allow_html=True)
            st.link_button("عرض على علي بابا 🤝", lnk, use_container_width=True)
            st.write("")
else:
    st.info("👋 ارفع ملف الإكسل من القائمة الجانبية.")
