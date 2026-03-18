import streamlit as st
import pandas as pd

# 1. إعدادات المنصة العالمية
st.set_page_config(page_title="Global Deals Hub", page_icon="🌍", layout="wide")

# 2. تصميم CSS احترافي (Modern Global Look)
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .product-card {
        background-color: white;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #e0e0e0;
        text-align: center;
        transition: 0.3s ease-in-out;
    }
    .product-card:hover { 
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.1); 
    }
    .price { color: #d32f2f; font-weight: bold; font-size: 1.4rem; margin: 5px 0; }
    .title { font-size: 0.95rem; font-weight: 600; height: 50px; overflow: hidden; color: #333; margin-bottom: 10px; }
    img { border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة البيانات (تخزين السلع)
if 'inventory' not in st.session_state:
    st.session_state['inventory'] = None

# 4. لوحة التحكم (Admin Panel)
with st.sidebar:
    st.title("🛡️ Admin Dashboard")
    pwd = st.text_input("Security Key", type="password")
    
    if pwd == "dz2026":
        st.success("Access Granted")
        st.subheader("📦 Bulk Upload (AliExpress)")
        
        # رفع الملف اللي يخرج من AliExpress Ad Center ديريكت
        uploaded_file = st.file_uploader("Upload Excel/CSV from AliExpress", type=['xlsx', 'csv'])
        
        if uploaded_file:
            try:
                # قراءة الملف
                if uploaded_file.name.endswith('xlsx'):
                    df = pd.read_excel(uploaded_file)
                else:
                    df = pd.read_csv(uploaded_file)
                
                # تنظيف أسماء الأعمدة (Mapping) باش الكود يفهم أي ملف ترفعه
                mapping = {
                    'Product Name': 'Title', 'Product Title': 'Title', 'Title': 'Title',
                    'Sale Price': 'Price', 'Price': 'Price', 'Target Sale Price': 'Price',
                    'Product Main Image Url': 'Image', 'ImageUrl': 'Image', 'Image URL': 'Image',
                    'Promotion Link': 'Link', 'Product Detail Url': 'Link', 'Affiliate Link': 'Link'
                }
                df = df.rename(columns=mapping)
                st.session_state['inventory'] = df
                st.sidebar.success(f"🚀 Loaded {len(df)} products!")
            except Exception as e:
                st.error(f"Error reading file: {e}")

        if st.button("🗑️ Reset All"):
            st.session_state['inventory'] = None
            st.rerun()

# 5. الواجهة الرئيسية
st.title("🌍 Global Deals Hub")
st.markdown("#### *Direct Deals from AliExpress - Automated Catalog*")

if st.session_state['inventory'] is not None:
    df = st.session_state['inventory']
    
    # محرك البحث
    search = st.text_input("🔍 Search products...", placeholder="Find your deal...")
    if search:
        df = df[df['Title'].str.contains(search, case=False, na=False)]

    st.divider()
    
    # عرض السلع في 4 أعمدة
    cols = st.columns(4)
    for i, row in df.iterrows():
        with cols[i % 4]:
            # جلب وتصحيح البيانات
            title = str(row.get('Title', 'Product'))
            price = str(row.get('Price', '0.00'))
            img = str(row.get('Image', ''))
            link = str(row.get('Link', '#'))

            # --- تصحيح رابط الصورة السحري ---
            if img.startswith('//'):
                img = 'https:' + img
            elif not img.startswith('http') or img == 'nan':
                img = "https://via.placeholder.com/200x200?text=No+Image"

            # العرض داخل كارد
            with st.container():
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                
                # محاولة عرض الصورة بأمان لتفادي الـ Error
                try:
                    st.image(img, use_container_width=True)
                except:
                    st.image("https://via.placeholder.com/200x200?text=Image+Error", use_container_width=True)
                
                st.markdown(f'<div class="title">{title[:55]}...</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="price">${price}</div>', unsafe_allow_html=True)
                st.link_button("🔥 View Deal", link, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                st.write("") # فراغ بين السطور
else:
    st.info("👋 Welcome! Go to Sidebar -> Upload the Excel file you got from AliExpress.")
    st.image("https://via.placeholder.com/1000x300?text=Waiting+for+Inventory+Upload...", use_container_width=True)
