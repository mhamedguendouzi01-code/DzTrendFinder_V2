import streamlit as st
import sqlite3

st.set_page_config(page_title="DzTrendFinder", layout="wide")
st.title("🇩🇿 DzTrendFinder Dashboard")

def get_products():
    try:
        conn = sqlite3.connect('dz_finder.db')
        # هاد السطر يخلينا نجبدو البيانات بالاسم ماشي بالرقم
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
        conn.close()
        return products
    except Exception as e:
        st.error(f"خطأ: {e}")
        return []

products = get_products()

if not products:
    st.warning("⚠️ قاعدة البيانات فارغة أو غير موجودة. تأكد من تشغيل scraper.PY أولاً!")
else:
    cols = st.columns(3)
    for i, row in enumerate(products):
        with cols[i % 3]:
            # هنا نجبدو بالاسم، هكذا حتى لو تبدل الترتيب ما يصرى والو
            title = row['title'] if 'title' in row.keys() else "بدون عنوان"
            price = row['price'] if 'price' in row.keys() else "0.00"
            img   = row['image_url'] if 'image_url' in row.keys() else ""
            url   = row['url'] if 'url' in row.keys() else "#"

            if img and str(img).startswith('http'):
                st.image(img, use_container_width=True)
            else:
                st.image("https://via.placeholder.com/300?text=No+Image", use_container_width=True)
            
            st.subheader(title)
            st.write(f"💰 **السعر:** {price}")
            if url != "#":
                st.link_button("View Product", url)
            st.markdown("---")