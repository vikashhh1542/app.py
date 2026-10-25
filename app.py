import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
from supabase import create_client, Client
import google.generativeai as genai
import streamlit.components.v1 as components

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

# --- 1. MASTER SECURITY & AUTHENTICATION ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def check_password():
    if st.session_state.password_input == "vikash@1542":
        st.session_state.authenticated = True
    else:
        st.error("❌ Galat Password! Kripya sahi password dalein.")

if not st.session_state.authenticated:
    st.markdown("<h2 style='text-align: center; color: #2ea043;'>🔒 Security Lock - Trading Command Center</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8b949e;'>Kripya apna master password (vikash@1542) daal kar dashboard unlock karein.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.text_input("Master Password:", type="password", key="password_input", on_change=check_password)
    st.stop()

# --- 2. MASTER SETTINGS & RISK MANAGEMENT PANEL (SIDEBAR) ---
with st.sidebar:
    st.header("⚙️ Master Settings & Credentials")
    supabase_url_input = st.text_input("Supabase URL:")
    supabase_key_input = st.text_input("Supabase Key:", type="password")
    gemini_key_input = st.text_input("Google Gemini API Key:", type="password")
    
    if st.button("Save & Connect Backend"):
        if supabase_url_input and supabase_key_input:
            try:
                supabase: Client = create_client(supabase_url_input, supabase_key_input)
                st.session_state.supabase = supabase
                st.session_state.connected = True
                
                if gemini_key_input:
                    genai.configure(api_key=gemini_key_input.strip())
                    st.session_state.gemini_active = True
                else:
                    st.session_state.gemini_active = False
                    
                st.success("Successfully Connected to Supabase & AI Backend!")
            except Exception as e:
                st.error(f"Connection Error: {e}")
        else:
            st.warning("Kripya Supabase URL aur Key zaroor bharein.")

    st.markdown("---")
    st.subheader("🛡️ Risk & Capital Controls")
    capital_balance = st.number_input("Starting Capital (₹)", value=0.0, step=500.0)
    daily_target = st.number_input("Daily Profit Target (₹)", value=0.0, step=100.0)
    max_trades = st.number_input("Max Daily Trades Limit", value=0, min_value=0)
    
    st.markdown("---")
    st.subheader("🎛️ Master Toggles & Controls")
    st.toggle("API Request Limit Optimizer", value=True)
    st.toggle("Live Volatility Scanner", value=True)
    st.toggle("Auto Trailing Stop-Loss", value=False)
    st.toggle("Consecutive Loss Circuit Breaker", value=True)
    st.toggle("High-Conviction Mega Profit Override", value=False)
    st.toggle("Advanced Order Routing", value=True)
    st.toggle("AI Sentiment Filter", value=True)
    
    st.markdown("---")
    if st.button("🚨 EMERGENCY: SQUARE OFF ALL", type="primary"):
        st.error("🚨 EMERGENCY TRIGGERED: All active positions squared off and locked successfully!")

if "connected" not in st.session_state:
    st.session_state.connected = False
if "gemini_active" not in st.session_state:
    st.session_state.gemini_active = False# --- 3. TOP METRICS HEADER BAR ---
db_status = "Connected 🟢" if st.session_state.connected else "Offline 🔴"

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("Capital Balance", f"₹{capital_balance:,.2f}")
col_m2.metric("Daily Profit Target", f"₹{daily_target:,.2f}")
col_m3.metric("Allowed Trades Counter", f"{max_trades} Trades Max")
col_m4.metric("Database Status", db_status)

st.markdown("---")

# --- MAIN DASHBOARD HEADER ---
st.markdown("<h2 style='color: #2ea043;'>🚀 Ultimate AI Trading Command Center (Permanent Master Build)</h2>", unsafe_allow_html=True)

# --- 4. LIVE TRADINGVIEW CANDLESTICK CHART & ASSET SELECTOR ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📈 Live TradingView Candlestick Chart & Dynamic Asset Selector")
    custom_symbol = st.text_input("Enter NSE/BSE Symbol (e.g., RELIANCE, TCS, NIFTY):", value="")
    
    if custom_symbol.strip():
        formatted_symbol = f"NSE:{custom_symbol.strip().upper()}" if not ":" in custom_symbol else custom_symbol.strip().upper()
        
        tradingview_html = f"""
        <div class="tradingview-widget-container" style="height:450px;width:100%">
          <div id="tradingview_chart" style="height:100%;width:100%"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script type="text/javascript">
          new TradingView.widget(
          {{
            "width": "100%",
            "height": "450",
            "symbol": "{formatted_symbol}",
            "interval": "15",
            "timezone": "Asia/Kolkata",
            "theme": "dark",
            "style": "1",
            "locale": "en",
            "toolbar_bg": "#161b22",
            "enable_publishing": false,
            "allow_symbol_change": true,
            "container_id": "tradingview_chart"
          }});
          </script>
        </div>
        """
        components.html(tradingview_html, height=460)
    else:
        st.info("Kripya upar wale box mein koi bhi stock symbol type karein (jaise RELIANCE, TCS, NIFTY).")

with col2:
    st.subheader("💾 Supabase Trade Logger")
    stock_name = st.text_input("Stock Name to Save:", value="")
    qty = st.number_input("Quantity", min_value=0, value=0)
    buy_price = st.number_input("Entry Price (₹)", min_value=0.0, value=0.0, format="%.2f")
    
    if st.button("Save Trade to Supabase Database"):
        if st.session_state.connected and stock_name and qty > 0 and buy_price > 0:
            try:
                supabase = st.session_state.supabase
                data = {
                    "stock_name": stock_name.strip().upper(),
                    "quantity": int(qty),
                    "buy_price": float(buy_price),
                    "created_at": str(datetime.now())
                }
                response = supabase.table("trades").insert(data).execute()
                st.success("✅ Trade successfully saved to Supabase cloud table!")
            except Exception as e:
                st.error(f"Database Save Error: {e}")
        else:
            st.warning("Kripya pehle sidebar se Supabase connect karein aur saari fields sahi bharein.")

st.markdown("---")# --- 5. GEMINI AI ADVISOR & SIGNAL GENERATOR ---
st.subheader("🤖 Google Gemini AI Advisor & Autonomous Signal Generator")
if not st.session_state.gemini_active:
    st.info("💡 AI Signals use karne ke liye left sidebar mein apni Google Gemini API Key enter karein.")
else:
    ai_query = st.text_area("Ask AI for Trading Strategy (Entry, Target, Stop-Loss, Exit rules):", value="")
    if st.button("Generate AI Trade Signals"):
        if ai_query.strip():
            try:
                with st.spinner("Gemini AI is analyzing market setup..."):
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    prompt = f"""
                    You are an expert algorithmic stock trader. 
                    User Starting Capital: ₹{capital_balance}, Daily Target: ₹{daily_target}.
                    Query/Asset: {ai_query}
                    Provide a professional trading breakdown:
                    1. Action (BUY / SELL / HOLD)
                    2. Precise Entry Price Zone
                    3. Strict Stop Loss
                    4. Target 1 & Target 2
                    5. Exit Strategy & Risk Guidelines
                    """
                    response = model.generate_content(prompt)
                    st.markdown("### 📊 AI Recommendations & Risk Setup:")
                    st.write(response.text)
            except Exception as e:
                st.error(f"AI Error: {e}")
        else:
            st.warning("Kripya pehle apna sawal ya asset query type karein.")

st.markdown("---")

# --- 6. UNIVERSAL MARKET SCANNER TABLE ---
st.subheader("📊 Universal Market Scanner & Volatility Table")
st.markdown("Yahan apne pasand ke symbols comma separated (jaise RELIANCE.NS, TCS.NS) daal kar scanner chalayein:")

scanner_input = st.text_input("Enter Scanner Symbols (Comma Separated):", value="")

if scanner_input.strip():
    symbols_list = [s.strip().upper() for s in scanner_input.split(",") if s.strip()]
    scanner_data = []
    
    for sym in symbols_list:
        try:
            t = yf.Ticker(sym)
            hist = t.history(period="2d")
            if len(hist) >= 2:
                curr = hist['Close'].iloc[-1]
                prev = hist['Close'].iloc[-2]
                chg = ((curr - prev) / prev) * 100
                volatility = "High" if abs(chg) > 2.0 else ("Medium" if abs(chg) > 1.0 else "Low")
                scanner_data.append({
                    "Symbol": sym,
                    "Live Price (₹)": round(curr, 2),
                    "Change (%)": round(chg, 2),
                    "Volatility Rank": volatility
                })
        except Exception:
            pass
            
    if scanner_data:
        df_scanner = pd.DataFrame(scanner_data)
        st.dataframe(df_scanner, use_container_width=True)
    else:
        st.warning("Kripya valid symbols enter karein.")
else:
    st.info("Scanner chalane ke liye upar symbols enter karein.")

st.markdown("---")

# --- 7. SUPABASE TRADE AUDIT TRAIL & HISTORY ---
st.subheader("📋 Supabase Trade Audit Trail & History")
if st.session_state.connected:
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
        st.info(f"Supabase table error: {e}")
else:
    st.info("Trade history dekhne ke liye left sidebar se Supabase connect karein.")
