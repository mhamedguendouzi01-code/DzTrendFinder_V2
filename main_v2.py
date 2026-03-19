import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="Global Sourcing Hub DZ", page_icon="📦", layout="wide")

# 2. تصميم CSS احترافي
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
    .ali { background: #ff4747; } .alibaba { background: #ff6a00; }
    .calc-box { background: #f9f9f9; border-radius: 8px; padding: 10px; margin-top: 10px; border: 1px dashed #ccc; }
    </style>
    """, unsafe_allow_html=True)

# سعر الصرف (السكوار)
EXCHANGE_RATE = 240 

if 'inventory' not in st.session_state:
    st.session_state['inventory'] = None

# 3. لوحة التحكم (Sidebar)
with st.sidebar:
    st.title("🛡️ Admin Panel")
    key = st.text_input("Security Key", type="password")
    if key == "dz2026":
        uploaded_file = st.file_uploader("Upload Scraped File (Alibaba/AliExpress)", type=['xlsx', 'csv'])
        if uploaded_file:
            try:
                df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
                df.columns = df.columns.astype(str).str.strip()

                # القاموس السحري: هنا الحل! يربط أسامي أعمدة علي بابا بالكود
                mapping = {
                    'subject': 'Title', 'product_name': 'Title', 'title': 'Title', 'item_title': 'Title',
                    'min_price': 'Price', 'price_range': 'Price', 'price': 'Price', 'unit_price': 'Price',
                    'product_image': 'Image', 'image_url': 'Image', 'image': 'Image', 'src': 'Image', 'imageUrl': 'Image',
                    'product_url': 'Link', 'url': 'Link', 'link': 'Link', 'Link': 'Link',
                    'min_order': 'MOQ', 'moq': 'MOQ', 'Min. Order': 'MOQ'
                }
                
                df = df.rename(columns=mapping)
                st.session_state['inventory'] = df
                st.sidebar.success(f"✅ {len(df)} Items Loaded!")
            except Exception as e:
                st.sidebar.error(f"Error reading file: {e}")

# 4. الواجهة الرئيسية
st.title("🌍 Global Sourcing Hub - Algeria")

if st.session_state['inventory'] is not None:
    df = st.session_state['inventory']
    
    # عرض المنتجات
    cols = st.columns(4)
    for i, (idx, row) in enumerate(df.iterrows()):
        with cols[i % 4]:
            # جلب البيانات
            title = str(row.get('Title', 'No Title'))
            raw_price = str(row.get('Price', '0'))
            img = str(row.get('Image', ''))
            lnk = str(row.get('Link', '#'))
            moq_val = str(row.get('MOQ', '1'))

            # تنظيف السعر (لأن علي بابا يعطي مجال مثل $2.00 - $3.00)
            try:
                p_clean = float(raw_price.split('-')[0].replace('$', '').replace(',', '').strip())
            except:
                p_clean = 0.0

            # تحديد المنصة
            is_alibaba = 'alibaba' in lnk.lower()
            badge_class = "alibaba" if is_alibaba else "ali"
            badge_text = "WHOLESALE" if is_alibaba else "RETAIL"

            # تصحيح روابط صور علي بابا
            if img.startswith('//'): img = 'https:' + img
            if not img.startswith('http'): img = "https://via.placeholder.com/200?text=No+Image"

            st.markdown(f'''
                <div class="product-card">
                    <div class="badge {badge_class}">{badge_text}</div>
                    <img src="{img}" style="width:100%; border-radius:12px; margin-top:20px; height:180px; object-fit:contain;">
                    <div class="title">{title[:50]}...</div>
                    <div class="price-usd">${p_clean:.2f}</div>
                    <div class="price-dzd">≈ {int(p_clean * EXCHANGE_RATE):,} DA</div>
            ''', unsafe_allow_html=True)

            if is_alibaba:
                st.markdown('<div class="calc-box">', unsafe_allow_html=True)
                qty = st.number_input(f"Qty", min_value=1, value=1, key=f"q_{idx}")
                total = qty * p_clean
                st.markdown(f'Total: <b style="color:#e67e22;">${total:,.2f}</b>', unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:0.8rem; color:#888;">({int(total * EXCHANGE_RATE):,} DA)</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                st.link_button("🤝 Contact Supplier", lnk, use_container_width=True)
            else:
                st.markdown('<div style="height:115px;"></div>', unsafe_allow_html=True)
                st.link_button("🛒 Buy Now", lnk, use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)
            st.write("")
else:
    st.info("👋 Welcome! Please upload your Excel file from the sidebar.")
