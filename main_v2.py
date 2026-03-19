import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="Global Sourcing Hub DZ", page_icon="📦", layout="wide")

# 2. تصميم CSS احترافي (يدعم الجملة والتجزئة)
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
    .badge { position: absolute; top: 15px; left: 15px; padding: 4px 10px; border-radius: 5px; color: white; font-size: 0.7rem; font-weight: bold; }
    .ali { background: #ff4747; } .alibaba { background: #ff6a00; } .other { background: #95a5a6; }
    .calc-box { background: #f9f9f9; border-radius: 8px; padding: 10px; margin-top: 10px; border: 1px dashed #ccc; }
    </style>
    """, unsafe_allow_html=True)

# إعداد سعر الصرف (السكوار)
EXCHANGE_RATE = 240 

if 'inventory' not in st.session_state:
    st.session_state['inventory'] = None

# 3. لوحة التحكم (Admin Sidebar)
with st.sidebar:
    st.title("🛡️ Admin Panel")
    if st.text_input("Security Key", type="password") == "dz2026":
        st.success("Access Granted")
        uploaded_file = st.file_uploader("Upload Scraped File (Ali/Alibaba)", type=['xlsx', 'csv'])
        
        if uploaded_file:
            try:
                # قراءة الملف
                df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
                df.columns = df.columns.astype(str).str.strip()

                # القاموس الذكي الشامل (Mapping) لفك شفرة ملفات السكرابر
                mapping = {
                    # العناوين
                    'subject': 'Title', 'product_name': 'Title', 'title': 'Title', 'Product Desc': 'Title', 'item_title': 'Title',
                    # الأسعار
                    'min_price': 'Price', 'price_range': 'Price', 'price': 'Price', 'unit_price': 'Price', 'Discount Price': 'Price',
                    # الصور
                    'product_image': 'Image', 'image_url': 'Image', 'image': 'Image', 'src': 'Image', 'imageUrl': 'Image', 'Product Main Image Url': 'Image',
                    # الروابط
                    'product_url': 'Link', 'url': 'Link', 'link': 'Link', 'Link': 'Link', 'Promotion Url': 'Link',
                    # الجملة (MOQ)
                    'min_order': 'MOQ', 'moq': 'MOQ', 'Min. Order': 'MOQ', 'min_order_quantity': 'MOQ'
                }
                
                df = df.rename(columns=mapping)
                st.session_state['inventory'] = df
                st.sidebar.success(f"✅ {len(df)} Items Loaded!")
            except Exception as e:
                st.sidebar.error(f"Error: {e}")

# 4. الواجهة الرئيسية
st.title("🌍 Global Sourcing Hub - Algeria")
st.markdown("##### *Your Gateway to Alibaba Wholesale & AliExpress Deals*")

if st.session_state['inventory'] is not None:
    df = st.session_state['inventory']
    
    # محرك البحث والفلترة
    col_search, col_cat = st.columns([2, 1])
    with col_search:
        q = st.text_input("🔍 Search for products, brands or suppliers...")
    with col_cat:
        if 'Category' in df.columns:
            cats = ["All Categories"] + sorted(df['Category'].dropna().unique().tolist())
            selected_cat = st.selectbox("📂 Category", cats)
        else:
            selected_cat = "All Categories"

    # تطبيق الفلترة
    display_df = df.copy()
    if q: display_df = display_df[display_df['Title'].str.contains(q, case=False, na=False)]
    if selected_cat != "All Categories": display_df = display_df[display_df['Category'] == selected_cat]

    st.divider()

    # 5. عرض المنتجات في 4 أعمدة
    cols = st.columns(4)
    for i, (idx, row) in enumerate(display_df.iterrows()):
        with cols[i % 4]:
            # جلب وتنظيف البيانات
            title = str(row.get('Title', 'No Title'))
            raw_price = str(row.get('Price', '0'))
            img = str(row.get('Image', ''))
            lnk = str(row.get('Link', '#'))
            moq_val = str(row.get('MOQ', '1'))

            # معالجة السعر (يأخذ القيمة الصغرى إذا كان هناك مجال)
            try:
                p_clean = float(raw_price.split('-')[0].replace('$', '').strip())
            except:
                p_clean = 0.0

            # تحديد نوع المنصة
            is_alibaba = 'alibaba.com' in lnk.lower()
            badge_class = "alibaba" if is_alibaba else "ali"
            badge_text = "WHOLESALE" if is_alibaba else "RETAIL"

            # تصحيح رابط الصورة
            if img.startswith('//'): img = 'https:' + img
            if not img.startswith('http'): img = "https://via.placeholder.com/200?text=No+Image"

            # إنشاء الكارد
            st.markdown(f'''
                <div class="product-card">
                    <div class="badge {badge_class}">{badge_text}</div>
                    <img src="{img}" style="width:100%; border-radius:12px; margin-top:20px; height:180px; object-fit:contain;">
                    <div class="title">{title[:55]}...</div>
                    <div class="price-usd">${p_clean:.2f}</div>
                    <div class="price-dzd">≈ {int(p_clean * EXCHANGE_RATE):,} DA</div>
            ''', unsafe_allow_html=True)

            # آلة حاسبة إذا كان المنتج من علي بابا (جملة)
            if is_alibaba:
                st.markdown('<div class="calc-box">', unsafe_allow_html=True)
                # استخراج رقم الـ MOQ
                try: moq_int = int(''.join(filter(str.isdigit, moq_val))) 
                except: moq_int = 1
                
                qty = st.number_input(f"Qty (Min: {moq_val})", min_value=1, value=moq_int, key=f"q_{idx}")
                total = qty * p_clean
                st.markdown(f'<span style="font-size:0.8rem; color:#666;">Total:</span> <b style="color:#e67e22;">${total:,.2f}</b>', unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:0.75rem; color:#888;">({int(total * EXCHANGE_RATE):,} DA)</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                st.link_button("🤝 Contact Supplier", lnk, use_container_width=True)
            else:
                st.markdown('<div style="height:115px;"></div>', unsafe_allow_html=True)
                st.link_button("🛒 Buy Now", lnk, use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)
            st.write("")
else:
    st.info("👋 Welcome! Go to the Admin Panel on the left, enter the key 'dz2026', and upload your Excel file to start.")
    st.image("https://via.placeholder.com/1200x400?text=Waiting+for+Inventory+Upload...", use_container_width=True)
