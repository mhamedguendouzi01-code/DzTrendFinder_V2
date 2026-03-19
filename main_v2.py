import streamlit as st
import pandas as pd
import re

# 1. إعدادات الصفحة واللغة
st.set_page_config(page_title="مركز التوريد العالمي - الجزائر", page_icon="🌍", layout="wide")

# 2. تصميم CSS احترافي يدعم العربية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [data-testid="stSidebar"], .main { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .product-card {
        background: white; border-radius: 15px; padding: 20px;
        border: 1px solid #eee; text-align: center; height: 100%;
        transition: 0.3s ease; display: flex; flex-direction: column;
        justify-content: space-between; position: relative;
    }
    .product-card:hover { transform: translateY(-8px); box-shadow: 0 10px 20px rgba(0,0,0,0.08); }
    .price-usd { color: #27ae60; font-weight: bold; font-size: 1.3rem; margin: 5px 0; }
    .price-dzd { color: #7f8c8d; font-size: 0.9rem; font-weight: 500; margin-bottom: 10px; }
    .title { font-size: 0.85rem; font-weight: 600; min-height: 45px; overflow: hidden; color: #333; margin-bottom: 10px; line-height: 1.4; }
    .badge { position: absolute; top: 15px; right: 15px; padding: 4px 10px; border-radius: 5px; color: white; font-size: 0.7rem; font-weight: bold; background: #ff6a00; z-index: 10; }
    .product-img { max-height: 180px; width: 100%; object-fit: contain; margin-bottom: 15px; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# سعر الصرف في السكوار
EXCHANGE_RATE = 240 

if 'inventory' not in st.session_state:
    st.session_state['inventory'] = None

# 3. لوحة التحكم (Admin Sidebar)
with st.sidebar:
    st.title("🛡️ لوحة التحكم")
    if st.text_input("كود الأمان", type="password") == "dz2026":
        uploaded_file = st.file_uploader("ارفع ملف الإكسل (Alibaba)", type=['xlsx', 'csv'])
        if uploaded_file:
            try:
                df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
                df.columns = df.columns.astype(str).str.strip()

                # --- الربط المباشر مع أسماء الأعمدة في صورتك الأخيرة ---
                mapping = {
                    'product-title-text': 'Title',
                    'tp-inline-block': 'Price',
                    'product-title-text src': 'Img1',
                    'tp-h-full src': 'Img2',
                    'tp-w-6 src': 'Img3',
                    'tp-w-[18px] src': 'Img4',
                    'tp-me-1 href': 'Link',
                    'tp-text-sm href': 'Link_Alt',
                    'tp-inline-flex href': 'Link_Alt2'
                }
                
                df = df.rename(columns=mapping)
                st.session_state['inventory'] = df
                st.sidebar.success(f"✅ تم تحميل {len(df)} سلعة!")
            except Exception as e:
                st.sidebar.error(f"خطأ: {e}")

# 4. الواجهة الرئيسية
st.title("🌍 مركز التوريد العالمي - الجزائر")

if st.session_state['inventory'] is not None:
    # ميزة البحث (Search Bar)
    search_query = st.text_input("🔍 ابحث عن منتج بالاسم...", "")
    
    df = st.session_state['inventory']
    
    # تصفية المنتجات بناءً على البحث
    if search_query:
        df = df[df['Title'].str.contains(search_query, case=False, na=False)]

    cols = st.columns(4)
    for i, (idx, row) in enumerate(df.iterrows()):
        with cols[i % 4]:
            # جلب العنوان
            title = str(row.get('Title', 'بدون عنوان'))
            
            # معالجة السعر
            price_val = str(row.get('Price', '0'))
            try:
                p_str = price_val.replace(',', '.').replace(' ', '').replace('$', '').strip()
                p_clean = float(re.findall(r'\d+\.?\d*', p_str)[0])
            except:
                p_clean = 0.0

            # "رادار الصور" المتعدد بناءً على ملفك
            img = ""
            for col_img in ['Img1', 'Img2', 'Img3', 'Img4']:
                val = str(row.get(col_img, ''))
                if "http" in val or val.startswith("//"):
                    img = val
                    break
            
            if img.startswith('//'): img = 'https:' + img
            if not img: img = "https://via.placeholder.com/200?text=No+Image"

            # جلب الرابط الصحيح
            lnk = str(row.get('Link', row.get('Link_Alt', row.get('Link_Alt2', '#'))))

            # عرض بطاقة المنتج
            st.markdown(f'''
                <div class="product-card">
                    <div class="badge">بيع بالجملة</div>
                    <img src="{img}" class="product-img">
                    <div class="title">{title[:70]}...</div>
                    <div class="price-usd">{p_clean:,.2f} دولار</div>
                    <div class="price-dzd">≈ {int(p_clean * EXCHANGE_RATE):,} دج</div>
                </div>
            ''', unsafe_allow_html=True)
            st.link_button("تفاصيل المنتج 🤝", lnk, use_container_width=True)
            st.write("")
else:
    st.info("👋 ارفع ملف الإكسل من القائمة الجانبية (Admin) بالكود dz2026.")
