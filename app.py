import streamlit as st
import sqlite3
import urllib.parse
from datetime import datetime

# 1. Global Configuration
st.set_page_config(page_title="Global Trend Finder | Best Tech Deals", layout="wide", initial_sidebar_state="collapsed")

# 2. Global Professional CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    .stApp { background-color: #ffffff; font-family: 'Inter', sans-serif; }
    
    /* Global Header */
    .hero-section {
        text-align: center; padding: 60px 20px; background: linear-gradient(135deg, #1a1a1a 0%, #333333 100%);
        color: white; border-radius: 0 0 40px 40px; margin-bottom: 40px;
    }

    /* Product Cards */
    .deal-card {
        background: white; border-radius: 24px; padding: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05); transition: 0.4s;
        border: 1px solid #f0f0f0; margin-bottom: 25px; text-align: left;
    }
    .deal-card:hover { transform: translateY(-10px); box-shadow: 0 20px 40px rgba(0,0,0,0.1); border-color: #ff4747; }
    .product-img { width: 100%; border-radius: 18px; aspect-ratio: 1/1; object-fit: cover; }
    
    .price-tag { font-size: 24px; font-weight: 900; color: #ff4747; }
    .old-price { text-decoration: line-through; color: #999; font-size: 14px; margin-left: 8px; }
    .discount-badge { 
        background: #ff4747; color: white; padding: 4px 12px; 
        border-radius: 10px; font-weight: bold; font-size: 12px;
    }
    
    div.stButton > button {
        border-radius: 12px; font-weight: 700; width: 100%;
        background: #1a1a1a; color: white; height: 50px; border: none;
    }
    div.stButton > button:hover { background: #ff4747; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 3. Database Function
def get_data():
    conn = sqlite3.connect('dz_finder.db')
    conn.row_factory = sqlite3.Row
    res = conn.execute("SELECT * FROM products ORDER BY added_at DESC").fetchall()
    conn.close()
    return res

if 'page' not in st.session_state: st.session_state.page = 'home'

# --- PAGE 1: GLOBAL HOME ---
if st.session_state.page == 'home':
    st.markdown("""
        <div class="hero-section">
            <h1 style='font-size: 45px; font-weight: 900;'>🔥 Global Trend Finder</h1>
            <p style='font-size: 18px; opacity: 0.8;'>Hand-picked Tech & Gadget Deals with Worldwide Shipping</p>
        </div>
    """, unsafe_allow_html=True)
    
    products = get_data()
    
    cols = st.columns(4)
    for i, row in enumerate(products):
        discount = int(((row['market_price'] - row['promo_price']) / row['market_price']) * 100)
        with cols[i % 4]:
            st.markdown(f"""
                <div class="deal-card">
                    <img src="{row['image_url']}" class="product-img">
                    <div style="margin-top:15px; font-weight:700; height:45px; overflow:hidden;">{row['title']}</div>
                    <div style="margin: 10px 0;">
                        <span class="price-tag">${row['promo_price']/200:.2f}</span>
                        <span class="old-price">${row['market_price']/200:.2f}</span>
                    </div>
                    <div class="discount-badge">SAVE {discount}%</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("View Deal →", key=f"d_{row['id']}"):
                st.session_state.selected_id = row['id']
                st.session_state.page = 'detail'
                st.rerun()

# --- PAGE 2: PRODUCT DETAIL ---
elif st.session_state.page == 'detail':
    if st.button("← Back to Deals"):
        st.session_state.page = 'home'
        st.rerun()
    
    conn = sqlite3.connect('dz_finder.db')
    conn.row_factory = sqlite3.Row
    p = conn.execute("SELECT * FROM products WHERE id = ?", (st.session_state.selected_id,)).fetchone()
    conn.close()

    if p:
        c1, c2 = st.columns([1.2, 1])
        with c1:
            st.image(p['image_url'], use_container_width=True)
        with c2:
            st.markdown(f"""
                <h1 style='font-size:35px;'>{p['title']}</h1>
                <h2 style='color:#ff4747; font-size:45px;'>${p['promo_price']/200:.2f}</h2>
                <p style='color:#888; text-decoration:line-through;'>Original Price: ${p['market_price']/200:.2f}</p>
                <div style='background:#f9f9f9; padding:20px; border-radius:15px;'>
                    <p>⭐ <b>Rating:</b> {p['rating']}/5.0</p>
                    <p>📦 <b>Shipping:</b> Worldwide Available</p>
                    <p>🛡️ <b>Buyer Protection:</b> 75-Day Money Back Guarantee</p>
                </div>
                <br>
            """, unsafe_allow_html=True)
            
            # This would be your Affiliate Link
            st.link_button("🚀 GET THIS DEAL ON ALIEXPRESS", "https://s.click.aliexpress.com/...")

# --- ADMIN PANEL ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
with st.expander("🔐 Global Admin Console"):
    if st.text_input("Access Key", type="password") == "dz2026":
        if st.button("🚀 Scrape Global Deals"):
            import scraper
            scraper.auto_hunter()
            st.success("Global database updated!")
            st.rerun()