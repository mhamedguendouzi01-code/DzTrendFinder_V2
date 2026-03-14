import streamlit as st
import sqlite3
from datetime import datetime, timedelta

# إعداد الصفحة لتكون واسعة جداً وتناسب 10 أعمدة
st.set_page_config(page_title="DzTrend Intelligence", layout="wide", page_icon="📈")

# ستايل CSS متطور للتحكم في الأعمدة وشكل السلعة
st.markdown("""
    <style>
    /* تصغير الفراغات بين الأعمدة */
    [data-testid="stHorizontalBlock"] { gap: 5px !important; }
    
    /* ستايل كرت المنتج */
    .product-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 8px;
        text-align: center;
        background-color: white;
        transition: transform 0.2s;
        min-height: 250px;
    }
    .product-card:hover { transform: scale(1.02); border-color: #FF4B4B; }
    .title { font-size: 11px; font-weight: bold; height: 35px; overflow: hidden; margin: 5px 0; }
    .old-price { color: #999; text-decoration: line-through; font-size: 10px; }
    .new-price { color: #2ecc71; font-weight: bold; font-size: 13px; }
    .discount-badge { background: #FF4B4B; color: white; border-radius: 5px; padding: 2px 5px; font-size: 10px; position: absolute; }
    </style>
    """, unsafe_allow_html=True)

# --- وظائف قاعدة البيانات ---
def get_all_products():
    conn = sqlite3.connect('dz_finder.db')
    conn.row_factory = sqlite3.Row
    res = conn.execute('SELECT * FROM products ORDER BY added_at DESC').fetchall()
    conn.close()
    return res

# --- واجهة المستخدم ---

# 1. القائمة الجانبية (Sidebar)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1162/1162456.png", width=80)
    st.title("لوحة التحكم")
    
    # البحث بالصورة
    st.subheader("🔍 بحث بالصورة")
    img_file = st.file_uploader("ارفع صورة المنتج", type=['jpg', 'png', 'jpeg'])
    if img_file:
        st.info("جاري تحليل الصورة والبحث عن برومو...")

    st.divider()
    
    # نظام التسجيل
    st.subheader("📩 اشتراك التنبيهات")
    email = st.text_input("بريدك الإلكتروني")
    if st.button("تفعيل التنبيهات"):
        st.success("تم التسجيل! ستحصل على الهمزات فور صدورها.")

# 2. المحتوى الرئيسي
st.title("🚀 DzTrend Intelligence")
st.markdown("### أقوى التخفيضات والبروموات الحالية (تحديث لحظي)")

products = get_all_products()

if not products:
    st.warning("لا توجد منتجات حالياً. شغل scraper.PY أولاً.")
else:
    # إنشاء 10 أعمدة
    cols = st.columns(10)
    
    for i, row in enumerate(products):
        # نوزع المنتجات على الـ 10 أعمدة بالتناوب
        with cols[i % 10]:
            # عرض الكرت
            st.markdown(f"""
                <div class="product-card">
                    <span class="discount-badge">-{row['discount_percent']}</span>
                    <img src="{row['image_url']}" style="width:100%; border-radius:5px;">
                    <div class="title">{row['title']}</div>
                    <div class="old-price">{row['original_price']} DA</div>
                    <div class="new-price">{row['promo_price']} DA</div>
                </div>
            """, unsafe_allow_html=True)
            
            # زر الحجز (نظام 24 ساعة)
            if st.button(f"حجز 🛒", key=f"btn_{row['id']}"):
                st.toast(f"تم حجز {row['title']} لمدة 24 ساعة باسمك!", icon="✅")

# 3. تذييل الصفحة
st.divider()
st.caption("نظام ذكي لمراقبة الأسعار - جميع الحقوق محفوظة لـ DzTrend 2026")