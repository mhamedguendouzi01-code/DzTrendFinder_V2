import streamlit as st
import sqlite3
import urllib.parse

st.set_page_config(page_title="DzTrend Intelligence", layout="wide")

st.markdown("""
    <style>
    [data-testid="stHorizontalBlock"] { gap: 10px !important; }
    .product-card {
        border: 1px solid #eee; border-radius: 10px; padding: 10px;
        background: white; text-align: center; min-height: 280px;
    }
    .img-container { width: 100%; height: 130px; overflow: hidden; border-radius: 8px; margin-bottom: 10px; }
    .img-container img { width: 100%; height: 100%; object-fit: contain; }
    .title { font-size: 12px; font-weight: bold; color: #333; height: 35px; overflow: hidden; margin: 5px 0; }
    .price { color: #FF4B4B; font-weight: bold; font-size: 16px; }
    </style>
    """, unsafe_allow_html=True)

def load_products():
    conn = sqlite3.connect('dz_finder.db')
    conn.row_factory = sqlite3.Row
    data = conn.execute('SELECT * FROM products ORDER BY price ASC').fetchall()
    conn.close()
    return data

st.title("🚀 DzTrend Intelligence (Under 2000 DA)")

with st.sidebar:
    st.header("🔍 بحث بالصورة (Source)")
    st.file_uploader("ارفع صورة للبحث في AliExpress", type=['jpg', 'png'])

products = load_products()

if not products:
    st.warning("⚠️ لا توجد سلع تحت 2000 دج.")
else:
    cols = st.columns(6)
    for i, row in enumerate(products):
        with cols[i % 6]:
            with st.container(border=True):
                # الحل النهائي للصور: عرضها عبر HTML لتفادي بلوك Streamlit
                st.markdown(f'''
                    <div class="product-card">
                        <div class="img-container">
                            <img src="{row['image_url']}" onerror="this.src='https://via.placeholder.com/150?text=Image+Error'">
                        </div>
                        <div class="title">{row['title']}</div>
                        <div class="price">{row['price']} DA</div>
                    </div>
                ''', unsafe_allow_html=True)
                
                # زر الواتساب
                msg = f"سلام محمد، حاب نطلب هاد المنتج (برومو < 2000 دج):\n{row['title']}\nالسعر: {row['price']} DA"
                wa_url = f"https://wa.me/213600000000?text={urllib.parse.quote(msg)}"
                st.link_button("🚀 اطلب الآن", wa_url)