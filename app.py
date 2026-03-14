import streamlit as st
import sqlite3
import urllib.parse

st.set_page_config(page_title="DzTrend Intelligence", layout="wide")

# ستايل احترافي لـ 6 أعمدة
st.markdown("""
    <style>
    .product-card {
        border: 1px solid #eee; border-radius: 10px; padding: 10px;
        background: white; text-align: center; min-height: 320px;
    }
    .title { font-size: 12px; font-weight: bold; color: #333; height: 35px; overflow: hidden; margin: 10px 0; }
    .price { color: #2ecc71; font-weight: bold; font-size: 15px; }
    .discount { background: #ff4b4b; color: white; padding: 2px 5px; border-radius: 5px; font-size: 10px; }
    </style>
    """, unsafe_allow_html=True)

def load_products():
    conn = sqlite3.connect('dz_finder.db')
    conn.row_factory = sqlite3.Row
    data = conn.execute('SELECT * FROM products ORDER BY added_at DESC').fetchall()
    conn.close()
    return data

st.title("🚀 DzTrend Intelligence")

# القائمة الجانبية للبحث بالصورة في السورس
with st.sidebar:
    st.header("🔍 بحث بالصورة (Source)")
    st.file_uploader("ارفع صورة للبحث في AliExpress", type=['jpg', 'png', 'jpeg'])

products = load_products()

if not products:
    st.warning("⚠️ لا توجد سلع. شغل scraper.PY")
else:
    cols = st.columns(6) # هنا درنا الـ 6 أعمدة
    for i, row in enumerate(products):
        with cols[i % 6]:
            with st.container(border=True):
                # عرض الصورة بطريقة تضمن الظهور
                st.image(row['image_url'], use_container_width=True)
                
                st.markdown(f"<div class='discount'>-{row['discount_percent']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='title'>{row['title']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='price'>{row['promo_price']} DA</div>", unsafe_allow_html=True)
                
                # زر الواتساب
                msg = f"سلام محمد، حاب نطلب هاد المنتج:\n{row['title']}\nالسعر: {row['promo_price']} DA"
                wa_url = f"https://wa.me/213600000000?text={urllib.parse.quote(msg)}"
                st.link_button("🚀 اطلب الآن", wa_url)