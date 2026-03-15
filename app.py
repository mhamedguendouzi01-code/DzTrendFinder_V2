import streamlit as st
import sqlite3
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="Global Trend Finder", layout="wide", page_icon="🌍")

# 2. كود توثيق Pinterest
st.markdown('<head><meta name="p:domain_verify" content="5de1caac797abccd2cd0b92e1cc47217"/></head>', unsafe_allow_html=True)

# 3. إعداد قاعدة البيانات (تنبيه: هذا الكود سيمسح السلع القديمة المعطوبة)
def init_db():
    conn = sqlite3.connect('dz_finder.db', check_same_thread=False)
    # هاد السطر هو "المفتاح": يمسح الجدول القديم اللي فيه خلل
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

# تشغيل التهيئة عند كل تحديث للكود
init_db()

# 4. واجهة العرض
st.title("🌍 Global Trend Finder")
products = get_products()

if not products:
    st.info("👋 الموقع جاهز! أضف أول سلعة من القائمة الجانبية.")
else:
    cols = st.columns(3)
    for i, row in enumerate(products):
        with cols[i % 3]:
            # عرض الصورة
            if row['image_url']:
                st.image(row['image_url'], use_container_width=True)
            
            st.subheader(row['title'])
            st.write(f"### ${row['promo_price']}")
            
            # زر الشراء (تم إصلاح الخلل هنا)
            aff_link = row['affiliate_link'] if row['affiliate_link'] else "https://s.click.aliexpress.com"
            st.link_button("🎁 Buy on AliExpress", aff_link, use_container_width=True)

# 5. لوحة التحكم
with st.sidebar:
    st.header("🔐 Admin Access")
    pwd = st.text_input("Password", type="password")
    
    if pwd == "dz2026":
        st.success("Welcome Back!")
        with st.form("add_form", clear_on_submit=True):
            t = st.text_input("Product Name")
            p = st.number_input("Price ($)", min_value=0.01, step=0.01)
            img = st.text_input("Image URL")
            aff = st.text_input("Affiliate Link")
            submit = st.form_submit_button("Publish Now")
            
            if submit:
                if t and img:
                    try:
                        conn = sqlite3.connect('dz_finder.db', check_same_thread=False)
                        conn.execute("INSERT INTO products (title, promo_price, image_url, affiliate_link, added_at) VALUES (?, ?, ?, ?, ?)",
                                     (t, p, img, aff, datetime.now()))
                        conn.commit()
                        conn.close()
                        st.success("✅ تم بنجاح! السلعة الآن مباشرة على الموقع.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"خطأ في الحفظ: {e}")
                else:
                    st.warning("يرجى إدخال الاسم ورابط الصورة!")