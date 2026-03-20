import streamlit as st

# إعداد الصفحة الرئيسية للنسخة V2
st.set_page_config(
    page_title="DzTrendFinder V2",
    page_icon="📈",
    layout="wide"
)

# تصميم القائمة الجانبية (Sidebar) بلمسة AliExpress
st.sidebar.markdown("""
    <div style="background-color: #FF4747; padding: 15px; border-radius: 10px; text-align: center;">
        <h2 style="color: white; margin: 0;">DzTrend V2</h2>
        <p style="color: white; font-size: 12px;">Smart Sourcing Hub</p>
    </div>
    <br>
""", unsafe_allow_html=True)

st.sidebar.title("📌 القائمة الرئيسية")
st.sidebar.info("اختر القسم المطلوب من الأعلى للتنقل بين الجملة والتجزئة.")

# محتوى الصفحة الرئيسية (Dashboard)
st.title("🚀 مرحباً بك في DzTrendFinder V2")
st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="إجمالي المنتجات المراقبة", value="1,240", delta="12%+")
with col2:
    st.metric(label="أفضل مورد (Alibaba)", value="Shenzhen Tech", delta="Verified")
with col3:
    st.metric(label="أعلى ربح متاح", value="5,200 DA", delta="Hot Deal")

st.divider()
st.subheader("📝 ملاحظات المدير (ADV Notes)")
st.text_area("أضف ملاحظاتك حول حالة السوق اليوم:", placeholder="مثال: ارتفاع أسعار الشحن من علي بابا...")

st.success("المنصة جاهزة للعمل. ابدأ برفع بياناتك من الأقسام الجانبية.")
