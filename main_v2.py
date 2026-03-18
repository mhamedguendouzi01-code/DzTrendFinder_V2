if st.session_state['data'] is not None:
    df = st.session_state['data']
    cols = st.columns(4)
    for i, row in df.iterrows():
        with cols[i % 4]:
            with st.container():
                # 1. جلب البيانات وتصحيحها
                t = str(row.get('Title', 'No Title'))
                p = str(row.get('Price', '0.00'))
                img = str(row.get('Image', ''))
                lnk = str(row.get('Link', '#'))
                
                # 2. تصحيح رابط الصورة (هذا هو سبب الخطأ)
                if img.startswith('//'):
                    img = 'https:' + img
                elif not img.startswith('http'):
                    img = "https://via.placeholder.com/150?text=No+Image"

                st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
                
                # 3. محاولة عرض الصورة بأمان
                try:
                    if img and img != 'nan':
                        st.image(img, use_container_width=True)
                    else:
                        st.image("https://via.placeholder.com/150?text=No+Image", use_container_width=True)
                except:
                    st.image("https://via.placeholder.com/150?text=Error+Loading", use_container_width=True)

                st.markdown(f'<div class="title">{t[:60]}...</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="price">${p}</div>', unsafe_allow_html=True)
                st.link_button("🔥 Get Deal", lnk, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                st.write("")
