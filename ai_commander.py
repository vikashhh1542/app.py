import streamlit as st
import pandas as pd
import yfinance as yf
import google.generativeai as genai

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Deep Timeframe Commander",
    page_icon="🤖",
    layout="wide"
)

# --- PROFESSIONAL BLACK BACKGROUND THEME ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='color: #2ea043;'>🤖 Multi-Timeframe & Indicator Deep AI Commander</h2>", unsafe_allow_html=True)
st.markdown("Yeh dedicated page aapke liye bina `app.py` ko chhede saare timeframes, indicators aur chart patterns ko deep analyze karega.")

# API Key Input for this page
api_key_input = st.text_input("Enter Google Gemini API Key:", type="password")

if api_key_input.strip():
    genai.configure(api_key=api_key_input.strip())
    
    target_symbol = st.text_input("Enter Stock / Index Symbol for Deep Scan (e.g., RELIANCE.NS, TCS.NS, NIFTY):", value="")
    
    if target_symbol.strip():
        if st.button("Run Multi-Timeframe & Pattern Deep Scan"):
            try:
                with st.spinner("Fetching multi-timeframe candles & running institutional AI analysis..."):
                    ticker = yf.Ticker(target_symbol.strip())
                    
                    # Fetching multiple timeframes
                    df_daily = ticker.history(period="1mo", interval="1d")
                    df_hourly = ticker.history(period="5d", interval="60m")
                    
                    if not df_daily.empty and not df_hourly.empty:
                        curr_price = df_daily['Close'].iloc[-1]
                        prev_close = df_daily['Close'].iloc[-2] if len(df_daily) > 1 else curr_price
                        pct_change = ((curr_price - prev_close) / prev_close) * 100
                        
                        prompt = f"""
                        You are an elite Chief Quantitative Trader and Technical Analyst.
                        Analyze '{target_symbol.upper()}' across multiple timeframes and indicators.
                        
                        Data Snapshot:
                        - Current Price: ₹{curr_price:.2f}
                        - Daily Change: {pct_change:.2f}%
                        - Daily Closes (Last 5): {df_daily['Close'].tail(5).tolist()}
                        - Hourly Closes (Last 5): {df_hourly['Close'].tail(5).tolist()}
                        
                        Provide a comprehensive institutional breakdown:
                        1. **Multi-Timeframe Alignment**: Trend analysis across Daily and Hourly charts.
                        2. **Indicator Confluence**: Moving averages, momentum, and volatility check.
                        3. **Chart Pattern Insights**: Potential breakouts, supports, or resistances.
                        4. **Exact Trading Setup**: Action (BUY/SELL/WAIT), Entry Zone, Strict Stop Loss, Target 1, Target 2.
                        5. **Risk & Exit Guidelines**: Trailing stop rules.
                        """
                        
                        model = genai.GenerativeModel("gemini-1.5-flash")
                        response = model.generate_content(prompt)
                        
                        st.markdown("### 📊 Supreme AI Trading Command & Analysis:")
                        st.write(response.text)
                    else:st.warning("Sahi symbol enter karein, data fetch nahi ho paya.")
            except Exception as e:
                st.error(f"Scan Error: {e}")
    else:
        st.info("Kripya upar wale box mein stock symbol daalein.")
else:
    st.warning("Kripya AI analysis ke liye apni Gemini API Key enter karein.")
