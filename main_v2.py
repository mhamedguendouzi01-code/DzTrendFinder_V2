import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="DZ Trend Finder", page_icon="🛍️", layout="wide")

# 2. تصميم CSS احترافي وعصري
st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    .product-card {
        background-color: white; border-radius: 15px; padding: 15px;
        border: 1px solid #eee; text-align: center;
        transition: 0.3s ease; height: 100%;
    }
    .product-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
    .price { color: #e63946; font-weight: bold; font-size: 1.4rem; margin: 10px 0; }
    .title { font-size: 0.9rem; font-weight: 600; height: 45px; overflow: hidden; color: #333; margin-bottom: 10px; }
    img { border-radius: 10px; margin-bottom: 10px; object-fit: contain; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #000; color: #fff; }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة البيانات
if 'inventory' not in st.session_state:
    st.session_state['inventory'] = None

# 4. لوحة التحكم (Sidebar)
with st.sidebar:
    st.title("🛡️ Admin Panel")
    pwd = st.text_input("Security Key", type="password")
    
    if pwd == "dz2026":
        st.success("Authorized")
        uploaded_file = st.file_uploader("Upload AliExpress Excel", type=['xlsx', 'csv'])
        
        if uploaded_file:
            try:
                # قراءة الملف حسب النوع
                df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
                df.columns = df.columns.astype(str).str.strip() # تنظيف العناوين
                
                # قاموس ذكي لترجمة أعمدة علي إكسبريس (النسخة الرمادية)
                rename_dict = {
                    'Product Desc': 'Title', 'Product Name': 'Title', 'Product Title': 'Title',
                    'Price': 'Price', 'Discount Price': 'Price', 'Sale Price': 'Price',
                    'Image Url': 'Image', 'Product Main Image Url': 'Image', 'ImageUrl': 'Image',
                    'Link': 'Link', 'Promotion Url': 'Link', 'Promotion Link': 'Link'
                }
                df = df.rename(columns=rename_dict)
                
                # حفظ البيانات في الجلسة
                st.session_state['inventory'] = df
                st.sidebar.success(f"✅ Loaded {len(df)} products!")
            except Exception as e:
                st.sidebar.error(f"Error: {e}")

# 5. الواجهة الرئيسية
st.title("🛍️ DZ Trend Finder")
st.markdown("#### *Find the best deals from AliExpress in one place*")

if st.session_state['inventory'] is not None:
    inventory_df = st.session_state['inventory']
    
    # محرك بحث بسيط
    search = st.text_input("🔍 Search products...", placeholder="What are you looking for?")
    
    if search:
        display_df = inventory_df[inventory_df['Title'].str.contains(search, case=False, na=False)]
    else:
        display_df = inventory_df

    st.divider()

    # 6. عرض السلع في 4 أعمدة
    if not display_df.empty:
        cols = st.columns(4)
        for i, (index, row) in enumerate(display_df.iterrows()):
            with cols[i % 4]:
                # جلب البيانات
                t = str(row.get('Title', 'No Title'))
                p = str(row.get('Price', '0.00'))
                img = str(row.get('Image', ''))
                lnk = str(row.get('Link', '#'))

                # تصحيح روابط الصور (https:)
                if img.startswith('//'): img = 'https:' + img
                if img == 'nan' or not img.startswith('http'):
                    img = "https://via.placeholder.com/200?text=Check+Link"

                # الكارد الخاص بالمنتج
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                try:
                    st.image(img, use_container_width=True)
                except:
                    st.image("https://via.placeholder.com/200?text=Image+Error", use_container_width=True)
                
                st.markdown(f'<div class="title">{t[:55]}...</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="price">${p}</div>', unsafe_allow_html=True)
                st.link_button("🔥 View Deal", lnk, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                st.write("") # مسافة صغيرة
    else:
        st.warning("No products matching your search.")
else:
    st.info("👋 Welcome! Please upload your AliExpress Excel file from the Admin Panel on the left.")
    st.image("https://via.placeholder.com/1000x300?text=Waiting+for+Inventory+Upload...", use_container_width=True)
