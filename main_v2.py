import streamlit as st
import pandas as pd

st.set_page_config(page_title="Global Sourcing & Retail Hub", layout="wide")

# --- تصميم CSS متطور جداً ---
st.markdown("""
    <style>
    .product-card {
        background: white; border-radius: 20px; padding: 20px;
        border: 1px solid #f0f0f0; text-align: center; height: 100%;
        transition: 0.4s ease; position: relative;
    }
    .product-card:hover { transform: translateY(-10px); box-shadow: 0 15px 30px rgba(0,0,0,0.1); }
    .price-tag { color: #27ae60; font-weight: bold; font-size: 1.5rem; margin-bottom: 5px; }
    .price-dzd { color: #7f8c8d; font-size: 0.9rem; margin-bottom: 10px; font-weight: 500; }
    .title { font-size: 0.9rem; font-weight: 600; height: 45px; overflow: hidden; color: #2c3e50; margin-bottom: 15px; }
    .badge { position: absolute; top: 15px; left: 15px; padding: 4px 12px; border-radius: 50px; color: white; font-size: 0.7rem; font-weight: bold; }
    .ali { background: linear-gradient(45deg, #ff4747, #ff8c8c); }
    .alibaba { background: linear-gradient(45deg, #ff6a00, #ee0979); }
    .calc-box { background: #f8f9fa; border-radius: 10px; padding: 10px; margin-top: 10px; border: 1px dashed #ddd; }
    .total-price { color: #e67e22; font-weight: bold; font-size: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# إعدادات العملة (تقدر تبدل سعر السكوار هنا)
EXCHANGE_RATE = 240 

if 'inventory' not in st.session_state: st.session_state['inventory'] = None

# --- الجانب الإداري ---
with st.sidebar:
    st.title("🛡️ Admin Console")
    if st.text_input("Security Key", type="password") == "dz2026":
        file = st.file_uploader("Upload Master File (Ali/Alibaba/Temu)", type=['xlsx', 'csv'])
        if file:
            df = pd.read_excel(file) if file.name.endswith('xlsx') else pd.read_csv(file)
            df.columns = df.columns.astype(str).str.strip()
            # القاموس الذكي
            mapping = {
                'Product Desc': 'Title', 'title': 'Title', 'Price': 'Price', 'price': 'Price',
                'Image Url': 'Image', 'image': 'Image', 'Link': 'Link', 'url': 'Link',
                'MOQ': 'MOQ', 'Min. Order': 'MOQ', 'Category': 'Category'
            }
            st.session_state['inventory'] = df.rename(columns=mapping)
            st.success("Database Updated!")

st.title("🛍️ Global Sourcing & Retail Hub")
st.markdown("---")

if st.session_state['inventory'] is not None:
    df = st.session_state['inventory']
    
    # فلترة ذكية
    col1, col2 = st.columns([1, 2])
    with col1:
        cats = ["All Categories"] + sorted(df['Category'].dropna().unique().tolist()) if 'Category' in df.columns else ["All Categories"]
        selected_cat = st.selectbox("📂 Category", cats)
    with col2:
        search = st.text_input("🔍 Search for products or suppliers...")

    # منطق الفلترة
    display_df = df
    if selected_cat != "All Categories": display_df = display_df[display_df['Category'] == selected_cat]
    if search: display_df = display_df[display_df['Title'].str.contains(search, case=False, na=False)]

    # --- عرض المنتجات ---
    cols = st.columns(4)
    for i, (idx, row) in enumerate(display_df.iterrows()):
        with cols[i % 4]:
            t, p, img, lnk = str(row.get('Title','')), row.get('Price', 0), str(row.get('Image','')), str(row.get('Link',''))
            moq = str(row.get('MOQ', '1'))
            
            # تنظيف السعر (إذا كان مكتوب كـ "10.5 - 15.0" يدي القيمة الأولى)
            try:
                p_clean = float(str(p).split('-')[0].replace('$', '').strip())
            except:
                p_clean = 0.0

            # تحديد نوع المتجر
            is_wholesale = 'alibaba' in lnk.lower()
            b_class = "alibaba" if is_wholesale else "ali"
            b_name = "Wholesale (Joumala)" if is_wholesale else "Retail (Affiliate)"

            st.markdown(f'''
                <div class="product-card">
                    <div class="badge {b_class}">{b_name}</div>
                    <img src="{img if 'http' in img else 'https://via.placeholder.com/150'}" style="width:100%; border-radius:15px; margin-top:20px;">
                    <div class="title">{t[:50]}...</div>
                    <div class="price-tag">${p_clean:.2f}</div>
                    <div class="price-dzd">≈ {int(p_clean * EXCHANGE_RATE):,} DA</div>
            ''', unsafe_allow_html=True)

            # إذا كانت جملة (علي بابا)، نزيدو آلة حاسبة
            if is_wholesale:
                st.markdown('<div class="calc-box">', unsafe_allow_html=True)
                qty = st.number_input(f"Qty (Min: {moq})", min_value=1, value=int(moq) if moq.isdigit() else 1, key=f"qty_{idx}")
                total = qty * p_clean
                st.markdown(f'Total: <span class="total-price">${total:,.2f}</span>', unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:0.8rem; color:#888;">({int(total*EXCHANGE_RATE):,} DA)</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                st.link_button("🤝 Contact Supplier", lnk, use_container_width=True)
            else:
                st.markdown('<div style="height:115px;"></div>', unsafe_allow_html=True) # موازنة الطول
                st.link_button("🛒 Buy Now", lnk, use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)
            st.write("")
else:
    st.info("Please upload your inventory file to begin.")
