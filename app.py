"""
GrowGuru — Stock Fundamental Valuation Analyzer
================================================
Built for Streamlit Community Cloud.
Financial logic mirrors GrowGuru_Valuation_Model_2.xlsx exactly.
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Stock · Valuation Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS — clean, disciplined dark-accent UI
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base & Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── App background ── */
.stApp {
    background-color: #0f1117;
    color: #e8eaf0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #161b27;
    border-right: 1px solid #2a2f3e;
}
[data-testid="stSidebar"] * {
    color: #c9cfe0 !important;
}
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stNumberInput label {
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: #7b8cad !important;
}

/* ── Sidebar section headers ── */
.sidebar-section {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #4a9eff !important;
    margin: 1.4rem 0 0.5rem 0;
    padding-bottom: 0.3rem;
    border-bottom: 1px solid #2a3550;
}

/* ── Main header ── */
.main-header {
    display: flex;
    align-items: baseline;
    gap: 0.6rem;
    margin-bottom: 0.2rem;
}
.brand-name {
    font-size: 1.6rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.02em;
}
.brand-tag {
    font-size: 0.75rem;
    font-weight: 500;
    color: #4a9eff;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 2px 8px;
    border: 1px solid #4a9eff;
    border-radius: 3px;
}
.tagline {
    font-size: 0.82rem;
    color: #5a6580;
    margin-bottom: 1.8rem;
    letter-spacing: 0.01em;
}

/* ── Ticker input area ── */
.ticker-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #7b8cad;
    margin-bottom: 0.35rem;
}

/* ── Company name display ── */
.company-display {
    background: linear-gradient(135deg, #1a2035 0%, #1e2640 100%);
    border: 1px solid #2e3a54;
    border-radius: 8px;
    padding: 1rem 1.4rem;
    margin-bottom: 1.4rem;
}
.company-display .co-name {
    font-size: 1.05rem;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 0.2rem;
}
.company-display .co-sector {
    font-size: 0.75rem;
    color: #5a6a8a;
}

/* ── Metric cards ── */
.metric-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
}
.metric-card {
    flex: 1;
    background: #161b27;
    border: 1px solid #232a3b;
    border-radius: 8px;
    padding: 1rem 1.2rem;
}
.metric-card .mc-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #5a6a8a;
    margin-bottom: 0.3rem;
}
.metric-card .mc-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.25rem;
    font-weight: 600;
    color: #e8eaf0;
}
.metric-card .mc-sub {
    font-size: 0.7rem;
    color: #4a5570;
    margin-top: 0.15rem;
}

/* ── Verdict banner ── */
.verdict-good {
    background: linear-gradient(135deg, #0d2e1f 0%, #0f3325 100%);
    border: 1px solid #1a5e38;
    border-left: 4px solid #22c55e;
    border-radius: 8px;
    padding: 1.2rem 1.6rem;
    margin: 1.2rem 0;
}
.verdict-bad {
    background: linear-gradient(135deg, #2e0d0d 0%, #331010 100%);
    border: 1px solid #5e1a1a;
    border-left: 4px solid #ef4444;
    border-radius: 8px;
    padding: 1.2rem 1.6rem;
    margin: 1.2rem 0;
}
.verdict-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.verdict-good .verdict-label { color: #22c55e; }
.verdict-bad .verdict-label { color: #ef4444; }
.verdict-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.3rem;
}
.verdict-detail {
    font-size: 0.82rem;
    color: #8a9ab5;
    line-height: 1.5;
}

/* ── Section titles ── */
.section-title {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #4a9eff;
    margin: 2rem 0 0.8rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #1e2940;
}

/* ── Sensitivity table ── */
.sensitivity-note {
    font-size: 0.73rem;
    color: #4a5570;
    margin-top: 0.5rem;
    font-style: italic;
}

/* ── Return badge ── */
.return-badge {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.4rem;
    font-weight: 700;
    padding: 0.6rem 1.2rem;
    border-radius: 6px;
    margin: 0.5rem 0;
}
.return-good { background: #0d2e1f; color: #22c55e; border: 1px solid #1a5e38; }
.return-bad  { background: #2e0d0d; color: #ef4444; border: 1px solid #5e1a1a; }

/* ── Divider ── */
.gg-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #2a3550 30%, #2a3550 70%, transparent);
    margin: 1.8rem 0;
}

/* ── Streamlit element overrides ── */
.stTextInput > div > div > input {
    background-color: #1a2035;
    border: 1px solid #2e3a54;
    color: #e8eaf0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 1rem;
    border-radius: 6px;
    letter-spacing: 0.05em;
}
.stTextInput > div > div > input:focus {
    border-color: #4a9eff;
    box-shadow: 0 0 0 2px rgba(74,158,255,0.15);
}
.stButton > button {
    background-color: #4a9eff;
    color: #000;
    font-weight: 600;
    font-size: 0.82rem;
    letter-spacing: 0.06em;
    border: none;
    border-radius: 6px;
    padding: 0.45rem 1.4rem;
}
.stButton > button:hover {
    background-color: #6ab4ff;
}
div[data-testid="stDataFrame"] {
    border-radius: 8px;
    overflow: hidden;
}
.stSlider > div > div {
    color: #e8eaf0;
}
.stNumberInput > div > div > input {
    background-color: #1a2035;
    border: 1px solid #2e3a54;
    color: #e8eaf0;
    font-family: 'JetBrains Mono', monospace;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# UTILITY FUNCTIONS
# ─────────────────────────────────────────────

def crores(value: float) -> float:
    """Convert raw rupee value → crores."""
    return value / 1e7


def fmt_crores(value: float, decimals: int = 0) -> str:
    """Format a crore value with commas and ₹ symbol."""
    if value >= 1e5:
        return f"₹{value/1e5:,.2f}L Cr"
    return f"₹{value:,.{decimals}f} Cr"


def pct(value: float) -> str:
    return f"{value*100:.1f}%"


@st.cache_data(ttl=300, show_spinner=False)
def fetch_stock_data(ticker: str):
    """
    Fetch fundamentals and 2-year price history from yfinance.
    Returns a dict of core fields or raises on failure.
    """
    t = yf.Ticker(ticker)
    info = t.info

    # Validate the ticker returned something meaningful
    if not info or info.get("regularMarketPrice") is None:
        raise ValueError(f"No data found for ticker '{ticker}'. Check the symbol and try again.")

    # Current share price
    price = info.get("currentPrice") or info.get("regularMarketPrice") or info.get("previousClose")

    # Market cap in crores (raw value is in ₹ for Indian equities)
    market_cap_raw = info.get("marketCap", 0)
    market_cap_cr  = crores(market_cap_raw) if market_cap_raw else None

    # Last year's revenue in crores
    revenue_raw = info.get("totalRevenue", 0)
    revenue_cr  = crores(revenue_raw) if revenue_raw else None

    # 2-year historical OHLCV
    hist = t.history(period="2y", interval="1d", auto_adjust=True)

    return {
        "ticker":       ticker.upper(),
        "name":         info.get("longName") or info.get("shortName", ticker),
        "sector":       info.get("sector", ""),
        "industry":     info.get("industry", ""),
        "price":        price,
        "market_cap":   market_cap_cr,
        "revenue":      revenue_cr,
        "currency":     info.get("currency", "INR"),
        "history":      hist,
        "info":         info,
    }


# ─────────────────────────────────────────────
# CORE VALUATION ENGINE  (mirrors the Excel model)
# ─────────────────────────────────────────────

def run_valuation(last_sales, market_cap, growth_rate, terminal_multiple,
                  desired_return, hold_years):
    """
    Replicates GrowGuru_Valuation_Model_2.xlsx cell-for-cell.

    Parameters
    ----------
    last_sales         : float   Last year's total revenue (₹ Cr)
    market_cap         : float   Current market cap (₹ Cr)
    growth_rate        : float   Expected annual sales CAGR  (e.g. 0.20)
    terminal_multiple  : float   Price-to-Sales multiple at exit (e.g. 5)
    desired_return     : float   Hurdle rate / wanted CAGR    (e.g. 0.15)
    hold_years         : int     Investment horizon in years   (e.g. 10)

    Returns
    -------
    dict with all intermediate and final figures
    """
    # ── Projected Sales ─────────────────────────────────────────────────────
    projected_sales = last_sales * (1 + growth_rate) ** hold_years          # row "Sales after N years"

    # ── Future Company Worth ─────────────────────────────────────────────────
    future_worth = projected_sales * terminal_multiple                        # row "Company worth after N years"

    # ── Fair Value Today (DCF to present at desired return) ──────────────────
    fair_value_today = future_worth / (1 + desired_return) ** hold_years     # row "What it should cost today"

    # ── Actual Yearly Return at current price ────────────────────────────────
    actual_return = (future_worth / market_cap) ** (1 / hold_years) - 1     # row "Your yearly return"

    # ── Valuation verdict ────────────────────────────────────────────────────
    pct_diff = (market_cap - fair_value_today) / fair_value_today            # positive → overpaying
    overpaying = market_cap > fair_value_today

    return {
        "projected_sales":  projected_sales,
        "future_worth":     future_worth,
        "fair_value_today": fair_value_today,
        "actual_return":    actual_return,
        "pct_diff":         pct_diff,
        "overpaying":       overpaying,
    }


def build_sensitivity_table(last_sales, market_cap, terminal_multiple,
                             desired_return, hold_years,
                             growth_range=(0.10, 0.15, 0.20, 0.25, 0.30)):
   """
    Mirrors the "WHAT IF GROWTH IS FASTER OR SLOWER?" section of the Excel.
    Returns a styled DataFrame with green/red conditional formatting.
    """
    rows = []
    for g in growth_range:
        v = run_valuation(last_sales, market_cap, g, terminal_multiple,
                          desired_return, hold_years)
        rows.append({
            "Growth Rate": f"{g*100:.0f}%",
            "Projected Sales (₹ Cr)": round(v["projected_sales"], 0),
            "Future Worth (₹ Cr)":    round(v["future_worth"],    0),
            "Fair Value Today (₹ Cr)":round(v["fair_value_today"],0),
            "vs. Market Cap":         "MORE ↑" if v["overpaying"] else "LESS ↓",
            "_overpaying":            v["overpaying"],
            "_diff":                  v["pct_diff"],
        })

    df = pd.DataFrame(rows)

    # 1. Calculate Fair Share Price mathematically before adding commas
    df["Fair Share Price (₹)"] = data["price"] * (df["Fair Value Today (₹ Cr)"] / data["market_cap"])

    # 2. Format large number columns with commas (no decimals)
    for col in ["Projected Sales (₹ Cr)", "Future Worth (₹ Cr)", "Fair Value Today (₹ Cr)"]:
        df[col] = df[col].apply(lambda x: f"₹{x:,.0f}")

    # 3. Format the Fair Share Price with commas and 2 decimals
    df["Fair Share Price (₹)"] = df["Fair Share Price (₹)"].apply(lambda x: f"₹{x:,.2f}")

    # 4. Add % diff column
    df["Over/Under"] = df["_diff"].apply(lambda x: f"+{x*100:.1f}%" if x > 0 else f"{x*100:.1f}%")

    # 5. Insert "Fair Share Price (₹)" into the final display layout
    display_df = df[["Growth Rate", "Projected Sales (₹ Cr)", "Future Worth (₹ Cr)",
                     "Fair Value Today (₹ Cr)", "Fair Share Price (₹)", "vs. Market Cap", "Over/Under"]].copy()

    # 6. Cleaned up color_row function mapping to your dark-mode colors
    def color_row(row):
        overpaying = df.loc[row.name, "_overpaying"]
        if overpaying:
            # Leaves first 3 columns blank, highlights the last 4 columns in red
            return ["", "", ""] + ["background-color:#2e0d0d;color:#ef4444"] * 4
        else:
            # Leaves first 3 columns blank, highlights the last 4 columns in green
            return ["", "", ""] + ["background-color:#0d2e1f;color:#22c55e"] * 4

    # 7. Apply your custom dark-mode table styling
    styled = display_df.style.apply(color_row, axis=1).set_properties(**{
        "background-color": "#161b27",
        "color": "#c9cfe0",
        "border": "1px solid #232a3b",
        "font-family": "JetBrains Mono, monospace",
        "font-size": "0.82rem",
        "text-align": "center",
    }).set_table_styles([
        {"selector": "th",
         "props": [("background-color", "#0f1520"),
                   ("color", "#7b8cad"),
                   ("font-size", "0.7rem"),
                   ("letter-spacing", "0.08em"),
                   ("border", "1px solid #232a3b"),
                   ("padding", "8px 12px")]},
        {"selector": "td",
         "props": [("padding", "8px 12px"),
                   ("border", "1px solid #1e2535")]},
    ])

    return styled

def build_price_chart(history: pd.DataFrame, ticker: str):
    """
    Plotly chart: 2-year closing price + 50/200-day SMAs.
    """
    df = history.copy()
    df["SMA50"]  = df["Close"].rolling(50).mean()
    df["SMA200"] = df["Close"].rolling(200).mean()

    fig = go.Figure()

    # Price area fill
    fig.add_trace(go.Scatter(
        x=df.index, y=df["Close"],
        name="Close Price",
        line=dict(color="#4a9eff", width=1.5),
        fill="tozeroy",
        fillcolor="rgba(74,158,255,0.06)",
        hovertemplate="<b>%{x|%d %b %Y}</b><br>₹%{y:,.2f}<extra></extra>",
    ))

    # SMA 50
    fig.add_trace(go.Scatter(
        x=df.index, y=df["SMA50"],
        name="50-Day SMA",
        line=dict(color="#f59e0b", width=1.4, dash="dot"),
        hovertemplate="SMA50: ₹%{y:,.2f}<extra></extra>",
    ))

    # SMA 200
    fig.add_trace(go.Scatter(
        x=df.index, y=df["SMA200"],
        name="200-Day SMA",
        line=dict(color="#a855f7", width=1.4, dash="dash"),
        hovertemplate="SMA200: ₹%{y:,.2f}<extra></extra>",
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#8a9ab5"),
        margin=dict(l=0, r=0, t=10, b=0),
        height=340,
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="left",   x=0,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11, color="#8a9ab5"),
        ),
        xaxis=dict(
            gridcolor="#1e2535",
            showline=False,
            tickfont=dict(size=11),
        ),
        yaxis=dict(
            gridcolor="#1e2535",
            showline=False,
            tickfont=dict(size=11),
            tickprefix="₹",
        ),
        hovermode="x unified",
    )

    return fig


# ─────────────────────────────────────────────
# SESSION STATE INITIALISATION
# ─────────────────────────────────────────────
if "stock_data" not in st.session_state:
    st.session_state.stock_data = None
if "ticker_input" not in st.session_state:
    st.session_state.ticker_input = ""


# ─────────────────────────────────────────────
# SIDEBAR — Settings & Controls
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-section">ValuePulse</div>', unsafe_allow_html=True)
    st.markdown("**Fundamental Valuation Analyzer**")
    st.markdown("<small style='color:#4a5570'>All values in ₹ Crore · Indian equities focus</small>", unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Model Settings</div>', unsafe_allow_html=True)

    # 1. Expected Sales Growth Rate Slider
    growth_rate_pct = st.slider(
        "Expected Sales Growth Rate",
        min_value=1, max_value=50, value=20, step=1,
        format="%d%%",
        help="How fast you expect the company's revenue to grow per year. Default: 20%"
    )
    growth_rate = growth_rate_pct / 100.0

    # 2. Terminal Sales Multiple Slider
    terminal_multiple = st.slider(
        "Terminal Sales Multiple (P/S)",
        min_value=1.0, max_value=20.0, value=5.0, step=0.5,
        format="%.1fx",
        help="How many times its annual sales the company will be worth at exit. Default: 5×"
    )

    # 3. Desired Yearly Return Slider
    desired_return_pct = st.slider(
        "Desired Yearly Return",
        min_value=5, max_value=40, value=15, step=1,
        format="%d%%",
        help="The minimum annual return you want to earn. Default: 15%"
    )
    desired_return = desired_return_pct / 100.0

    hold_years = st.slider(
        "Years to Hold",
        min_value=1, max_value=30, value=10, step=1,
        format="%d yrs",
        help="How many years you plan to hold the stock. Default: 10"
    )

    st.markdown('<div class="sidebar-section">Sensitivity Range</div>', unsafe_allow_html=True)
    sens_min = st.number_input("Min Growth %", value=10, min_value=1, max_value=49, step=5)
    sens_max = st.number_input("Max Growth %", value=30, min_value=2, max_value=50, step=5)
    sens_step= st.number_input("Step %", value=5, min_value=1, max_value=10, step=1)

    sensitivity_range = [
        round(x / 100, 2)
        for x in range(int(sens_min), int(sens_max) + 1, int(sens_step))
    ]

    st.markdown('<div class="sidebar-section">About</div>', unsafe_allow_html=True)
    st.markdown("""
    <small style='color:#4a5570;line-height:1.7'>
    This model estimates intrinsic value by projecting future revenue, 
    applying a terminal multiple, and discounting back at your desired return.
    <br><br>
    This is a <b style='color:#7b8cad'>learning tool</b>, not financial advice.
    Always do your own research.
    </small>
    """, unsafe_allow_html=True)
    
# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <span class="brand-name">STOCK</span>
  <span class="brand-tag">Valuation Analyzer</span>
</div>
<p class="tagline">Enter a ticker → get fundamentals auto-filled → see if you're paying too much.</p>
""", unsafe_allow_html=True)

import requests

# ── Ticker Search ──────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([4, 1])

with col_input:
    st.markdown('<div class="ticker-label">Search Indian Company Name or Ticker</div>', unsafe_allow_html=True)
    
    # 1. User types part of the company name (e.g., "Reliance" or "Tata")
    search_query = st.text_input(
        label="search",
        placeholder="e.g. Reliance, Tata Motors, Wipro...",
        label_visibility="collapsed",
    )
    
    # 2. Fetch live autocomplete suggestions dynamically
    suggestions = []
    if search_query.strip():
        # Securely hit Yahoo's internal search API
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={search_query.strip()}"
        headers = {'User-Agent': 'Mozilla/5.0'} 
        try:
            res = requests.get(url, headers=headers).json()
            # Filter specifically for Indian markets (.NS for NSE, .BO for BSE)
            for q in res.get('quotes', []):
                sym = q.get('symbol', '')
                if sym.endswith('.NS') or sym.endswith('.BO'):
                    name = q.get('longname') or q.get('shortname') or 'Unknown'
                    suggestions.append(f"{sym}  |  {name}")
        except Exception:
            pass

    # 3. Create a dropdown if we found matches, or auto-append .NS if not
    ticker_raw = ""
    if suggestions:
        selected_option = st.selectbox("Select the exact company:", suggestions)
        # Extract just the ticker (e.g. "RELIANCE.NS" from "RELIANCE.NS | Reliance Industries")
        ticker_raw = selected_option.split("  |  ")[0]
    elif search_query.strip():
        # Fallback: If they type a raw ticker like "TCS" and hit enter, auto-add .NS
        ticker_raw = search_query.strip().upper()
        if not ticker_raw.endswith(".NS") and not ticker_raw.endswith(".BO"):
            ticker_raw += ".NS"

with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_clicked = st.button("Analyze →", use_container_width=True)

# ── Fetch data on button click ─────────────────────────────────────────────────
if analyze_clicked and ticker_raw:
    with st.spinner(f"Fetching data for **{ticker_raw}** …"):
        try:
            st.session_state.stock_data = fetch_stock_data(ticker_raw)
            st.session_state.ticker_input = ticker_raw
        except Exception as e:
            st.error(f"⚠️ {e}")
            st.session_state.stock_data = None

# ── No data state ──────────────────────────────────────────────────────────────
if st.session_state.stock_data is None:
    st.markdown("""
    <div style="margin-top:3rem;text-align:center;color:#2e3a54;">
        <div style="font-size:2.5rem;margin-bottom:0.6rem;">📊</div>
        <div style="font-size:1rem;color:#3a4a6a;font-weight:500">
            Search for an Indian company above and press <b style="color:#4a9eff">Analyze →</b>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────
# DATA LOADED — Render the full analysis
# ─────────────────────────────────────────────
data = st.session_state.stock_data

# Validate completeness
missing = []
if data["price"] is None:       missing.append("current share price")
if data["market_cap"] is None:  missing.append("market cap")
if data["revenue"] is None:     missing.append("revenue")

if missing:
    st.warning(
        f"⚠️ Could not retrieve: **{', '.join(missing)}** for `{data['ticker']}`. "
        "yfinance may not have complete data for this ticker. "
        "You can enter the missing values below."
    )

# ── Company Header ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="company-display">
  <div class="co-name">🏢 {data['name']} &nbsp;<code style="font-size:0.75rem;color:#4a9eff">{data['ticker']}</code></div>
  <div class="co-sector">{data['sector']} · {data['industry']}</div>
</div>
""", unsafe_allow_html=True)

# ── Editable Data Fields ───────────────────────────────────────────────────────
st.markdown('<div class="section-title">📥 Auto-Filled Data (editable)</div>', unsafe_allow_html=True)
st.markdown(
    "<small style='color:#4a5570'>Fields are pre-filled from live market data. "
    "Override any value if you have a different source.</small><br><br>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    share_price = st.number_input(
        "Current Share Price (₹)",
        value=float(data["price"]) if data["price"] else 0.0,
        min_value=0.0, step=1.0, format="%.2f",
        help="Auto-filled from yfinance. Edit if stale."
    )
with col2:
    market_cap = st.number_input(
        "Market Cap (₹ Cr)",
        value=float(round(data["market_cap"])) if data["market_cap"] else 0.0,
        min_value=0.0, step=100.0, format="%.0f",
        help="Auto-filled from yfinance. Edit if stale."
    )
with col3:
    last_sales = st.number_input(
        "Last Year's Revenue (₹ Cr)",
        value=float(round(data["revenue"])) if data["revenue"] else 0.0,
        min_value=0.0, step=100.0, format="%.0f",
        help="Auto-filled from yfinance. Edit if stale."
    )

# Guard: can't run model without core numbers
if market_cap <= 0 or last_sales <= 0:
    st.info("ℹ️ Enter Market Cap and Revenue above to run the valuation.")
    st.stop()

# ─────────────────────────────────────────────
# RUN VALUATION MODEL
# ─────────────────────────────────────────────
v = run_valuation(
    last_sales=last_sales,
    market_cap=market_cap,
    growth_rate=growth_rate,
    terminal_multiple=terminal_multiple,
    desired_return=desired_return,
    hold_years=hold_years,
)

st.markdown('<div class="gg-divider"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SECTION 1 — FUTURE WORTH
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">📈 What The Company Will Be Worth Later</div>', unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f"""
    <div class="metric-card">
      <div class="mc-label">Sales Today</div>
      <div class="mc-value">{fmt_crores(last_sales)}</div>
      <div class="mc-sub">Last reported annual revenue</div>
    </div>""", unsafe_allow_html=True)
with m2:
    st.markdown(f"""
    <div class="metric-card">
      <div class="mc-label">Projected Sales in {hold_years}Y</div>
      <div class="mc-value">{fmt_crores(v['projected_sales'])}</div>
      <div class="mc-sub">@ {pct(growth_rate)} CAGR</div>
    </div>""", unsafe_allow_html=True)
with m3:
    st.markdown(f"""
    <div class="metric-card">
      <div class="mc-label">Future Company Worth</div>
      <div class="mc-value">{fmt_crores(v['future_worth'])}</div>
      <div class="mc-sub">{terminal_multiple}× terminal sales multiple</div>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SECTION 2 — VALUATION VERDICT
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">⚖️ Are You Paying Too Much Right Now?</div>', unsafe_allow_html=True)

c_left, c_right = st.columns([3, 2])

with c_left:
    fv_col, mc_col = st.columns(2)
    with fv_col:
        st.markdown(f"""
        <div class="metric-card">
          <div class="mc-label">Fair Value Today</div>
          <div class="mc-value">{fmt_crores(v['fair_value_today'])}</div>
          <div class="mc-sub">Discounted at {pct(desired_return)}/yr over {hold_years}Y</div>
        </div>""", unsafe_allow_html=True)
    with mc_col:
        st.markdown(f"""
        <div class="metric-card">
          <div class="mc-label">Current Market Cap</div>
          <div class="mc-value">{fmt_crores(market_cap)}</div>
          <div class="mc-sub">What the market charges today</div>
        </div>""", unsafe_allow_html=True)

    # Verdict banner
    pct_diff_abs = abs(v["pct_diff"]) * 100
    if v["overpaying"]:
        direction_word = "MORE"
        st.markdown(f"""
        <div class="verdict-bad">
          <div class="verdict-label">🔴 Valuation Verdict</div>
          <div class="verdict-title">You're paying TOO MUCH</div>
          <div class="verdict-detail">
            The market cap is <b style="color:#ef4444">{pct_diff_abs:.1f}% MORE</b> than 
            the fair value today ({fmt_crores(v['fair_value_today'])}). 
            At this price you earn less than your {pct(desired_return)} target.
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        direction_word = "LESS"
        st.markdown(f"""
        <div class="verdict-good">
          <div class="verdict-label">🟢 Valuation Verdict</div>
          <div class="verdict-title">You're getting a GOOD PRICE</div>
          <div class="verdict-detail">
            The market cap is <b style="color:#22c55e">{pct_diff_abs:.1f}% LESS</b> than 
            the fair value today ({fmt_crores(v['fair_value_today'])}). 
            At this price you beat your {pct(desired_return)} target.
          </div>
        </div>""", unsafe_allow_html=True)

with c_right:
    st.markdown('<div class="section-title" style="margin-top:0">📊 Your Actual Yearly Return</div>', unsafe_allow_html=True)
    return_class = "return-good" if v["actual_return"] >= desired_return else "return-bad"
    comparison   = "≥" if v["actual_return"] >= desired_return else "<"
    st.markdown(f"""
    <div class="metric-card" style="text-align:center;padding:1.4rem;">
      <div class="mc-label">If you buy at today's market cap</div>
      <div class="return-badge {return_class}">{v['actual_return']*100:.2f}% / yr</div>
      <div class="mc-sub" style="margin-top:0.4rem">
        {comparison} your target of <b>{pct(desired_return)}</b><br>
        over {hold_years} years
      </div>
    </div>
    <br>
    <div class="metric-card">
      <div class="mc-label">Capital Invested</div>
      <div class="mc-value">{fmt_crores(market_cap)}</div>
      <div class="mc-sub">Today's market cap</div>
    </div>
    <br>
    <div class="metric-card">
      <div class="mc-label">Worth After {hold_years} Years</div>
      <div class="mc-value">{fmt_crores(v['future_worth'])}</div>
      <div class="mc-sub">At {pct(growth_rate)} revenue growth · {terminal_multiple}× PS</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="gg-divider"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SECTION 3 — SENSITIVITY MATRIX
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">🎛️ What If Growth Is Faster Or Slower?</div>', unsafe_allow_html=True)
st.markdown(
    "<small style='color:#4a5570'>Adjust the Sensitivity Range in the sidebar. "
    "Green = fair value > market cap (good price). Red = paying too much.</small>",
    unsafe_allow_html=True
)

if len(sensitivity_range) < 2:
    st.warning("Sensitivity range too narrow — increase the range or decrease the step.")
else:
    styled_table = build_sensitivity_table(
        last_sales=last_sales,
        market_cap=market_cap,
        terminal_multiple=terminal_multiple,
        desired_return=desired_return,
        hold_years=hold_years,
        growth_range=sensitivity_range,
    )
    st.dataframe(styled_table, use_container_width=True, hide_index=True)
    st.markdown(
        "<p class='sensitivity-note'>Fair Value Today is what the market cap "
        "would need to be for you to earn exactly your desired yearly return.</p>",
        unsafe_allow_html=True
    )

st.markdown('<div class="gg-divider"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SECTION 4 — TECHNICAL ANALYSIS CHART
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">📉 Price History & Moving Averages (2 Years)</div>', unsafe_allow_html=True)
st.markdown(
    "<small style='color:#4a5570'>"
    "50-day SMA (amber) tracks medium-term momentum. "
    "200-day SMA (violet) is the long-term trend baseline. "
    "Price above 200-day SMA generally indicates bullish momentum.</small><br>",
    unsafe_allow_html=True
)

hist = data.get("history")
if hist is not None and len(hist) > 60:
    fig = build_price_chart(hist, data["ticker"])
    st.plotly_chart(fig, use_container_width=True)

    # Quick SMA interpretation
    latest_close  = hist["Close"].iloc[-1]
    sma50_latest  = hist["Close"].rolling(50).mean().iloc[-1]
    sma200_latest = hist["Close"].rolling(200).mean().iloc[-1]

    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown(f"""
        <div class="metric-card">
          <div class="mc-label">Latest Close</div>
          <div class="mc-value">₹{latest_close:,.2f}</div>
        </div>""", unsafe_allow_html=True)
    with t2:
        above50 = latest_close > sma50_latest
        st.markdown(f"""
        <div class="metric-card">
          <div class="mc-label">vs 50-Day SMA</div>
          <div class="mc-value" style="color:{'#22c55e' if above50 else '#ef4444'}">
            {'▲' if above50 else '▼'} ₹{sma50_latest:,.2f}
          </div>
          <div class="mc-sub">Price is {'above' if above50 else 'below'} 50-day average</div>
        </div>""", unsafe_allow_html=True)
    with t3:
        above200 = latest_close > sma200_latest
        st.markdown(f"""
        <div class="metric-card">
          <div class="mc-label">vs 200-Day SMA</div>
          <div class="mc-value" style="color:{'#22c55e' if above200 else '#ef4444'}">
            {'▲' if above200 else '▼'} ₹{sma200_latest:,.2f}
          </div>
          <div class="mc-sub">Price is {'above' if above200 else 'below'} 200-day average</div>
        </div>""", unsafe_allow_html=True)
else:
    st.info("ℹ️ Not enough historical data to plot moving averages (need > 60 trading days).")

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown('<div class="gg-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;font-size:0.7rem;color:#2e3a54;padding-bottom:1.5rem;">
  GrowGuru Valuation Analyzer · Built for long-term investors · 
  Data via <b style="color:#3a4a6a">yfinance</b> · 
  Not financial advice — always do your own research.
</div>
""", unsafe_allow_html=True)
st.markdown("---")
st.caption("**Disclaimer:** This application is for educational and informational purposes only. It does not constitute financial, investment, or trading advice. The valuations are based on mathematical models and public data, which may be inaccurate or delayed. Always consult with a registered financial advisor before making investment decisions.")
