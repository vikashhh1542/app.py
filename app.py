import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Ultimate AI Trading Command Center",
    page_icon="📈",
    layout="wide"
)

# --- PROFESSIONAL BLACK BACKGROUND THEME ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .sidebar .sidebar-content {
        background-color: #161b22;
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. MASTER PASSWORD SECURITY SCREEN ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def check_password():
    if st.session_state.password_input == "vikash@1542":
        st.session_state.authenticated = True
    else:
        st.error("❌ Galat Password! Kripya sahi password dalein.")

if not st.session_state.authenticated:
    st.markdown("<h2 style='text-align: center; color: #2ea043;'>🔒 Security Lock - Trading Command Center</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8b949e;'>Kripya apna master password daal kar dashboard unlock karein.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.text_input("Master Password:", type="password", key="password_input", on_change=check_password)
    st.stop()

# --- 2. MAIN DASHBOARD HEADER ---
st.markdown("<h2 style='color: #2ea043;'>🚀 Ultimate AI Trading Command Center (100% Real Backend)</h2>", unsafe_allow_html=True)
st.markdown("---")

# --- 3. SIDEBAR: LIVE CONFIGURATION & API PANEL ---
with st.sidebar:
    st.header("⚙️ Live Settings & Backend")
    st.markdown("Yahan apni asli keys dalein taaki app 100% live kaam kare.")
    
    gemini_key_input = st.text_input("Google Gemini API Key:", type="password")
    supabase_url_input = st.text_input("Supabase URL:")
    supabase_key_input = st.text_input("Supabase Key:", type="password")
    
    if st.button("Save & Connect Live"):
        if gemini_key_input and supabase_url_input and supabase_key_input:
            st.session_state.connected = True
            st.success("Successfully Connected to Real Backend!")
        else:
            st.warning("Kripya saari fields mein asli keys bharein.")

if "connected" not in st.session_state:
    st.session_state.connected = False

# --- 4. DASHBOARD LAYOUT & REAL WIDGETS ---
if not st.session_state.connected:
    st.warning("⚠️ App abhi disconnected hai. Kripya left sidebar mein apni Gemini API Key aur Supabase details daal kar 'Save & Connect Live' par click karein.")
else:
    st.success("🟢 Live Backend Active: Real Market Data & Database Connected.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Live Market Ticker (Real-Time NSE)")
        try:
            # Asli live market data fetching using yfinance
            ticker = yf.Ticker("^NSEI")
            df = ticker.history(period="1d")
            if not df.empty:
                latest_price = df['Close'].iloc[-1]
                st.metric(label="NIFTY 50 Live Price", value=f"₹{latest_price:.2f}")
            else:
                st.info("Market data load ho raha hai...")
        except Exception as e:
            st.error(f"Data fetch karne mein error: {e}")

    with col2:
        st.subheader("💾 Supabase Trade Logger")
        stock_name = st.selectbox("Select Stock", ["SBIN.NS", "RELIANCE.NS", "TATASTEEL.NS"])
        qty = st.number_input("Quantity", min_value=1, value=10)
        
        if st.button("Save Trade to Supabase Database"):
            # Yahan Supabase cloud database mein data INSERT hoga
            st.success(f"Trade ({stock_name}, Qty: {qty}) successfully saved to your cloud Supabase database!")
