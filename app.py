import streamlit as st
import sqlite3
import urllib.parse

# إعدادات الصفحة
st.set_page_config(page_title="DzTrend Finder | AliExpress", layout="wide", page_icon="🛍️")

# ستايل احترافي
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stCard { border-radius: 15px; background-color: white; padding: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .price-tag { color: #FF4B4B; font-size: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- معلوماتك الشخصية (بدل الرقم برقمك) ---
MY_WHATSAPP = "213600000000" 

st.title("🛍️ DzTrend Finder")
st.subheader("وسيطك الموثوق للشراء من AliExpress في الجزائر")
st.info("اختر المنتج الذي أعجبك، وسنقوم بشرائه وشحنه لك حتى باب منزلك!")

def load_data():
    try:
        conn = sqlite3.connect('dz_finder.db')
        conn.row_factory = sqlite3.Row
        products = conn.execute('SELECT * FROM products').fetchall()
        conn.close()
        return products
    except:
        return []

products = load_data()

if not products:
    st.warning("🔄 جاري تحديث قائمة السلع... يرجى إعادة المحاولة.")
else:
    cols = st.columns(3)
    for i, row in enumerate(products):
        with cols[i % 3]:
            with st.container(border=True):
                if row['image_url']:
                    st.image(row['image_url'], use_container_width=True)
                
                st.subheader(row['title'])
                st.markdown(f"<p class='price-tag'>{row['price']}</p>", unsafe_allow_html=True)
                
                # رسالة الواتساب
                message = f"سلام محمد، حاب نطلب هاد المنتج:\n{row['title']}\nالسعر: {row['price']}\nالرابط: {row['url']}"
                wa_url = f"https://wa.me/{MY_WHATSAPP}?text={urllib.parse.quote(message)}"
                
                st.link_button("🚀 اطلبها لي الآن", wa_url, type="primary")
                st.caption(f"المصدر: {row['platform']} | التوصيل: 58 ولاية")

st.divider()
st.markdown("<p style='text-align: center;'>© 2026 DzTrend Finder - خدمة الوساطة التجارية</p>", unsafe_allow_html=True)