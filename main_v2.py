import streamlit as st
import pandas as pd
import re

# 1. إعدادات الصفحة والتصميم
st.set_page_config(page_title="مركز التوريد العالمي", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [data-testid="stSidebar"], .main { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .product-card {
        background: white; border-radius: 12px; padding: 15px;
        border: 1px solid #eee; text-align: center; height: 100%;
        transition: 0.3s;
    }
    .product-card:hover { box-shadow: 0 10px 20px rgba(0,0,0,0.1); transform: translateY(-5px); }
    .price-dzd { color: #27ae60; font-weight: bold; font-size: 1.2rem; }
    .product-img { height: 180px; object-fit: contain; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. وظيفة جلب البيانات (Persistency)
def load_data():
    # نحاول نقرأ الملف الثابت أولاً
    try:
        df = pd.read_excel("inventory.xlsx")
        return df
    except:
        # إذا ما لقاش الملف، نرجعو None باش يرفع واحد جديد
        return st.session_state.get('uploaded_df', None)

# 3. إدارة التنقل والذاكرة (Navigation & Memory)
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_item' not in st.session_state:
    st.session_state.selected_item = None

# --- صفحة المتجر (الجملة) ---
def show_home(df):
    st.title("🌍 مركز التوريد العالمي - الجزائر")
    
    if df is not None:
        # شريط البحث
        search = st.text_input("🔍 ابحث عن سلعة...", "")
        display_df = df[df.iloc[:, 0].astype(str).str.contains(search, case=False)] if search else df

        cols = st.columns(4)
        for i, (idx, row) in enumerate(display_df.iterrows()):
            with cols[i % 4]:
                # محرك استخراج الصور (الرادار اللي خدمناه)
                img = next((str(row[c]) for c in df.columns if 'src' in str(c).lower() and "http" in str(row[c])), "")
                if img.startswith('//'): img = 'https:' + img
                
                st.markdown(f"""
                    <div class="product-card">
                        <img src="{img}" class="product-img">
                        <div style="height:50px; overflow:hidden;"><b>{str(row.get('product-title-text', 'منتج'))[:50]}...</b></div>
                        <div class="price-dzd">{int(float(re.findall(r'\d+', str(row.get('tp-inline-block', '0')))[0]) * 240):,} دج</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # زر الانتقال للتفاصيل
                if st.button("عرض التفاصيل 🔍", key=f"btn_{idx}", use_container_width=True):
                    st.session_state.selected_item = row
                    st.session_state.page = 'details'
                    st.rerun()
    else:
        st.warning("⚠️ لم يتم العثور على بيانات. ارفع ملف الإكسل في القائمة الجانبية.")

# --- صفحة التفاصيل (Details Page) ---
def show_details():
    item = st.session_state.selected_item
    if st.button("⬅️ العودة للمتجر"):
        st.session_state.page = 'home'
        st.rerun()
        
    col1, col2 = st.columns([1, 1.2])
    with col1:
        img = next((str(item[c]) for c in item.index if 'src' in str(c).lower() and "http" in str(item[c])), "")
        st.image(img, use_container_width=True)
    
    with col2:
        st.title(item.get('product-title-text', 'اسم المنتج'))
        price_usd = float(re.findall(r'\d+', str(item.get('tp-inline-block', '0')))[0])
        st.header(f"السعر: {price_usd * 240:,.2f} دج")
        st.write(f"💵 السعر بالدولار: {price_usd}$")
        st.write("---")
        st.markdown("### تفاصيل التوريد")
        st.write("📦 **نوع البيع:** جملة (Wholesale)")
        st.write("📍 **المصدر:** علي بابا (التوصيل للجزائر)")
        
        # زر الواتساب (التنسيق للطلب)
        msg = f"أريد استيراد: {item.get('product-title-text')}"
        st.link_button("اطلب عبر واتساب ✅", f"https://wa.me/213XXXXXXXXX?text={msg}")

# --- القائمة الجانبية (Admin) ---
with st.sidebar:
    st.header("⚙️ الإدارة")
    up = st.file_uploader("تحديث السلعة (Excel)", type=['xlsx'])
    if up:
        st.session_state['uploaded_df'] = pd.read_excel(up)
        st.success("تم التحديث!")

# --- منطق التشغيل ---
main_df = load_data()
if st.session_state.page == 'home':
    show_home(main_df)
else:
    show_details()
