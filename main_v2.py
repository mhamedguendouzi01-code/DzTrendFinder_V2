import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الاحترافية (Layout Wide)
st.set_page_config(page_title="Global Deals Hub", page_icon="🌍", layout="wide")

# 2. تصميم CSS عصري (تصغير الصور وتنسيق البطاقات)
st.markdown("""
    <style>
    /* تنسيق الحاوية الكبيرة */
    .main {
        background-color: #f0f2f6;
    }
    /* تنسيق بطاقة المنتج */
    [data-testid="stVerticalBlock"] > div:has(div.stImage) {
        background-color: white;
        border-radius: 15px;
        padding: 15px;
        border: 1px solid #e6e6e6;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    [data-testid="stVerticalBlock"] > div:has(div.stImage):hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    /* تصغير حجم السعر */
    .price-tag {
        color: #1a73e8;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 10px;
    }
    /* تنسيق العناوين */
    .product-title {
        font-weight: 600;
        font-size: 0.9rem;
        height: 40px;
        overflow: hidden;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. لوحة التحكم في الجانب (Sidebar)
with st.sidebar:
    st.title("🔐 Admin Panel")
    pwd = st.text_input("Password", type="password")
    
    if pwd == "dz2026":
        st.success("Access Granted!")
        uploaded_file = st.file_uploader("Upload Excel File", type=['xlsx'])
        if uploaded_file:
            # قراءة الملف وتنظيف أسماء الأعمدة من أي فراغ خفي
            df = pd.read_excel(uploaded_file)
            df.columns = df.columns.str.strip()
            # حفظ البيانات في جلسة العمل
            st.session_state['data'] = df
            st.sidebar.info(f"✅ Loaded {len(df)} Products!")
        
        if st.button("🗑️ Clear All Data"):
            if 'data' in st.session_state:
                del st.session_state['data']
                st.rerun()

# 4. الواجهة الرئيسية
st.title("🌍 Global Deals Hub")
st.write("Discover Viral Gadgets: Amazon, AliExpress & Temu")

# 5. ميزة البحث (Search Bar)
if 'data' in st.session_state:
    search_query = st.text_input("🔍 Search for products...", placeholder="e.g. Smart Watch")
    
    df_display = st.session_state['data']
    
    # فلترة النتائج بناءً على البحث
    if search_query:
        df_display = df_display[df_display['Product Title'].str.contains(search_query, case=False, na=False)]

    st.divider()

    # 6. عرض المنتجات في 4 أعمدة (لتصغير الصور)
    if not df_display.empty:
        cols = st.columns(4) # هنا صغرنا الصور بجعل الأعمدة 4
        
        for index, row in df_display.reset_index().iterrows():
            with cols[index % 4]:
                # استخراج البيانات
                img_url = str(row.get('Image URL', '')).strip()
                title = str(row.get('Product Title', 'No Title'))
                price = row.get('Price', '0.00')
                link = str(row.get('Affiliate Link', '#')).strip()
                platform = str(row.get('Platform', 'Shop Now'))

                # عرض الصورة
                if img_url and img_url != 'nan':
                    st.image(img_url, use_container_width=True)
                else:
                    st.image("https://via.placeholder.com/150?text=No+Image", use_container_width=True)
                
                # عرض النصوص والبوطونة
                st.markdown(f"<div class='product-title'>{title[:50]}...</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='price-tag'>${price}</div>", unsafe_allow_html=True)
                st.caption(f"📍 Platform: {platform}")
                st.link_button("🔥 View Deal", link, use_container_width=True)
                st.write("") # فراغ صغير بين الأسطر
    else:
        st.warning("No products found for your search.")
else:
    # واجهة الترحيب عند عدم وجود بيانات
    st.info("👋 Welcome! Use the Admin Panel on the left to upload your Excel inventory.")
    st.image("https://via.placeholder.com/1200x400?text=Waiting+for+Your+Deals...", use_container_width=True)

# 7. تذييل الصفحة
st.markdown("---")
st.markdown("<center>© 2026 Global Deals Hub - All Rights Reserved</center>", unsafe_allow_html=True)
