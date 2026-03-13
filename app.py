import streamlit as st
import sqlite3

# إعدادات الصفحة
st.set_page_config(page_title="DzTrendFinder", layout="wide")

st.title("🇩🇿 DzTrendFinder - Dashboard")

# دالة لجلب البيانات
def get_products():
    conn = sqlite3.connect('dz_finder.db')
    conn.row_factory = sqlite3.Row
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return products

products = get_products()

# عرض المنتجات في مربعات (Grid)
cols = st.columns(3) # يعرض 3 منتجات في السطر

for i, product in enumerate(products):
    with cols[i % 3]:
        st.image(product['image_url'], use_container_width=True)
        st.subheader(product['title'])
        st.write(f"**Prix:** ${product['price']}")
        st.write(f"**Plateforme:** {product['platform']}")
        st.link_button("Voir le produit", product['url'])
        st.markdown("---")