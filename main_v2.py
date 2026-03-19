import streamlit as st
import pandas as pd
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="مركز التوريد العالمي - الجزائر", page_icon="🌍", layout="wide")

# 2. تصميم CSS احترافي للجزائر (Cairo Font + RTL)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [data-testid="stSidebar"], .main { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .product-card {
        background: white; border-radius: 15px; padding: 20px;
        border: 1px solid #eee; text-align: center; height: 100%;
        transition: 0.3s ease; display: flex; flex-direction: column;
        justify-content: space-between;
    }
    .product-card:hover { transform: translateY(-10px); box-shadow: 0 12px 25px rgba(0,0,0,0.1); }
    .price-usd { color: #27ae60; font-weight: bold; font-size: 1.3rem; margin: 5px 0; }
    .price-dzd { color: #7f8c8d; font-size: 0.9rem; font-weight: 500; margin-bottom: 10px; }
    .title { font-size: 0.85rem; font-weight: 600; min-height: 45px; overflow: hidden; color: #333; margin-bottom: 10px; line-height: 1.4; }
    .badge { position: absolute; top: 15px; right: 15px; padding: 4px 10px; border-radius: 5px; color: white; font-size: 0.7rem; font-weight: bold; background: #ff6a00; z-index: 10; }
    .product-img { max-height: 180px; width: 100%; object-fit: contain; margin-bottom: 15px; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

EXCHANGE_RATE = 240 

if 'inventory' not in st.session_state:
    st.session_state['inventory'] = None

# 3. لوحة التحكم (Admin Sidebar)
with st.sidebar:
    st.title("🛡️ لوحة التحكم")
    if st.text_input("كود الأمان", type="password") == "dz2026":
        uploaded_file = st.file_uploader("ارفع ملف الإكسل (Alibaba Scraper)", type=['xlsx', 'csv'])
        if uploaded_file:
            try:
                df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
                df.columns = df.columns.astype(str).str.strip()

                # القاموس الشامل لربط الأعمدة المشفرة بالأسماء الحقيقية
                mapping = {
                    'product-title-text': 'Title', 'product': 'Title',
                    'tp-inline-block': 'Price', 'tp-inlin': 'Price',
                    'product-title-text src': 'Img1', 'tp-h-full src': 'Img2', 
                    'tp-w-fu': 'Img3', 'tp-w-[18px] src': 'Img4',
                    'tp-me-1 href': 'Link', 'tp-text-sm href': 'Link_Alt', 'tp-w-6': 'Link_Alt2'
                }
                df = df.rename(columns=mapping)
                st.session_state['inventory'] = df
                st.sidebar.success(f"✅ تم تحميل {len(df)} سلعة بنجاح!")
            except Exception as e:
                st.sidebar.error(f"خطأ في الملف: {e}")

# 4. الواجهة الرئيسية
st.title("🌍 مركز التوريد العالمي - الجزائر")

if st.session_state['inventory'] is not None:
    df = st.session_state['inventory']
    cols = st.columns(4)
    
    for i, (idx, row) in enumerate(df.iterrows()):
        with cols[i % 4]:
            # 1. العنوان
            title = str(row.get('Title', 'بدون عنوان'))
            
            # 2. السعر ومعالجته
            price_val = str(row.get('Price', '0'))
            try:
                p_str = price_val.replace(',', '.').replace(' ', '').replace('$', '').strip()
                p_clean = float(re.findall(r'\d+\.?\d*', p_str)[0])
            except:
                p_clean = 0.0

            # 3. "صياد الصور" المتعدد
            img = str(row.get('Img1', row.get('Img2', row.get('Img3', row.get('Img4', '')))))
            if img.startswith('//'): img = 'https:' + img
            if not img.startswith('http'): img = "https://via.placeholder.com/200?text=Check+Link"

            # 4. الرابط
            lnk = str(row.get('Link', row.get('Link_Alt', '#')))

            # عرض الكارد
            st.markdown(f'''
                <div class="product-card">
                    <div class="badge">بيع بالجملة</div>
                    <img src="{img}" class="product-img">
                    <div class="title">{title[:60]}...</div>
                    <div class="price-usd">{p_clean:,.2f} دولار</div>
                    <div class="price-dzd">≈ {int(p_clean * EXCHANGE_RATE):,} دج</div>
                </div>
            ''', unsafe_allow_html=True)
            st.link_button("عرض السلعة 🤝", lnk, use_container_width=True)
            st.write("")
else:
    st.info("👋 يا محمد، السيت جاهز! ارفع ملف الإكسل الأخير من القائمة الجانبية.")
