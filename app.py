import streamlit as st
import sqlite3
import urllib.parse
import time
from datetime import datetime, timedelta

# إعداد الصفحة لتكون واسعة وتناسب 6 أعمدة (تبان السلعة مليح)
st.set_page_config(page_title="DzTrend Intelligence", layout="wide", page_icon="🛍️")

# ستايل CSS احترافي (6 أعمدة + شكل الكرت)
st.markdown("""
    <style>
    /* تصغير الفراغات بين الأعمدة */
    [data-testid="stHorizontalBlock"] { gap: 8px !important; }
    
    /* ستايل كرت المنتج */
    .product-card {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 10px;
        text-align: center;
        background-color: white;
        transition: transform 0.2s, box-shadow 0.2s;
        min-height: 280px; /* طول أنسب لـ 6 أعمدة */
    }
    .product-card:hover { transform: scale(1.03); border-color: #3498db; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    .title { font-size: 13px; font-weight: bold; height: 38px; overflow: hidden; margin: 8px 0; color: #2c3e50; }
    .old-price { color: #999; text-decoration: line-through; font-size: 12px; }
    .new-price { color: #2ecc71; font-weight: bold; font-size: 16px; margin-bottom: 5px; }
    .discount-badge { background: #FF4B4B; color: white; border-radius: 5px; padding: 2px 6px; font-size: 11px; position: absolute; }
    .stButton>button { width: 100%; border-radius: 8px; font-size: 14px; font-weight: bold; height: 2.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- معلوماتك الشخصية ---
MY_WHATSAPP = "213600000000" # غير هاد الرقم برقمك الحقيقي

# --- وظائف قاعدة البيانات (المنصة تاعك) ---
def get_all_products():
    try:
        conn = sqlite3.connect('dz_finder.db')
        conn.row_factory = sqlite3.Row
        res = conn.execute('SELECT * FROM products ORDER BY added_at DESC').fetchall()
        conn.close()
        return res
    except:
        return []

# --- محاكاة البحث بالصورة في السورس (AliExpress) ---
# ملاحظة: هاد الوظيفة في المستقبل راح تربطوها بـ API للبحث بالصورة في AliExpress
def simulate_image_search_source(image_file):
    time.sleep(1.5) # محاكاة وقت البحث
    # سلع مقترحة من السورس (AliExpress)
    source_results = [
        ('سلعة مشابهة 1 (source)', '12.50$', 'https://via.placeholder.com/150/2ecc71/ffffff?text=Source1', 'https://aliexpress.com'),
        ('سلعة مشابهة 2 (source)', '8.99$', 'https://via.placeholder.com/150/3498db/ffffff?text=Source2', 'https://aliexpress.com'),
        ('سلعة مشابهة 3 (source)', '22.00$', 'https://via.placeholder.com/150/9b59b6/ffffff?text=Source3', 'https://aliexpress.com'),
    ]
    return source_results

# --- واجهة المستخدم الرئيسية ---

# 1. القائمة الجانبية (Sidebar)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1162/1162456.png", width=70)
    st.title("لوحة التحكم الذكية")
    
    # --- خانة البحث بالصورة ---
    st.subheader("🔍 بحث بالصورة في AliExpress")
    uploaded_file = st.file_uploader("ارفع صورة المنتج", type=['jpg', 'png', 'jpeg'])
    if uploaded_file:
        st.info("جاري تحليل الصورة والبحث عن المنتجات في AliExpress (السورس)...")
        # استدعاء البحث من السورس
        source_products = simulate_image_search_source(uploaded_file)
        
        st.write("### النتائج في السورس:")
        for p in source_products:
            with st.container(border=True):
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(p[2], width=50)
                with col2:
                    st.caption(f"**{p[0]}**")
                    st.caption(f"💰 {p[1]}")
                    # رسالة واتساب
                    message = f"سلام محمد، حاب نطلب هاد المنتج اللي بحثت عليه بالصورة من AliExpress:\n{p[0]}\nالسعر المقدر: {p[1]}\nالرابط: {p[3]}"
                    wa_url = f"https://wa.me/{MY_WHATSAPP}?text={urllib.parse.quote(message)}"
                    st.link_button("🚀 اطلبها لي", wa_url)
    
    st.divider()
    
    # --- نظام التسجيل (Newsletter) ---
    st.subheader("📩 اشتراك التنبيهات")
    email = st.text_input("بريدك الإلكتروني")
    if st.button("تفعيل التنبيهات"):
        st.success("تم التسجيل! ستحصل على الهمزات فور صدورها.")

# 2. المحتوى الرئيسي
st.title("🛍️ DzTrend Intelligence Portal")
st.markdown("### أقوى التخفيضات والهمزات الحالية (منصة وساطة)")

products = get_all_products()

if not products:
    st.warning("🔄 لا توجد منتجات حالياً. تأكد من تشغيل 'scraper.PY' أولاً.")
else:
    # إنشاء 6 أعمدة (العدد الأمثل للوضوح والكمية)
    cols = st.columns(6)
    
    for i, row in enumerate(products):
        # توزيع المنتجات على الـ 6 أعمدة
        with cols[i % 6]:
            with st.container(border=True):
                # عرض الكرت
                st.markdown(f"""
                    <div class="product-card">
                        <span class="discount-badge">-{row['discount_percent']}</span>
                        <img src="{row['image_url']}" style="width:100%; border-radius:10px;">
                        <div class="title">{row['title']}</div>
                        <div class="old-price">{row['original_price']} DA</div>
                        <div class="new-price">{row['promo_price']} DA</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # إعداد رسالة الواتساب (طلب مباشر من المنصة)
                message = f"سلام محمد، حاب نطلب هاد المنتج من DzTrend:\n{row['title']}\nالسعر المقدر: {row['promo_price']} DA\nالرابط: {row['url']}"
                wa_url = f"https://wa.me/{MY_WHATSAPP}?text={urllib.parse.quote(message)}"
                
                # زر الطلب (الهدف تفعيل الحجز بعد 24 ساعة في المستقبل)
                st.link_button("🚀 اطلبها لي", wa_url)

# 3. تذييل الصفحة
st.divider()
st.caption("© 2026 DzTrend Intelligence - جميع الحقوق محفوظة")