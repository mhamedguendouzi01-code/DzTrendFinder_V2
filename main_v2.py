import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="Global Sourcing DZ", layout="wide")

# 2. وظيفة جلب البيانات (معدلة لتقرأ من ملف ثابت أو رابط)
def get_data():
    try:
        # هنا تقدر تحط رابط Google Sheet مباشر (CSV) باش يقعد مڤاردي
        df = pd.read_excel("inventory.xlsx") 
        return df
    except:
        return None

# 3. نظام التنقل (Navigation System)
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'main'
if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None

# --- صفحة المتجر الرئيسية ---
def show_main_page(df):
    st.title("🌍 مركز التوريد العالمي - الجزائر")
    st.write("---")
    
    if df is not None:
        cols = st.columns(4)
        for i, (idx, row) in enumerate(df.iterrows()):
            with cols[i % 4]:
                # عرض كارد المنتج
                st.image(row.get('Image_URL', 'https://via.placeholder.com/200'), use_container_width=True)
                st.subheader(f"{row.get('Title', 'منتج')[:40]}...")
                st.write(f"💰 {row.get('Price', 0)} دولار")
                
                # زر الانتقال لصفحة التفاصيل
                if st.button("تفاصيل المنتج 🔍", key=f"prod_{idx}"):
                    st.session_state.selected_product = row
                    st.session_state.current_page = 'details'
                    st.rerun()
    else:
        st.error("لم يتم العثور على بيانات. يرجى رفع ملف inventory.xlsx")

# --- صفحة تفاصيل المنتج (Detail View) ---
def show_details():
    product = st.session_state.selected_product
    
    if st.button("⬅️ العودة للمتجر"):
        st.session_state.current_page = 'main'
        st.rerun()
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.image(product.get('Image_URL', ''), use_container_width=True)
    
    with col2:
        st.title(product.get('Title', ''))
        st.header(f"السعر: {product.get('Price', 0)} دولار")
        st.info(f"💡 الكمية الدنيا للطلب: {product.get('MOQ', 'غير محددة')}")
        
        st.write("### وصف المنتج")
        st.write(product.get('Description', 'لا يوجد وصف مفصل حالياً.'))
        
        st.write("---")
        # زر الواتساب للطلب المباشر
        wa_msg = f"مرحباً، أريد الاستفسار عن منتج: {product.get('Title')}"
        st.link_button("اطلب عبر واتساب 🟢", f"https://wa.me/213XXXXXXXXX?text={wa_msg}")

# --- منطق تشغيل السيت ---
data = get_data()

if st.session_state.current_page == 'main':
    show_main_page(data)
else:
    show_details()
