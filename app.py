import streamlit as st
import sqlite3
import urllib.parse

# إعدادات الصفحة
st.set_page_config(page_title="DzTrend Finder | AliExpress", layout="wide", page_icon="🛍️")

# ستايل CSS لتحسين المظهر
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #FF4B4B; color: white; height: 3em; font-weight: bold; }
    .stCard { border: 1px solid #eee; padding: 15px; border-radius: 15px; background: white; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    .price { color: #FF4B4B; font-size: 22px; font-weight: bold; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- معلوماتك (تأكد من وضع رقمك هنا) ---
MY_WHATSAPP = "213600000000" 

st.title("🛍️ DzTrend Finder")
st.subheader("في الجزائر AliExpress وسيطك الموثوق للشراء من")
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
    st.warning("🔄 جاري تحديث العروض... يرجى الانتظار.")
else:
    cols = st.columns(3)
    for i, row in enumerate(products):
        with cols[i % 3]:
            with st.container(border=True):
                # عرض الصورة مع رابط بديل إذا فشلت
                img = row['image_url'] if row['image_url'] else "https://via.placeholder.com/300"
                st.image(img, use_container_width=True)
                
                st.subheader(row['title'])
                st.markdown(f"<p class='price'>{row['price']}</p>", unsafe_allow_html=True)
                
                # رسالة واتساب
                msg = f"سلام محمد، حاب نطلب هاد المنتج:\n{row['title']}\nالسعر: {row['price']}\nالرابط: {row['url']}"
                wa_url = f"https://wa.me/{MY_WHATSAPP}?text={urllib.parse.quote(msg)}"
                
                st.link_button("🚀 اطلبها لي الآن", wa_url)
                st.caption(f"🚚 التوصيل: 58 ولاية | المصدر: {row['platform']}")

st.divider()
st.markdown("<p style='text-align: center;'>© 2026 DzTrend Finder - خدمة الوساطة التجارية</p>", unsafe_allow_html=True)