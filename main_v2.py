import streamlit as st
import pandas as pd

# 1. إعدادات المنصة العالمية
st.set_page_config(page_title="Global Deals Hub", page_icon="🌍", layout="wide")

# 2. تصميم CSS احترافي (Modern Marketplace Look)
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .product-card {
        background-color: white;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #e0e0e0;
        text-align: center;
        transition: 0.3s ease-in-out;
        height: 100%;
    }
    .product-card:hover { 
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.1); 
    }
    .price { color: #d32f2f; font-weight: bold; font-size: 1.4rem; margin: 5px 0; }
    .category-tag {
        background-color: #e3f2fd;
        color: #1976d2;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
    .title { font-size: 0.95rem; font-weight: 600; height: 45px; overflow: hidden; color: #333; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border-radius: 5px;
        padding: 10px 20px;
        border: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة البيانات (تخزين السلع)
if 'inventory' not in st.session_state:
    st.session_state['inventory'] = pd.DataFrame(columns=['Title', 'Price', 'Category', 'Image URL', 'Affiliate Link', 'Platform'])

# 4. لوحة التحكم (Admin Panel)
with st.sidebar:
    st.title("🛡️ Marketplace Admin")
    pwd = st.text_input("Security Key", type="password")
    
    if pwd == "dz2026":
        st.success("Admin Access Granted")
        
        # خيار 1: الرفع بالجملة (يحل مشكل التعب)
        st.subheader("📦 Bulk Upload (Excel)")
        uploaded_file = st.file_uploader("Upload your products file", type=['xlsx'])
        if uploaded_file:
            try:
                df_new = pd.read_excel(uploaded_file)
                df_new.columns = df_new.columns.str.strip() # تنظيف العناوين
                st.session_state['inventory'] = df_new
                st.sidebar.info(f"✅ Loaded {len(df_new)} items!")
            except Exception as e:
                st.error("Check Excel columns!")

        st.divider()
        
        # خيار 2: إضافة يدوية سريعة
        with st.expander("➕ Add Single Product"):
            t = st.text_input("Title")
            p = st.text_input("Price ($)")
            c = st.selectbox("Category", ["Electronics", "Home", "Gadgets", "Fashion", "Beauty"])
            img = st.text_input("Image URL")
            link = st.text_input("Affiliate Link")
            plat = st.selectbox("Source", ["AliExpress", "Amazon", "Temu"])
            
            if st.button("Publish Now"):
                new_row = pd.DataFrame([[t, p, c, img, link, plat]], columns=st.session_state['inventory'].columns)
                st.session_state['inventory'] = pd.concat([st.session_state['inventory'], new_row], ignore_index=True)
                st.toast("Published!")

        if st.button("🗑️ Clear Everything"):
            st.session_state['inventory'] = pd.DataFrame(columns=st.session_state['inventory'].columns)
            st.rerun()

# 5. الواجهة الرئيسية للعرض
st.title("🌍 Global Deals Hub")
st.write("### Your Gateway to Viral International Products")

df = st.session_state['inventory']

if not df.empty:
    # محرك بحث ذكي
    search = st.text_input("🔍 Search our global inventory...", placeholder="Type to find amazing deals...")
    if search:
        df = df[df['Title'].str.contains(search, case=False, na=False)]

    # نظام التصنيفات (Tabs)
    unique_cats = ["All Deals"] + sorted(df['Category'].unique().tolist())
    tabs = st.tabs(unique_cats)

    for i, tab in enumerate(tabs):
        with tab:
            cat_filter = unique_cats[i]
            display_df = df if cat_filter == "All Deals" else df[df['Category'] == cat_filter]
            
            if display_df.empty:
                st.warning("No items in this category.")
            else:
                # عرض السلع في 4 أعمدة (منصة عالمية)
                rows = len(display_df)
                cols_count = 4
                for r_idx in range(0, rows, cols_count):
                    cols = st.columns(cols_count)
                    for c_idx in range(cols_count):
                        item_idx = r_idx + c_idx
                        if item_idx < rows:
                            row = display_df.iloc[item_idx]
                            with cols[c_idx]:
                                st.markdown(f"""
                                <div class="product-card">
                                    <div class="category-tag">{row['Category']}</div>
                                    <img src="{row['Image URL']}" style="width:100%; height:180px; object-fit:contain; border-radius:8px;">
                                    <div class="title">{row['Title'][:50]}...</div>
                                    <div class="price">${row['Price']}</div>
                                </div>
                                """, unsafe_allow_html=True)
                                st.link_button(f"View on {row['Platform']}", row['Affiliate Link'], use_container_width=True)
                                st.write("")
else:
    st.info("👋 Welcome to Global Deals Hub! Admin: Please upload inventory to start.")
    st.image("https://via.placeholder.com/1000x300?text=Marketplace+Offline+-+Waiting+for+Data", use_container_width=True)

# 6. Footer
st.markdown("---")
st.markdown("<center>© 2026 Global Deals Hub | Automated Affiliate Solutions</center>", unsafe_allow_html=True)
