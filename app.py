import streamlit as st
import sqlite3

# 1. إعدادات الصفحة (Design)
st.set_page_config(page_title="DzTrendFinder", layout="wide", page_icon="🇩🇿")

# إضافة CSS مخصص لتحسين مظهر الصور
st.markdown("""
    <style>
    [data-testid="stImage"] img {
        border-radius: 10px;
        object-fit: contain;
        background-color: #f9f9f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🇩🇿 DzTrendFinder Dashboard")
st.write("مرحباً بك! هنا تجد آخر المنتجات التي تم جمعها.")

# 2. دالة جلب البيانات من قاعدة البيانات
def get_products():
    try:
        # تأكد أن ملف dz_finder.db موجود في نفس المجلد
        conn = sqlite3.connect('dz_finder.db')
        cursor = conn.cursor()
        # جلب كل البيانات من جدول products
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
        conn.close()
        return products
    except Exception as e:
        st.error(f"خطأ في قاعدة البيانات: {e}")
        return []

# 3. عرض البيانات
products = get_products()

if not products:
    st.info("ℹ️ لا توجد بيانات حالياً. شغل سكريبت scraper.PY أولاً لجلب المنتجات.")
else:
    # تقسيم الصفحة إلى 3 أعمدة
    cols = st.columns(3)
    
    for i, row in enumerate(products):
        with cols[i % 3]:
            # توزيع البيانات حسب ترتيب الأعمدة في قاعدة البيانات
            # الترتيب المتوقع: العنوان، السعر، رابط الصورة، رابط المنتج، المنصة
            title = row[0] if len(row) > 0 else "بدون عنوان"
            price = row[1] if len(row) > 1 else "غير محدد"
            img_url = row[2] if len(row) > 2 else ""
            link_url = row[3] if len(row) > 3 else "#"
            platform = row[4] if len(row) > 4 else "Unknown"
            
            # عرض الصورة مع رابط بديل إذا كانت الصورة خاسرة
            if img_url and str(img_url).startswith('http'):
                st.image(img_url, use_container_width=True)
            else:
                st.image("https://via.placeholder.com/300x300?text=No+Image", use_container_width=True)
            
            # عرض تفاصيل المنتج
            st.caption(f"Platform: {platform}")
            st.subheader(title)
            st.write(f"💰 **السعر:** {price}")
            
            if link_url != "#":
                st.link_button("🌐 عرض المنتج في المتجر", link_url)
            
            st.markdown("---")

# 4. تذييل الصفحة
st.markdown("<p style='text-align: center; color: gray;'>DzTrendFinder V2.0</p>", unsafe_allow_html=True)