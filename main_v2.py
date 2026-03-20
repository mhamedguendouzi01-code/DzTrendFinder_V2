import streamlit as st
import pandas as pd

# 1. إعداد الصفحة (يجب أن يكون أول أمر Streamlit)
st.set_page_config(
    page_title="Global AI Deals Hub", 
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. تصميم القائمة الجانبية (Menu) المستوحى من AliExpress
st.sidebar.markdown("""
    <style>
        .css-1d391kg {  /* تعديل لون القائمة الجانبية في بعض الثيمات */
            background-color: #f5f5f5;
        }
        .aliexpress-menu-header {
            font-size: 24px;
            font-weight: bold;
            color: #FF4747; /* لون أحمر AliExpress */
            text-align: center;
            padding: 10px 0;
            border-bottom: 2px solid #FF4747;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# رأس القائمة الجانبية
st.sidebar.markdown('<div class="aliexpress-menu-header">GLOBAL AI HUB</div>', unsafe_allow_html=True)

# إضافة عناصر إضافية للقائمة الجانبية (غير الصفحات التلقائية)
st.sidebar.subheader("🌍 التنقل السريع")
st.sidebar.info("استخدم القائمة أعلاه للانتقال بين أسواق الجملة والتجزئة.")

st.sidebar.divider()
st.sidebar.subheader("👤 حسابي")
st.sidebar.button("لوحة التحكم (Dashboard)")
st.sidebar.button("الإعدادات")

# --- محتوى الصفحة الرئيسية ---
st.title("Welcome to Global AI Deals Hub")
st.markdown("""
### منصتك الذكية لإدارة الصفقات بين أسواق الجملة والتجزئة.

👈 **اختر من القائمة الجانبية:**
* **Wholesale (علي بابا):** للبحث عن الموردين وإدارة المخزون بالجملة.
* **Retail (علي إكسبريس، تيمو، أمازون):** لمراقبة أسعار التجزئة وتنسيق الصفقات الذكية.
""")

# يمكنك إضافة الـ Dashboard الرئيسي هنا مستقبلاً
