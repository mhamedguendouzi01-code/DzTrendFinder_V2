import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="DzTrend V2", layout="wide")

# تصميم الأزرار (CSS) لتشبه AliExpress
st.markdown("""
    <style>
    div.stButton > button {
        background-color: #FF4747;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-weight: bold;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #D32F2F;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 DzTrendFinder V2 - لوحة التحكم")
st.write("مرحباً بك! اختر القسم الذي تريد العمل عليه:")

# توزيع الأزرار في أعمدة لتكون منظمة
col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 سوق الجملة")
    st.write("إدارة الموردين وحساب التكاليف من Alibaba")
    if st.button("الانتقال إلى الجملة 🏭"):
        # ملاحظة: يجب أن يكون الملف موجوداً في مجلد pages بهذا الاسم تماماً
        st.switch_page("pages/1_Wholesale.py")

with col2:
    st.subheader("🛍️ سوق التجزئة")
    st.write("مراقبة AliExpress, Temu و Amazon")
    if st.button("الانتقال إلى التجزئة 🛒"):
        st.switch_page("pages/2_Retail.py")

st.divider()
st.info("نصيحة: يمكنك دائماً استخدام القائمة الجانبية للتنقل السريع.")
