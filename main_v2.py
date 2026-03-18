import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="Global Deals Hub", page_icon="🌍", layout="wide")

# 2. تصميم CSS عصري
st.markdown("""
    <style>
    .product-card {
        background-color: white;
        border-radius: 15px;
        padding: 10px;
        border: 1px solid #efefef;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .stImage > img {
        border-radius: 10px;
        max-height: 180px;
        object-fit: contain;
    }
    .price { color: #1a73e8; font-weight: bold; font-size: 1.2rem; }
    .title { font-size: 0.9rem; font-weight: 600; height: 40px; overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة البيانات (تخزين السلع في الجلسة)
if 'products_list' not in st.session_state:
    st.session_state['products_list'] = []

# 4. لوحة التحكم (Sidebar) - إضافة يدوية
with st.sidebar:
    st.title("🔐 Admin Panel")
    pwd = st.text_input("Password", type="password")
    
    if pwd == "dz2026":
        st.success("Access Granted!")
        st.subheader("➕ Add New Product")
        new_title = st.text_input("Product Title")
        new_price = st.text_input("Price (e.g. 25.00)")
        new_img = st.text_input("Image URL (Direct link .jpg/.png)")
        new_link = st.text_input("Affiliate Link")
        new_platform = st.selectbox("Platform", ["AliExpress", "Amazon", "Temu", "Other"])
        
        if st.button("🚀 Add Product"):
            if new_title and new_img:
                new_item = {
                    "Title": new_title,
                    "Price": new_price,
                    "Image": new_img,
                    "Link": new_link,
                    "Platform": new_platform
                }
                st.session_state['products_list'].append(new_item)
                st.sidebar.balloons()
                st.success("Added!")
            else:
                st.error("Title and Image URL are required!")

        st.divider()
        if st.button("🗑️ Clear All Products"):
            st.session_state['products_list'] = []
            st.rerun()

# 5. الواجهة الرئيسية
st.title("🌍 Global Deals Hub")
st.write("Viral Products Dashboard - Manual Entry Mode")

if st.session_state['products_list']:
    # محرك البحث
    search = st.text_input("🔍 Search products...", "")
    
    # تصفية البيانات حسب البحث
    items_to_show = st.session_state['products_list']
    if search:
        items_to_show = [i for i in items_to_show if search.lower() in i['Title'].lower()]

    st.divider()
    
    # عرض السلع في 4 أعمدة
    cols = st.columns(4)
    for index, item in enumerate(items_to_show):
        with cols[index % 4]:
            with st.container():
                # عرض الصورة
                img_url = item['Image'].strip()
                if img_url.startswith('http'):
                    st.image(img_url, use_container_width=True)
                else:
                    st.image("https://via.placeholder.com/150?text=Invalid+Link", use_container_width=True)
                
                # النصوص والبوطونة
                st.markdown(f"<div class='title'>{item['Title'][:45]}...</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='price'>${item['Price']}</div>", unsafe_allow_html=True)
                st.caption(f"📍 {item['Platform']}")
                st.link_button("🔥 View Deal", item['Link'], use_container_width=True)
                st.write("") 
else:
    st.info("👋 Welcome! Use the sidebar on the left to add your first product manually.")
