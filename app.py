import streamlit as st
import sqlite3
import urllib.parse

# إعداد الصفحة
st.set_page_config(page_title="DzTrend Intelligence", layout="wide", page_icon="🛍️")

# ستايل CSS (تم تحديثه لضمان ظهور الصور بوضوح)
st.markdown("""
    <style>
    [data-testid="stHorizontalBlock"] { gap: 10px !important; }
    .product-card {
        border: 1px solid #eee;
        border-radius: 12px;
        padding: 10px;
        text-align: center;
        background: white;
        min-height: 300px;
    }
    /* إجبار الصور على التناسب مع حجم العمود */
    .product-card img {
        max-width: 100%;
        height: auto;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .title { font-size: 13px; font-weight: bold; color: #333; height: 40px; overflow: hidden; }
    .price { color: #2ecc71; font-size: 16px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- معلوماتك ---
MY_WHATSAPP = "213600000000" 

def load_data():
    try:
        conn = sqlite3.connect('dz_finder.db')
        conn.row_factory = sqlite3.Row
        products = conn.execute('SELECT * FROM products ORDER BY added_at DESC').fetchall()
        conn.close()
        return products
    except:
        return []

# --- الواجهة ---
st.title("🚀 DzTrend Intelligence Portal")

with st.sidebar:
    st.subheader("🔍 البحث بالصورة (Source)")
    st.file_uploader("ارفع صورة للبحث في AliExpress", type=['jpg', 'png', 'jpeg'])
    st.divider()
    st.info("الصور يتم جلبها مباشرة من السورس.")

products = load_data()

if not products:
    st.warning("⚠️ لم يتم العثور على سلع. يرجى تشغيل scraper.PY أولاً.")
else:
    # استخدام 6 أعمدة
    cols = st.columns(6)
    
    for i, row in enumerate(products):
        with cols[i % 6]:
            with st.container(border=True):
                # --- حل مشكلة الصور ---
                # نستخدم try/except أو رابط احتياطي في حالة فشل الرابط الأصلي
                img_url = row['image_url'] if row['image_url'] else "https://via.placeholder.com/150"
                
                # استخدام st.image مع تعطيل الكاش إذا لزم الأمر
                st.image(img_url, use_container_width=True, output_format="JPEG")
                
                st.markdown(f"<div class='title'>{row['title']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='price'>{row['promo_price']} DA</div>", unsafe_allow_html=True)
                
                # زر الواتساب
                msg = f"سلام محمد، حاب نطلب هاد المنتج:\n{row['title']}\nالسعر: {row['promo_price']} DA"
                wa_url = f"https://wa.me/{MY_WHATSAPP}?text={urllib.parse.quote(msg)}"
                st.link_button("🚀 اطلب الآن", wa_url)