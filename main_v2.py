import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="Global Sourcing Hub DZ", layout="wide")

# --- 1. وظيفة لجلب البيانات (باش تقعد مڤارديا) ---
def load_data():
    # هنا تقدر تحط اسم ملف الإكسل تاعك اللي فيه السلعة
    try:
        df = pd.read_excel("inventory.xlsx") # الملف لازم يكون في نفس Dossier
        return df
    except:
        return None

# --- 2. إدارة التنقل بين الصفحات ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_item' not in st.session_state:
    st.session_state.selected_item = None

# --- 3. صفحة المتجر (الجملة) ---
def show_home():
    st.title("🌍 متجر الجملة - الجزائر")
    df = load_data()
    
    if df is not None:
        cols = st.columns(4)
        for i, (idx, row) in enumerate(df.iterrows()):
            with cols[i % 4]:
                st.image(row['Image'], use_column_width=True)
                st.subheader(row['Title'][:50])
                st.write(f"السعر: {row['Price']} $")
                
                # زر "عرض التفاصيل" هو اللي ينسق بين الصفحات
                if st.button(f"تفاصيل المنتج", key=f"btn_{idx}"):
                    st.session_state.selected_item = row
                    st.session_state.page = 'details'
                    st.rerun()
    else:
        st.warning("يرجى التأكد من وجود ملف inventory.xlsx في مجلد المشروع")

# --- 4. صفحة التفاصيل (Detail Page) ---
def show_details():
    item = st.session_state.selected_item
    if item is not None:
        if st.button("⬅️ العودة للمتجر"):
            st.session_state.page = 'home'
            st.rerun()
            
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image(item['Image'], width=400)
        with col2:
            st.title(item['Title'])
            st.header(f"السعر: {item['Price']} $")
            st.write(f"**الكمية الدنيا (MOQ):** {item.get('MOQ', '10 قطع')}")
            st.write("---")
            st.write("**وصف المنتج:**")
            st.write(item.get('Description', 'لا يوجد وصف متاح حالياً لهذا المنتج المستورد.'))
            
            # زر التواصل
            st.link_button("طلب السلعة عبر واتساب ✅", f"https://wa.me/213XXXXXXX?text=اريد_طلب_{item['Title']}")

# --- 5. منطق التشغيل ---
if st.session_state.page == 'home':
    show_home()
else:
    show_details()
