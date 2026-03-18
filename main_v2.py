import streamlit as st
import pandas as pd

st.set_page_config(page_title="Global Deals Hub", layout="wide")

# تصميم الواجهة
st.markdown("""
    <style>
    .product-card {
        background: white; border-radius: 12px; padding: 15px;
        border: 1px solid #e0e0e0; text-align: center; margin-bottom: 20px;
    }
    .price { color: #d32f2f; font-weight: bold; font-size: 1.3rem; }
    .title { font-size: 0.85rem; font-weight: 600; height: 45px; overflow: hidden; margin-top: 10px; }
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
                # قراءة الملف
                df = pd.read_excel(file) if file.name.endswith('xlsx') else pd.read_csv(file)
                df.columns = df.columns.astype(str).str.strip() # تنظيف العناوين
                
                # القاموس المحدث حسب الأعمدة اللي بعثتهم ذرك
                rename_dict = {
                    'Product Desc': 'Title', 
                    'Product Name': 'Title', 
                    'Product Title': 'Title',
                    'Price': 'Price', 
                    'Discount Price': 'Price',
                    'Image Url': 'Image', 
                    'Product Main Image Url': 'Image',
                    'Link': 'Link', 
                    'Promotion Url': 'Link'
                }
                df = df.rename(columns=rename_dict)
                
                # التحقق من الأعمدة
                needed = ['Title', 'Price', 'Image', 'Link']
                found = [c for c in needed if c in df.columns]
                
                if len(found) >= 4:
                    st.session_state['inventory'] = df
                    st.sidebar.success(f"✅ {len(df)} Items Loaded!")
                else:
                    st.sidebar.error(f"Missing columns. Found: {list(df.columns)}")
                    st.sidebar.info("I need: Product Desc, Price, Image Url, and Link")
            except Exception as e:
                st.sidebar.error(f"Error: {e}")

st.title("🌍 Global Deals Hub")

if st.session_state['inventory'] is not None:
    df = st.session_state['inventory']
    cols = st.columns(4)
    for i, row in df.iterrows():
        with cols[i % 4]:
            # جلب البيانات
            t = str(row.get('Title', 'No Title'))
            p = str(row.get('Price', '0.00'))
            img = str(row.get('Image', ''))
            lnk = str(row.get('Link', '#'))

            # تصحيح رابط الصورة
            if img.startswith('//'): img = 'https:' + img
            if img == 'nan' or not img.startswith('http'):
                img = "https://via.placeholder.com/200?text=No+Image"

            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            try:
                st.image(img, use_container_width=True)
            except:
                st.image("https://via.placeholder.com/200?text=Image+Error", use_container_width=True)
            
            st.markdown(f'<div class="title">{t[:50]}...</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="price">${p}</div>', unsafe_allow_html=True)
            st.link_button("🔥 Buy Now", lnk, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.write("")
else:
    st.info("👋 Upload the file from AliExpress to start!")
