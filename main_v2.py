import streamlit as st

# إعداد الصفحة للـ Cloud
st.set_page_config(
    page_title="DzTrendFinder V2",
    page_icon="📈",
    layout="wide"
)

# تصميم الأزرار بستايل AliExpress
st.markdown("""
    <style>
    div.stButton > button {
        background-color: #FF4747;
        color: white;
        border-radius: 10px;
        height: 3.5em;
        width: 100%;
        font-weight: bold;
        border: none;
        font-size: 18px;
    }
    div.stButton > button:hover {
        background-color: #D32F2F;
        border: 1px solid white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 DzTrendFinder V2 - لوحة التحكم الذكية")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 إدارة الجملة")
    st.write("تحليل الموردين وتكاليف الاستيراد من Alibaba")
    if st.button("فتح قسم الجملة 🏭"):
        try:
            st.switch_page("pages/1_Wholesale.py")
        except Exception as e:
            st.error(f"خطأ في المسار: تأكد من وجود الملف في pages/1_Wholesale.py")

with col2:
    st.subheader("🛍️ تحليل التجزئة")
    st.write("مراقبة AliExpress, Amazon, Temu")
    if st.button("فتح قسم التجزئة 🛒"):
        try:
            st.switch_page("pages/2_Retail.py")
        except Exception as e:
            st.error("خطأ في المسار: تأكد من وجود الملف في pages/2_Retail.py")

st.sidebar.success("تم تسجيل الدخول بصفتك: Admin (ADV)")
