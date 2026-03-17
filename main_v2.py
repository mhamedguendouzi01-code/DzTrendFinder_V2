import streamlit as st
import pandas as pd

# إعدادات واجهة المستخدم
st.set_page_config(page_title="Global Deals Hub", page_icon="🌍", layout="wide")

# إخفاء عناصر Streamlit الزائدة ليعطيك مظهر احترافي
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# كلمة المرور للدخول للوحة التحكم
PASSWORD = "dz2026"

# لوحة التحكم في الجانب (Sidebar)
st.sidebar.title("🔐 Admin Panel")
pwd_input = st.sidebar.text_input("Password", type="password")

if pwd_input == PASSWORD:
    st.sidebar.success("Access Granted!")
    st.sidebar.markdown("---")
    st.sidebar.subheader("📦 Bulk Upload")
    
    # زر رفع ملف الإكسل
    uploaded_file = st.sidebar.file_uploader("Choose Excel File", type=['xlsx'])

    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            st.session_state['products'] = df.to_dict('records')
            st.sidebar.success(f"Loaded {len(df)} products!")
        except Exception as e:
            st.sidebar.error(f"Error reading file: {e}")

# واجهة العرض الرئيسية
st.title("🌍 Global Deals Hub")
st.markdown("### Discover Viral Gadgets: Amazon, AliExpress & Temu")
st.markdown("---")

# عرض السلع إذا كانت موجودة
if 'products' in st.session_state and st.session_state['products']:
    products = st.session_state['products']
    
    # عرض السلع في شكل شبكة (Grid) من 3 أعمدة
    cols = st.columns(3)
    for idx, item in enumerate(products):
        with cols[idx % 3]:
            # عرض الصورة
            img = item.get('Image URL', 'https://via.placeholder.com/300')
            st.image(img, use_container_width=True)
            
            # معلومات السلعة
            st.subheader(item.get('Product Title', 'No Title'))
            st.write(f"**Price:** ${item.get('Price', '0.00')}")
            st.write(f"**Platform:** {item.get('Platform', 'Store')}")
            
            # زر الرابط (Affiliate Link)
            link = item.get('Affiliate Link', '#')
            st.markdown(f"[🔗 View Deal]({link})")
            st.markdown("---")
else:
    # رسالة تظهر عندما يكون السيت فارغاً
    st.info("👋 Welcome! Please upload an Excel file from the Sidebar to see products.")
    st.image("https://via.placeholder.com/1000x400?text=Waiting+for+Inventory+Upload...", use_container_width=True)
