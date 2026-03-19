import streamlit as st
import pandas as pd
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="مركز التوريد العالمي - الجزائر", page_icon="🌍", layout="wide")

# 2. تصميم CSS احترافي (عربي 100%)
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
    .product-card:hover { transform: translateY(-8px); box-shadow: 0 12px 24px rgba(0,0,0,0.1); }
    .price-usd { color: #27ae60; font-weight: bold; font-size: 1.4rem; margin: 5px 0; }
    .price-dzd { color: #7f8c8d; font-size: 0.95rem; font-weight: 500; margin-bottom: 10px; }
    .title { font-size: 0.85rem; font-weight: 600; min-height: 50px; overflow: hidden; color: #333; margin-bottom: 10px; line-height: 1.4; }
    .badge { position: absolute; top: 15px; right: 15px; padding: 4px 10px; border-radius: 5px; color: white; font-size: 0.7rem; font-weight: bold; background: #ff6a00; z-index: 10; }
    .product-img { max-height: 200px; width: 100%; object-fit: contain; margin-bottom: 15px; border-radius: 10px; background: #f9f9f9; }
    </style>
    """, unsafe_allow_html=True)

# سعر السكوار الحالي
EXCHANGE_RATE = 240 

if 'inventory' not in st.session_state:
    st.session_state['inventory'] = None

# 3. لوحة التحكم (Admin Sidebar)
with st.sidebar:
    st.title("🛡️ لوحة التحكم")
    if st.text_input("كود الأمان", type="password") == "dz2026":
        uploaded_file = st.file_uploader("ارفع ملف علي بابا الأخير", type=['xlsx', 'csv'])
        if uploaded_file:
            try:
                df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
                # تنظيف أسماء الأعمدة
                df.columns = [str(col).strip() for col in df.columns]
                st.session_state['inventory'] = df
                st.sidebar.success(f"✅ تم تحميل {len(df)} سلعة بنجاح!")
            except Exception as e:
                st.sidebar.error(f"خطأ في قراءة الملف: {e}")

# 4. الواجهة الرئيسية
st.title("🌍 مركز التوريد العالمي - الجزائر")

if st.session_state['inventory'] is not None:
    df = st.session_state['inventory']
    
    # محرك البحث
    search_q = st.text_input("🔍 ابحث عن منتج بالاسم...", "")
    if search_q:
        # البحث في عمود العنوان (نحاول تخمين اسم العمود)
        title_col = next((c for c in df.columns if 'title' in c.lower() or 'product' in c.lower()), df.columns[0])
        df = df[df[title_col].astype(str).str.contains(search_q, case=False, na=False)]

    cols = st.columns(4)
    for i, (idx, row) in enumerate(df.iterrows()):
        with cols[i % 4]:
            # --- منطق استخراج البيانات الذكي ---
            
            # 1. استخراج العنوان
            title = str(row.get('product-title-text', row.get('product', row.get('Title', 'بدون عنوان'))))
            
            # 2. استخراج وتنظيف السعر
            price_raw = str(row.get('tp-inline-block', row.get('tp-inlin', row.get('Price', '0'))))
            try:
                p_clean = float(re.findall(r'\d+\.?\d*', price_raw.replace(',', '.'))[0])
            except:
                p_clean = 0.0

            # 3. "رادار الصور" المطور (يحل مشكلة الاختفاء)
            # يبحث عن أي عمود ينتهي بـ "src" أو يحتوي على رابط صورة
            img = ""
            img_columns = [c for c in df.columns if 'src' in c.lower() or 'image' in c.lower() or 'img' in c.lower()]
            
            for col in img_columns:
                val = str(row.get(col, ''))
                if ("http" in val or val.startswith("//")) and "flag" not in val.lower() and "icon" not in val.lower():
                    img = val
                    break
            
            if img.startswith('//'): img = 'https:' + img
            # إذا لم يجد صورة، نضع صورة افتراضية احترافية
            if not img or len(img) < 10: img = "https://via.placeholder.com/300x200?text=No+Image+Available"

            # 4. استخراج الرابط
            lnk = str(row.get('tp-me-1 href', row.get('tp-text-sm href', row.get('Link', '#'))))

            # عرض البطاقة
            st.markdown(f'''
                <div class="product-card">
                    <div class="badge">جملة</div>
                    <img src="{img}" class="product-img">
                    <div class="title">{title[:75]}...</div>
                    <div class="price-usd">{p_clean:,.2f} دولار</div>
                    <div class="price-dzd">≈ {int(p_clean * EXCHANGE_RATE):,} دج</div>
                </div>
            ''', unsafe_allow_html=True)
            st.link_button("تفاصيل المنتج 🤝", lnk, use_container_width=True)
            st.write("")
else:
    st.info("👋 يا محمد، السيت جاهز. ارفع ملف الإكسل من القائمة الجانبية (Admin).")
