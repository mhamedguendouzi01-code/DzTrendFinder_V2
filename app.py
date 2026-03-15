import streamlit as st
import sqlite3
from datetime import datetime

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="Global Trend Finder | Premium Deals",
    layout="wide",
    page_icon="🌍"
)

# 2. كود توثيق Pinterest (المهم جداً لربط حسابك)
st.markdown(
    """
    <head>
    <meta name="p:domain_verify" content="5de1caac797abccd2cd0b92e1cc47217"/>
    </head>
    """,
    unsafe_allow_html=True
)

# 3. تصميم CSS احترافي واجهة عالمية (Global Look)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stApp { max-width: 1200px; margin: 0 auto; }
    .product-card {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 25px;
        text-align: center;
        border: 1px solid #eee;
    }
    .product-image {
        width: 100%;
        height: 200px;
        object-fit: contain;
        border-radius: 8px;
    }
    .price-tag {
        color: #eb4d4b;
        font-size: 22px;
        font-weight: bold;
        margin: 10px 0;
    }
    .product-title {
        font-size: 16px;
        height: 50px;
        overflow: hidden;
        color: #2d3436;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. إعداد قاعدة البيانات (مصححة لتمحي الأخطاء السابقة)
def init_db():
    conn = sqlite3.connect('dz_finder.db')
    # ملاحظة: إذا حبيت تمسح كل السلع القديمة وتبدأ من جديد، نحي الهاش (#) من السطر اللي تحت
    # conn.execute("DROP TABLE IF EXISTS products") 
    conn.execute('''CREATE TABLE IF NOT EXISTS products 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT, promo_price REAL, image_url TEXT, affiliate_link TEXT, added_at DATETIME)''')
    conn.close()

def get_products():
    conn = sqlite3.connect('dz_finder.db')
    conn.row_factory = sqlite3.Row
    try:
        res = conn.execute("SELECT * FROM products ORDER BY added_at DESC").fetchall()
    except:
        res = []
    conn.close()
    return res

init_db()

# 5. واجهة الموقع الرئيسية
st.title("🌍 Global Trend Finder")
st.markdown("### Hand-Picked Viral Gadgets & Premium Deals")
st.divider()

products = get_products()

if not products:
    st.info("👋 Welcome! Start by adding products from the Admin Panel in the sidebar.")
else:
    cols = st.columns(3)
    for i, row in enumerate(products):
        with cols[i % 3]:
            st.markdown(f'''
                <div class="product-card">
                    <img src="{row['image_url']}" class="product-image">
                    <div class="product-title">{row['title']}</div>
                    <div class="price-tag">${row['promo_price']:.2f}</div>
                </div>
            ''', unsafe_allow_html=True)
            # زر الشراء مع حماية من الأخطاء
            aff_link = row['affiliate_link'] if 'affiliate_link' in row.keys() and row['affiliate_link'] else "https://s.click.aliexpress.com"
            st.link_button("🎁 Get Deal on AliExpress", aff_link, use_container_width=True)

# 6. لوحة التحكم الجانبية (Admin Panel)
with st.sidebar:
    st.header("🔐 Admin Access")
    pwd = st.text_input("Admin Password", type="password")
    
    if pwd == "dz2026":
        st.success("Log in Successful!")
        st.divider()
        st.subheader("➕ Add New Product")
        
        with st.form("add_product_form"):
            new_title = st.text_input("Product Name (English)")
            new_price = st.number_input("Price in USD ($)", min_value=0.01, step=0.01)
            new_img = st.text_input("Image Link (Direct URL)")
            new_aff = st.text_input("Your Affiliate Link")
            
            submitted = st.form_submit_button("Publish Product")
            
            if submitted and new_title and new_img:
                conn = sqlite3.connect('dz_finder.db')
                conn.execute("INSERT INTO products (title, promo_price, image_url, affiliate_link, added_at) VALUES (?, ?, ?, ?, ?)",
                             (new_title, new_price, new_img, new_aff, datetime.now()))
                conn.commit()
                conn.close()
                st.toast("Product added successfully!")
                st.rerun()
    else:
        st.warning("Enter password to add products.")

    st.divider()
    st.caption("Global Trend Finder v4.1 | 2026")