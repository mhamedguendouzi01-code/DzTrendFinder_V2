import streamlit as st
import sqlite3
from datetime import datetime

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="Global Trend Finder", layout="wide", page_icon="🌍")

# 2. كود توثيق Pinterest (باش يتنحى الخطأ الأحمر)
st.markdown('<head><meta name="p:domain_verify" content="5de1caac797abccd2cd0b92e1cc47217"/></head>', unsafe_allow_html=True)

# 3. دالة إعداد قاعدة البيانات (نسخة التنظيف النهائي)
def init_db():
    conn = sqlite3.connect('dz_finder.db', check_same_thread=False)
    # السطر اللي تحت يمسح الجداول القديمة المعطوبة لضمان عمل السيت 100%
    conn.execute("DROP TABLE IF EXISTS products") 
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

# تشغيل التهيئة عند كل تحديث
init_db()

# 4. واجهة العرض الرئيسية
st.title("🌍 Global Trend Finder")
st.markdown("### Viral Gadgets & Best AliExpress Deals")
st.divider()

products = get_products()

if not products:
    st.info("👋 الموقع جاهز الآن! أضف أول سلعة من القائمة الجانبية لتظهر هنا.")
else:
    cols = st.columns(3)
    for i, row in enumerate(products):
        with cols[i % 3]:
            # عرض الصورة بطريقة احترافية
            st.image(row['image_url'], use_container_width=True)
            st.subheader(row['title'])
            st.markdown(f"## ${row['promo_price']}")
            
            # رابط الأفلييت المباشر
            link = row['affiliate_link'] if row['affiliate_link'] else "https://s.click.aliexpress.com"
            st.link_button("🎁 View Deal on AliExpress", link, use_container_width=True)
            st.write("---")

# 5. لوحة التحكم (Sidebar)
with st.sidebar:
    st.header("🔐 Admin Access")
    pwd = st.text_input("Password", type="password")
    
    if pwd == "dz2026":
        st.success("Welcome Back!")
        st.divider()
        with st.form("add_product_form", clear_on_submit=True):
            t = st.text_input("Product Name")
            p = st.number_input("Price ($)", min_value=0.01, step=0.01)
            img = st.text_input("Image Link (URL)")
            aff = st.text_input("Affiliate Link")
            submit = st.form_submit_button("Publish Now")
            
            if submit:
                if t and img:
                    try:
                        conn = sqlite3.connect('dz_finder.db', check_same_thread=False)
                        query = "INSERT INTO products (title, promo_price, image_url, affiliate_link, added_at) VALUES (?, ?, ?, ?, ?)"
                        conn.execute(query, (t, p, img, aff, datetime.now()))
                        conn.commit()
                        conn.close()
                        st.success("✅ تم النشر بنجاح! السيت يتحدث الآن...")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error saving: {e}")
                else:
                    st.warning("Please enter at least the Name and Image Link.")
    else:
        st.info("ادخل كلمة السر لإدارة السلع.")