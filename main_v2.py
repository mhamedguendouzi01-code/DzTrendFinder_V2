import streamlit as st
import pandas as pd

st.set_page_config(page_title="Global Deals Hub", layout="wide")

# تصميم CSS
st.markdown("""
    <style>
    .product-card {
        background: white; border-radius: 12px; padding: 15px;
        border: 1px solid #e0e0e0; text-align: center; margin-bottom: 20px;
    }
    .price { color: #d32f2f; font-weight: bold; font-size: 1.3rem; }
    .title { font-size: 0.9rem; font-weight: 600; height: 45px; overflow: hidden; margin-top: 10px; }
    img { border-radius: 8px; max-height: 160px; object-fit: contain; }
    </style>
    """, unsafe_allow_html=True)

if 'inventory' not in st.session_state:
    st.session_state['inventory'] = None

with st.sidebar:
    st.title("🛡️ Admin Panel")
    key = st.text_input("Security Key", type="password")
    if key == "dz2026":
        st.success("Authorized")
        file = st.file_uploader("Upload AliExpress Excel", type=['xlsx', 'csv'])
        if file:
            try:
                df = pd.read_excel(file) if file.name.endswith('xlsx') else pd.read_csv(file)
                # تنظيف أسماء الأعمدة (حذف الفراغات)
                df.columns = df.columns.str.strip()
                
                # قاموس التصحيح التلقائي لأسماء الأعمدة
                rename_dict = {
                    'Product Name': 'Title', 'Product Title': 'Title',
                    'Sale Price': 'Price', 'Target Sale Price': 'Price',
                    'Product Main Image Url': 'Image', 'ImageUrl': 'Image',
                    'Promotion Link': 'Link', 'Product Detail Url': 'Link'
                }
                df = df.rename(columns=rename_dict)
                
                # التأكد من وجود الأعمدة الأساسية
                required = ['Title', 'Price', 'Image', 'Link']
                missing = [c for c in required if c not in df.columns]
                
                if not missing:
                    st.session_state['inventory'] = df
                    st.sidebar.success(f"✅ {len(df)} Items Loaded!")
                else:
                    st.sidebar.error(f"Missing columns: {missing}")
                    st.sidebar.info("Make sure your Excel has headers like: Product Name, Sale Price, etc.")
            except Exception as e:
                st.sidebar.error(f"Error: {e}")

st.title("🌍 Global Deals Hub")

if st.session_state['inventory'] is not None:
    df = st.session_state['inventory']
    cols = st.columns(4)
    
    for i, row in df.iterrows():
        with cols[i % 4]:
            # جلب البيانات مع قيم افتراضية إذا كانت فارغة
            title = str(row.get('Title', 'No Title'))
            price = str(row.get('Price', '0.00'))
            img = str(row.get('Image', ''))
            link = str(row.get('Link', '#'))

            # تصحيح رابط الصورة
            if img.startswith('//'): img = 'https:' + img
            if img == 'nan' or not img.startswith('http'):
                img = "https://via.placeholder.com/200?text=No+Image"

            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            try:
                st.image(img, use_container_width=True)
            except:
                st.image("https://via.placeholder.com/200?text=Image+Error", use_container_width=True)
            
            st.markdown(f'<div class="title">{title[:50]}...</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="price">${price}</div>', unsafe_allow_html=True)
            st.link_button("🔥 View Deal", link, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.write("")
else:
    st.info("👋 Welcome! Upload the file from AliExpress Ad Center to populate the store.")
