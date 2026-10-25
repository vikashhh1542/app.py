 import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
from supabase import create_client, Client

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
    st.stop()# --- 2. MAIN DASHBOARD HEADER ---
st.markdown("<h2 style='color: #2ea043;'>🚀 Ultimate AI Trading Command Center (100% Zero Hardcoding)</h2>", unsafe_allow_html=True)
st.markdown("---")

# --- 3. SIDEBAR: LIVE CONFIGURATION & API PANEL ---
with st.sidebar:
    st.header("⚙️ Live Settings & Backend")
    st.markdown("Yahan apni asli keys dalein taaki app live connect ho.")
    
    gemini_key_input = st.text_input("Google Gemini API Key:", type="password")
    supabase_url_input = st.text_input("Supabase URL:")
    supabase_key_input = st.text_input("Supabase Key:", type="password")
    
    if st.button("Save & Connect Live"):
        if supabase_url_input and supabase_key_input:
            try:
                supabase: Client = create_client(supabase_url_input, supabase_key_input)
                st.session_state.supabase = supabase
                st.session_state.connected = True
                st.success("Successfully Connected to Supabase!")
            except Exception as e:
                st.error(f"Connection Error: {e}")
        else:
            st.warning("Kripya Supabase URL aur Key zaroor bharein.")

if "connected" not in st.session_state:
    st.session_state.connected = False# --- 4. DASHBOARD LAYOUT (ZERO HARDCODING) ---
if not st.session_state.connected:
    st.warning("⚠️ App disconnected hai. Left sidebar mein apni Supabase details daal kar connect karein.")
else:
    st.success("🟢 Live Backend Active: Zero Hardcoded Data Mode.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Live Market Ticker (Dynamic Lookup)")
        # Absolutely blank input - zero hardcoded stocks
        custom_ticker = st.text_input("Enter Stock Symbol (e.g., RELIANCE.NS, TCS.NS, ^NSEI):", value="")
        
        if custom_ticker:
            try:
                ticker = yf.Ticker(custom_ticker.strip())
                df = ticker.history(period="1d")
                if not df.empty:
                    latest_price = df['Close'].iloc[-1]
                    st.metric(label=f"Live Price: {custom_ticker.upper()}", value=f"₹{latest_price:.2f}")
                else:
                    st.warning(f"'{custom_ticker}' ka data nahi mila. Sahi symbol dalein.")
            except Exception as e:
                st.error(f"Data fetch karne mein error: {e}")
        else:
            st.info("Kripya upar wale box mein koi bhi stock symbol type karein (jaise RELIANCE.NS).")

    with col2:
        st.subheader("💾 Supabase Trade Logger")
        # Completely blank fields - zero preset values
        stock_name = st.text_input("Stock Name:", value="")
        qty = st.number_input("Quantity", min_value=0, value=0)
        buy_price = st.number_input("Entry Price (₹)", min_value=0.0, value=0.0, format="%.2f")
        
        if st.button("Save Trade to Supabase Database"):
            if stock_name and qty > 0 and buy_price > 0:
                try:
                    supabase = st.session_state.supabase
                    data = {
                        "stock_name": stock_name.strip().upper(),
                        "quantity": int(qty),
                        "buy_price": float(buy_price),
                        "created_at": str(datetime.now())
                    }
                    response = supabase.table("trades").insert(data).execute()st.success(f"✅ Trade successfully saved to Supabase cloud!")
                except Exception as e:
                    st.error(f"Database Save Error: {e}")
            else:
                st.warning("Kripya stock name, quantity aur price saari fields sahi se bharein.")

    st.markdown("---")
    st.subheader("📊 Live Trade History from Supabase Cloud")
    
    try:
        supabase = st.session_state.supabase
        response = supabase.table("trades").select("*").execute()
        trades_data = response.data
        
        if trades_data:
            df_trades = pd.DataFrame(trades_data)
            st.dataframe(df_trades, use_container_width=True)
        else:
            st.info("Database bilkul khali hai. Upar form se trade save karne par yahan live dikhega.")
    except Exception as e:
        st.info("Supabase table 'trades' se data fetch karne mein wait kiya ja raha hai.")
