import streamlit as st
import sqlite3
from datetime import datetime
import os

# 1. إعدادات الصفحة (لازم تكون هي الأولى)
st.set_page_config(
    page_title="Global Trend Finder | Premium Deals",
    layout="wide",
    page_icon="🌍"
)

# 2. كود توثيق Pinterest
st.markdown(
    """
    <head>
    <meta name="p:domain_verify" content="5de1caac797abccd2cd0b92e1cc47217"/>
    </head>
    """,
    unsafe_allow_html=True
)

# 3. تصميم CSS احترافي
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .product-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        text-align: center;
    }
    .price-tag {
        color: #e63946;
        font-size: 24px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. إدارة قاعدة البيانات
def init_db():
    conn = sqlite3.connect('dz_finder.db', check_same_thread=False)
    # ملاحظة: إذا حبيت تمسح السلع القديمة وتبدأ من جديد، نحي الهاش (#) من السطر اللي تحت ودير Push
    # conn.execute("DROP TABLE IF EXISTS products")
    conn.execute('''CREATE TABLE IF NOT EXISTS products 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT, promo_price REAL, image_url TEXT, affiliate_link TEXT, added_at DATETIME)''')
    conn.commit()
    conn.close()

def get_products():
    conn = sqlite3.connect('dz_finder.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        res = conn.execute("SELECT * FROM products ORDER BY added_at DESC").fetchall()
    except:
        res = []
    conn.close()
    return res

init_db()

# 5. واجهة العرض الرئيسية
st.title("🌍 Global Trend Finder")
st.write("### Discover the most viral gadgets at the best prices!")
st.divider()

products = get_products()

if not products:
    st.info("👋 Welcome! Use the sidebar to add your first viral product.")
else:
    cols = st.columns(3)
    for i, row in enumerate(products):
        with cols[i % 3]:
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            st.image(row['image_url'], use_container_width=True)
            st.subheader(row['title'])
            st.markdown(f'<p class="price-tag">${row["promo_price"]:.2f}</p>', unsafe_allow_html=True)
            
            aff_link = row['affiliate_link'] if row['affiliate_link'] else "https://s.click.aliexpress.com"
            st.link_button("🎁 Get Deal on AliExpress", aff_link, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# 6. لوحة التحكم (Sidebar) - النسخة المصححة 100%
with st.sidebar:
    st.header("🔐 Admin Panel")
    password = st.text_input("Admin Password", type="password")
    
    if password == "dz2026":
        st.success("Access Granted!")
        st.divider()
        st.subheader("➕ Add New Product")
        
        # استمارة الإضافة مع مسح الخانات بعد الإرسال
        with st.form("add_product_form", clear_on_submit=True):
            new_title = st.text_input("Product Name")
            new_price = st.number_input("Price ($)", min_value=0.01, step=0.01)
            new_img = st.text_input("Image Link (URL)")
            new_aff = st.text_input("Affiliate Link")
            
            submit_button = st.form_submit_button("Publish to Website")
            
            if submit_button:
                if new_title and new_img:
                    try:
                        conn = sqlite3.connect('dz_finder.db', check_same_thread=False)
                        conn.execute("INSERT INTO products (title, promo_price, image_url, affiliate_link, added_at) VALUES (?, ?,