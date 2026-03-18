import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mega Store Hub", page_icon="🛍️", layout="wide")

# تصميم CSS (بطاقات السلع + التاجات)
st.markdown("""
    <style>
    .product-card {
        background: white; border-radius: 15px; padding: 15px;
        border: 1px solid #eee; text-align: center; height: 100%;
        transition: 0.3s ease;
    }
    .product-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
    .price { color: #2ecc71; font-weight: bold; font-size: 1.4rem; margin: 10px 0; }
    .title { font-size: 0.85rem; font-weight: 600; height: 45px; overflow: hidden; color: #333; }
    .category-tag { font-size: 0.7rem; color: #777; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

if 'inventory' not in st.session_state:
    st.session_state['inventory'] = None

# --- لوحة التحكم (Admin) ---
with st.sidebar:
    st.title("🛡️ Admin Panel")
    if st.text_input("Key", type="password") == "dz2026":
        file = st.file_uploader("Upload Excel File", type=['xlsx', 'csv'])
        if file:
            try:
                df = pd.read_excel(file) if file.name.endswith('xlsx') else pd.read_csv(file)
                df.columns = df.columns.astype(str).str.strip()
                
                # قاموس موسع لدعم جميع المنصات والأعمدة
                mapping = {
                    'Product Desc': 'Title', 'Product Name': 'Title', 'item_title': 'Title',
                    'Price': 'Price', 'sale_price': 'Price', 'Discount Price': 'Price',
                    'Image Url': 'Image', 'main_image': 'Image', 'Product Main Image Url': 'Image',
                    'Link': 'Link', 'Promotion Url': 'Link', 'url': 'Link',
                    'Category': 'Category', 'category': 'Category', 'Product Category': 'Category'
                }
                df = df.rename(columns=mapping)
                st.session_state['inventory'] = df
                st.sidebar.success(f"✅ Loaded {len(df)} Products!")
            except Exception as e:
                st.sidebar.error(f"Error: {e}")

# --- الواجهة الرئيسية ---
st.title("🛒 DZ Smart Marketplace")

if st.session_state['inventory'] is not None:
    df = st.session_state['inventory']
    
    # 1. إنشاء قائمة التصنيفات (Dynamic Dropdown)
    # نجبدو كامل الأصناف الموجودة في الإكسل بلا تكرار
    if 'Category' in df.columns:
        categories = ["All Categories"] + sorted(df['Category'].dropna().unique().tolist())
    else:
        categories = ["All Categories"]

    # 2. تصميم "ليستة ديرولونت" (الـ Filter)
    selected_cat = st.selectbox("📂 Select Category", categories)

    # 3. محرك البحث بالنص
    search_q = st.text_input("🔍 Search for a product...")

    # 4. عملية الفلترة (Filtering Logic)
    filtered_df = df.copy()
    
    # فلترة حسب التصنيف
    if selected_cat != "All Categories":
        filtered_df = filtered_df[filtered_df['Category'] == selected_cat]
    
    # فلترة حسب البحث
    if search_q:
        filtered_df = filtered_df[filtered_df['Title'].str.contains(search_q, case=False, na=False)]

    st.divider()

    # 5. عرض السلع
    if not filtered_df.empty:
        cols = st.columns(4)
        for i, (idx, row) in enumerate(filtered_df.iterrows()):
            with cols[i % 4]:
                t, p, img, lnk, cat = str(row.get('Title','')), str(row.get('Price','0')), str(row.get('Image','')), str(row.get('Link','#')), str(row.get('Category','General'))
                
                if img.startswith('//'): img = 'https:' + img
                if not img.startswith('http'): img = "https://via.placeholder.com/200"

                st.markdown(f'''
                    <div class="product-card">
                        <div class="category-tag">#{cat}</div>
                        <img src="{img}" style="width:100%; border-radius:10px;">
                        <div class="title">{t[:55]}...</div>
                        <div class="price">${p}</div>
                    </div>
                ''', unsafe_allow_html=True)
                st.link_button("🔥 Go to Deal", lnk, use_container_width=True)
                st.write("")
    else:
        st.warning("No products found in this category.")
else:
    st.info("👋 Admin: Upload the Excel file to show products and categories.")
