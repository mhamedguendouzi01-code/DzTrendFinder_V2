import streamlit as st
import pandas as pd
import pickle
from deepface import DeepFace
from scipy.spatial.distance import cosine
import os
from PIL import Image

# 1. إعدادات المنصة
st.set_page_config(page_title="Global AI Deals Hub", page_icon="🌍", layout="wide")

# 2. تصميم CSS احترافي (Modern Global Marketplace)
st.markdown("""
    <style>
    .main { background-color: #f6f9fc; }
    .product-card {
        background-color: white; border-radius: 12px; padding: 15px;
        border: 1px solid #e0e0e0; text-align: center;
        transition: 0.3s ease-in-out; margin-bottom: 20px;
    }
    .product-card:hover { transform: translateY(-5px); box-shadow: 0 12px 24px rgba(0,0,0,0.1); }
    .price { color: #d32f2f; font-weight: bold; font-size: 1.4rem; margin: 5px 0; }
    .title { font-size: 0.95rem; font-weight: 600; height: 50px; overflow: hidden; color: #333; margin-bottom: 10px; }
    img { border-radius: 10px; margin-bottom: 10px; object-fit: contain; }
    .stTabs [data-baseweb="tab-list"] { gap: 15px; }
    .stTabs [data-baseweb="tab"] { background-color: #ffffff; border-radius: 8px; padding: 10px 25px; }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة البيانات (تخزين السلع)
if 'inventory' not in st.session_state:
    st.session_state['inventory'] = None

# 4. لوحة التحكم (Admin Panel) لتخزين البيانات بالجملة
with st.sidebar:
    st.title("🛡️ Admin Panel")
    key = st.text_input("Security Key", type="password")
    if key == "dz2026":
        st.success("Authorized")
        file = st.file_uploader("Upload AliExpress Excel", type=['xlsx', 'csv'])
        if file:
            try:
                # قراءة الملف (سواء كان إكسل أو CSV)
                df = pd.read_excel(file) if file.name.endswith('xlsx') else pd.read_csv(file)
                df.columns = df.columns.astype(str).str.strip() # تنظيف العناوين
                
                # القاموس المحدث حسب الأعمدة اللي بعثتهم ذرك
                rename_dict = {
                    'Product Desc': 'Title', 'Product Name': 'Title', 'Product Title': 'Title',
                    'Price': 'Price', 'Discount Price': 'Price', 'Sale Price': 'Price',
                    'Image Url': 'Image', 'Product Main Image Url': 'Image', 'ImageUrl': 'Image',
                    'Link': 'Link', 'Promotion Url': 'Link', 'Promotion Link': 'Link'
                }
                df = df.rename(columns=rename_dict)
                
                # التحقق من الأعمدة
                needed = ['Title', 'Price', 'Image', 'Link']
                found = [c for c in needed if c in df.columns]
                
                if len(found) >= 4:
                    st.session_state['inventory'] = df
                    st.sidebar.success(f"✅ {len(df)} Items Loaded!")
                else:
                    st.sidebar.error(f"Missing columns. I need: Product Desc, Price, Image Url, Link")
            except Exception as e:
                st.sidebar.error(f"Error: {e}")

st.title("🌍 Global AI Deals Hub")
st.markdown("#### *Direct Deals from AliExpress - Powered by Visual Intelligence*")

# 5. الواجهة الرئيسية
if st.session_state['inventory'] is not None:
    df = st.session_state['inventory']

    # إنشاء Tabs للبحث
    tab_txt, tab_img = st.tabs(["🔍 Search by Text", "📷 Search by Image (AI)"])

    # 5.1. البحث بالنص (Text Search)
    with tab_txt:
        search = st.text_input("Type to find deals...", placeholder="Find your gadget...")
        if search:
            display_df = df[df['Title'].str.contains(search, case=False, na=False)]
        else:
            display_df = df

    # 5.2. البحث بالصورة (Visual Search AI)
    with tab_img:
        st.info("Upload a photo to find identical products!")
        
        # تحميل الملفات الضرورية للذكاء الاصطناعي
        @st.cache_resource
        def load_pkl():
            try:
                with open('image_hashes.pkl', 'rb') as f:
                    return pickle.load(f)
            except:
                st.error("image_hashes.pkl not found! visual search won't work.")
                return None
        
        db = load_pkl()
        
        if db:
            uploaded_image = st.file_uploader("Upload Image...", type=['png', 'jpg', 'jpeg'])
            if uploaded_image:
                st.image(uploaded_image, caption="Your Upload", width=200)
                
                with st.spinner("AI is thinking..."):
                    # حفظ الصورة مؤقتاً
                    temp_path = "user_input.jpg"
                    image_obj = Image.open(uploaded_image)
                    image_obj.convert('RGB').save(temp_path)
                    
                    try:
                        # استخراج الميزات باستعمال DeepFace
                        embedding = DeepFace.represent(img_path=temp_path, model_name="VGG-Face", enforce_detection=False)[0]["embedding"]
                        
                        # حساب التشابه
                        results = []
                        for item in db:
                            dist = cosine(embedding, item['embedding'])
                            score = 1 - dist
                            results.append({'id': item['id'], 'score': score})
                        
                        results = sorted(results, key=lambda x: x['score'], reverse=True)[:12]
                        
                        # تصفية قاعدة البيانات بناءً على النتائج
                        best_ids = [r['id'] for r in results if r['score'] > 0.8] # فقط المتشابهة جداً
                        display_df = df[df['Link'].isin(best_ids)]
                        
                    except Exception as e:
                        st.error(f"AI Error: {e}")
                    finally:
                        if os.path.exists(temp_path):
                            os.remove(temp_path)

    st.divider()
    
    # 6. عرض السلع في 4 أعمدة
    if 'display_df' in locals() and not display_df.empty:
        cols = st.columns(4)
        for i, (index, row) in enumerate(display_df.iterrows()):
            with cols[i % 4]:
                # جلب البيانات
                t = str(row.get('Title', 'No Title'))
                p = str(row.get('Price', '0.00'))
                img = str(row.get('Image', ''))
                lnk = str(row.get('Link', '#'))

                # تصحيح رابط الصورة
                if img.startswith('//'): img = 'https:' + img
                if img == 'nan' or not img.startswith('http'):
                    img = "https://via.placeholder.com/200?text=No+Image"

                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                try:
                    st.image(img, use_container_width=True)
                except:
                    st.image("https://via.placeholder.com/200?text=Image+Error", use_container_width=True)
                
                st.markdown(f'<div class="title">{t[:50]}...</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="price">${p}</div>', unsafe_allow_html=True)
                st.link_button("🔥 View Deal", lnk, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                st.write("")
    else:
        st.warning("No products found. Try a different search or upload inventory.")

else:
    st.info("👋 Welcome! Go to Sidebar -> Upload the Excel file from AliExpress.")
    st.image("https://via.placeholder.com/1000x300?text=Waiting+for+Inventory...", use_container_width=True)
