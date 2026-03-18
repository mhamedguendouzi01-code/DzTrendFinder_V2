import streamlit as st
import pandas as pd

st.set_page_config(page_title="Global Deals Hub", layout="wide")

# تصميم احترافي للمنصة
st.markdown("""
    <style>
    .product-card {
        background: white; border-radius: 15px; padding: 15px;
        border: 1px solid #eee; text-align: center; height: 100%;
    }
    .price { color: #e63946; font-size: 1.5rem; font-weight: bold; }
    .title { font-size: 0.9rem; height: 50px; overflow: hidden; margin-bottom: 10px; }
    img { border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

if 'data' not in st.session_state: st.session_state['data'] = None

with st.sidebar:
    st.title("🤖 Auto-Pilot Admin")
    pwd = st.text_input("Password", type="password")
    if pwd == "dz2026":
        # هنا ترفع الملف اللي تيليشارجيتو من AliExpress ديريكت
        uploaded_file = st.file_uploader("Upload AliExpress Export (Excel/CSV)", type=['xlsx', 'csv'])
        if uploaded_file:
            df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
            
            # الكود ذكي: يحوس على الأعمدة مهما كان اسمها
            mapping = {
                'Product Name': 'Title', 'Product Title': 'Title',
                'Sale Price': 'Price', 'Price': 'Price',
                'Product Main Image Url': 'Image', 'ImageUrl': 'Image', 'Image URL': 'Image',
                'Promotion Link': 'Link', 'Product Detail Url': 'Link', 'Affiliate Link': 'Link'
            }
            df = df.rename(columns=mapping)
            st.session_state['data'] = df
            st.success(f"🚀 {len(df)} Products Loaded Automatically!")

st.title("🌍 Global Deals Hub")

if st.session_state['data'] is not None:
    df = st.session_state['data']
    cols = st.columns(4)
    for i, row in df.iterrows():
        with cols[i % 4]:
            with st.container():
                # جلب البيانات أوتوماتيكياً
                t = row.get('Title', 'No Title')
                p = row.get('Price', '0.00')
                img = row.get('Image', '')
                lnk = row.get('Link', '#')
                
                st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
                if str(img) != 'nan': st.image(img, use_container_width=True)
                st.markdown(f'<div class="title">{str(t)[:60]}...</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="price">${p}</div>', unsafe_allow_html=True)
                st.link_button("🔥 Get Deal", str(lnk), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                st.write("")
else:
    st.info("👋 Welcome! Admin: Just upload the file from AliExpress Ad Center.")
