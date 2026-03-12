import streamlit as st
import sqlite3

st.set_page_config(page_title="GLOBAL HUB", layout="wide")

st.markdown("""
    <style>
    .card { background: white; border-radius: 6px; padding: 5px; border: 1px solid #eee; text-align: center; height: 210px; }
    .price-usd { color: #10b981; font-weight: bold; font-size: 16px; }
    .stImage > img { height: 90px !important; object-fit: contain; }
    .origin-tag { background: #333; color: white; font-size: 8px; padding: 2px 4px; border-radius: 3px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌎 Global Deal Finder ($)")

conn = sqlite3.connect('dz_finder.db')
try:
    items = conn.execute("SELECT origin, name, price_usd, discount, link, image_url FROM products").fetchall()
    conn.close()

    if items:
        cols = st.columns(10)
        for i, item in enumerate(items):
            with cols[i % 10]:
                st.markdown(f'<div class="card">', unsafe_allow_html=True)
                st.markdown(f'<span class="origin-tag">{item[0]}</span>', unsafe_allow_html=True)
                st.image(item[5])
                st.markdown(f"<p style='font-size:10px;'>{item[1][:15]}</p>", unsafe_allow_html=True)
                st.markdown(f'<p class="price-usd">${item[2]}</p>', unsafe_allow_html=True)
                st.link_button("View", item[4], use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Run Scraper in Actions first.")
except Exception as e:
    st.error(f"Error: {e}")