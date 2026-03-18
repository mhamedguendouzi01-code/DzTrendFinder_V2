import streamlit as st
import pandas as pd

st.set_page_config(page_title="Smart Auto-Category Store", layout="wide")

# تصميم احترافي
st.markdown("""
    <style>
    .product-card {
        background: white; border-radius: 15px; padding: 15px;
        border: 1px solid #eee; text-align: center; height: 100%;
        transition: 0.3s ease;
    }
    .product-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
    .price { color: #2ecc71; font-weight: bold; font-size: 1.4rem; }
    .title { font-size: 0.85rem; font-weight: 600; height: 45px; overflow: hidden; color: #333; }
    .cat-label { background: #f0f2f6; color: #555; font-size: 0.7rem; padding: 2px 8px; border-radius: 10px; margin-bottom: 5px; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

if 'inventory' not in st.session_state: st.session_state['inventory'] = None

# --- الجانب الإداري ---
with st.sidebar:
    st.title("🛡️ Admin")
    if st.text_input("Key", type="password") == "dz2026":
        file = st.file_uploader("Upload Scraped File", type=['xlsx', 'csv'])
        if file:
            try:
                df = pd.read_excel(file) if file.name.endswith('xlsx') else pd.read_csv(file)
                df.columns = df.columns.astype(str).str.strip()
                
                # قاموس ذكي للأعمدة بما فيها الكاتيقوري
                mapping = {
                    'Product Desc': 'Title', 'Product Name': 'Title', 'title': 'Title',
                    'Price': 'Price', 'sale_price': 'Price',
                    'Image Url': 'Image', 'main_image': 'Image',
                    'Link': 'Link', 'url': 'Link',
                    'Category': 'Category', 'category': 'Category', 'Category Name': 'Category', 'item_category': 'Category'
                }
                df = df.rename(columns=mapping)
                
                # إذا لم يجد عمود Category، نصنفه "General"
                if 'Category' not in df.columns:
                    df['Category'] = 'General'
                
                st.session_state['inventory'] = df
                st.sidebar.success(f"✅ Loaded {len(df)} Items!")
            except Exception as e:
                st.sidebar.error(f"Error: {e}")

# --- واجهة العرض ---
st.title("🛒 Smart Multi-Store")

if st.session_state['inventory'] is not None:
    df = st.session_state['inventory']
    
    # استخراج قائمة الأصناف من الملف تلقائياً
    raw_categories = df['Category'].dropna().unique().tolist()
    # تنظيف الأسماء (لأن علي إكسبريس يعطي مسارات طويلة مثل Electronics > Phones)
    clean_categories = sorted(list(set([str(c).split('>')[0].strip() for c in raw_categories])))
    
    categories = ["All Products"] + clean_categories
    
    # القائمة المنسدلة (Dropdown)
    selected_cat = st.selectbox("📂 Filter by Category:", categories)

    # محرك البحث
    search = st.text_input("🔍 Search for a specific item...")

    # الفلترة
    filtered_df = df.copy()
    if selected_cat != "All Products":
        # فلترة ذكية (تبحث إذا كان الكاتيقوري يحتوي على الكلمة المختارة)
        filtered_df = filtered_df[filtered_df['Category'].str.contains(selected_cat, case=False, na=False)]
    
    if search:
        filtered_df = filtered_df[filtered_df['Title'].str.contains(search, case=False, na=False)]

    st.divider()

    # العرض
    cols = st.columns(4)
    for i, (idx, row) in enumerate(filtered_df.iterrows()):
        with cols[i % 4]:
            t, p, img, lnk, c = str(row.get('Title','')), str(row.get('Price','0')), str(row.get('Image','')), str(row.get('Link','#')), str(row.get('Category','General')).split('>')[0]
            
            if img.startswith('//'): img = 'https:' + img
            
            st.markdown(f'''
                <div class="product-card">
                    <span class="cat-label">{c}</span>
                    <img src="{img if "http" in img else "https://via.placeholder.com/150"}" style="width:100%; border-radius:10px;">
                    <div class="title">{t[:55]}...</div>
                    <div class="price">${p}</div>
                </div>
            ''', unsafe_allow_html=True)
            st.link_button("🚀 Get Deal", lnk, use_container_width=True)
            st.write("")
else:
    st.info("Upload your AliExpress/Temu file to see the magic!")
