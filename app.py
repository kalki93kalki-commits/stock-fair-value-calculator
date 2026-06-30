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

# --- NEW: UPGRADED SCREENER.IN SCRAPER ---
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_shareholding_pattern(ticker):
    """
    Custom Scraper with stealth headers to bypass bot-blocks.
    Fetches the last 4 quarters of shareholding data.
    """
    import requests
    import pandas as pd
    
    clean_ticker = ticker.replace(".NS", "").replace(".BO", "")
    # Check both URL structures just in case
    urls = [
        f"https://www.screener.in/company/{clean_ticker}/consolidated/",
        f"https://www.screener.in/company/{clean_ticker}/"
    ]
    
    # Stealth headers to mimic a real human browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    for url in urls:
        try:
            res = requests.get(url, headers=headers, timeout=8)
            if res.status_code != 200:
                continue
                
            tables = pd.read_html(res.text)
            for df in tables:
                if df.empty or len(df.columns) < 2:
                    continue
                # Identify the correct shareholding table
                if df.iloc[:, 0].astype(str).str.contains('Promoters').any():
                    df.set_index(df.columns[0], inplace=True)
                    df.index.name = "Category"
                    df.dropna(how='all', inplace=True)
                    # Return only the last 4 quarters
                    if len(df.columns) >= 4:
                        return df.iloc[:, -4:]
                    else:
                        return df
        except Exception:
            continue
            
    return None
# ---------------------------------------
# ---------------------------------------

@st.cache_data(ttl=300, show_spinner=False)
def fetch_stock_data(ticker: str):
    """
    Fetch fundamentals and maximum price history from yfinance.
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

    # All-year historical OHLCV (Needed for the time-range buttons and P/E chart)
    hist = t.history(period="max", interval="1d", auto_adjust=True)
    
    # --- NEW: Safely fetch full statements and mutual fund data ---
    # 1. Pre-define them as None so Python doesn't panic if data is missing
    financials = balance_sheet = cashflow = mf_holders = None
    
    try:
        financials = t.financials
        balance_sheet = t.balance_sheet
        cashflow = t.cashflow
        mf_holders = t.mutualfund_holders # <-- Fetches the mutual fund data
        news = t.news
    except:
        pass

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
        # Use the safe local variables here, NOT t.financials
        "financials":   financials, 
        "balance_sheet": balance_sheet, 
        "cashflow":      cashflow,      
        "mf_holders":    mf_holders,
        "news":          news,
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
    df["Fair Share Price (₹)"] = data["price"] * (df["Fair Value Today (₹ Cr)"] / market_cap)

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

def calculate_reverse_dcf(market_cap, last_sales, terminal_multiple, desired_return, hold_years):
    """
    Works backward from the current Market Cap to find the exact growth rate
    the market is pricing into the stock.
    """
    if last_sales <= 0 or market_cap <= 0:
        return 0, 0
        
    required_future_worth = market_cap * ((1 + desired_return) ** hold_years)
    required_sales = required_future_worth / terminal_multiple
    implied_growth = (required_sales / last_sales) ** (1 / hold_years) - 1
    
    return implied_growth, required_sales
    
def calculate_f_score(financials, balance_sheet, cashflow):
    """
    Calculates the complete 8-point Piotroski F-Score with dynamic text.
    """
    try:
        if financials is None or balance_sheet is None or cashflow is None or financials.empty or balance_sheet.empty or cashflow.empty:
            return None, "Missing financial statements.", "#5a6a8a", []

        score = 0
        details = []

        def get_val(df, row_names, col_idx):
            for r in row_names:
                if r in df.index:
                    cols = df.columns
                    if len(cols) > col_idx:
                        val = df.loc[r, cols[col_idx]]
                        if pd.notna(val): return val
            return 0
            
        def add_detail(name, passed, desc):
            details.append({"name": name, "passed": passed, "desc": desc})
            return 1 if passed else 0

        # Current Year (0) and Prior Year (1) Data
        net_income = get_val(financials, ['Net Income'], 0)
        net_income_py = get_val(financials, ['Net Income'], 1)
        cfo = get_val(cashflow, ['Operating Cash Flow', 'Total Cash From Operating Activities'], 0)
        
        total_assets = get_val(balance_sheet, ['Total Assets'], 0)
        total_assets_py = get_val(balance_sheet, ['Total Assets'], 1)
        total_assets_ppy = get_val(balance_sheet, ['Total Assets'], 2)
        
        avg_assets = (total_assets + total_assets_py) / 2 if total_assets_py else total_assets
        avg_assets_py = (total_assets_py + total_assets_ppy) / 2 if total_assets_ppy else total_assets_py

        # 1. Profitability: Positive ROA
        roa = net_income / avg_assets if avg_assets else 0
        score += add_detail("Positive Return on Assets", roa > 0, 
                            "Generating positive net income from assets." if roa > 0 else "Failing to generate positive net income from assets.")

        # 2. Profitability: Positive Operating Cash Flow
        score += add_detail("Positive Operating Cash", cfo > 0, 
                            "Core operations are actively generating cash." if cfo > 0 else "Core operations are burning cash.")

        # 3. Profitability: Increasing ROA
        roa_py = net_income_py / avg_assets_py if avg_assets_py else 0
        score += add_detail("Increasing ROA", roa > roa_py, 
                            "Efficiency of capital deployment improved." if roa > roa_py else "Efficiency of capital deployment declined.")

        # 4. Profitability: Earnings Quality (CFO > Net Income)
        score += add_detail("Strong Earnings Quality", cfo > net_income, 
                            "Cash flow exceeds reported profit (high quality)." if cfo > net_income else "Reported profit exceeds actual cash flow (red flag).")

        # 5. Leverage: Decreasing Long Term Debt Ratio
        lt_debt = get_val(balance_sheet, ['Long Term Debt', 'Total Debt'], 0)
        lt_debt_py = get_val(balance_sheet, ['Long Term Debt', 'Total Debt'], 1)
        lt_ratio = lt_debt / total_assets if total_assets else 0
        lt_ratio_py = lt_debt_py / total_assets_py if total_assets_py else 0
        score += add_detail("Decreasing Debt Ratio", lt_ratio < lt_ratio_py, 
                            "Reliance on debt financing has decreased." if lt_ratio < lt_ratio_py else "Reliance on debt financing has increased.")

        # 6. Liquidity: Increasing Current Ratio
        curr_assets = get_val(balance_sheet, ['Current Assets'], 0)
        curr_liab = get_val(balance_sheet, ['Current Liabilities'], 0)
        curr_assets_py = get_val(balance_sheet, ['Current Assets'], 1)
        curr_liab_py = get_val(balance_sheet, ['Current Liabilities'], 1)
        cr = curr_assets / curr_liab if curr_liab else 0
        cr_py = curr_assets_py / curr_liab_py if curr_liab_py else 0
        score += add_detail("Increasing Current Ratio", cr > cr_py, 
                            "Short-term liquidity to pay bills improved." if cr > cr_py else "Short-term liquidity to pay bills declined.")

        # 7. Efficiency: Increasing Gross Margin
        gross_profit = get_val(financials, ['Gross Profit'], 0)
        revenue = get_val(financials, ['Total Revenue', 'Operating Revenue'], 0)
        gross_profit_py = get_val(financials, ['Gross Profit'], 1)
        revenue_py = get_val(financials, ['Total Revenue', 'Operating Revenue'], 1)
        margin = gross_profit / revenue if revenue else 0
        margin_py = gross_profit_py / revenue_py if revenue_py else 0
        score += add_detail("Expanding Gross Margin", margin > margin_py, 
                            "Profitability on core products increased." if margin > margin_py else "Profitability on core products shrank.")

        # 8. Efficiency: Increasing Asset Turnover
        turnover = revenue / avg_assets if avg_assets else 0
        turnover_py = revenue_py / avg_assets_py if avg_assets_py else 0
        score += add_detail("Increasing Asset Turnover", turnover > turnover_py, 
                            "Generating more sales per unit of assets." if turnover > turnover_py else "Generating fewer sales per unit of assets.")

        # Strict Grading Thresholds
        if score >= 6:
            verdict = "Pristine Balance Sheet (Strong Operations)"
            color = "#059669"
        elif score >= 4:
            verdict = "Average Financial Health (Monitor closely)"
            color = "#d97706"
        else:
            verdict = "Red Flags Detected (Poor Earnings Quality)"
            color = "#e11d48"

        return score, verdict, color, details

    except Exception as e:
        return None, f"Insufficient data: {e}", "#5a6a8a", []

def calculate_cash_conversion_cycle(financials, balance_sheet):
    """
    Calculates DSO, DIO, DPO, and the Cash Conversion Cycle.
    """
    try:
        if financials is None or balance_sheet is None or financials.empty or balance_sheet.empty:
            return None

        def get_val(df, row_names, col_idx=0):
            for r in row_names:
                if r in df.index:
                    cols = df.columns
                    if len(cols) > col_idx:
                        val = df.loc[r, cols[col_idx]]
                        if pd.notna(val): return val
            return 0

        # Pull raw data
        revenue = get_val(financials, ['Total Revenue', 'Operating Revenue'])
        cogs = get_val(financials, ['Cost Of Revenue', 'Cost Of Goods Sold'])
        receivables = get_val(balance_sheet, ['Accounts Receivable', 'Net Receivables'])
        inventory = get_val(balance_sheet, ['Inventory'])
        payables = get_val(balance_sheet, ['Accounts Payable'])

        # Fallbacks for zero-division safety (e.g., Software companies with 0 inventory)
        if revenue == 0: revenue = 1
        if cogs == 0: cogs = revenue * 0.5 # Rough fallback if COGS is missing

        # Calculate metrics
        dso = (receivables / revenue) * 365
        dio = (inventory / cogs) * 365
        dpo = (payables / cogs) * 365
        
        ccc = dso + dio - dpo

        return {"dso": dso, "dio": dio, "dpo": dpo, "ccc": ccc}
    except Exception:
        return None
        
def build_price_chart(history: pd.DataFrame, ticker: str):
    """
    Plotly chart: Historical closing price + 50/200-day SMAs with time selectors.
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
        margin=dict(l=0, r=0, t=75, b=0), # Increased top margin to give room for stacking
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02, # Keeps the legend just above the chart
            xanchor="left",   x=0,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11, color="#8a9ab5"),
        ),
        xaxis=dict(
            gridcolor="#1e2535",
            showline=False,
            tickfont=dict(size=11),
            type="date",
            rangeselector=dict(
                x=0, y=1.16, # Moved to the TOP LEFT, perfectly stacked above the legend
                xanchor="left", yanchor="bottom",
                bgcolor="#161b27", 
                activecolor="#232a3b", 
                font=dict(size=10, color="#8a9ab5"),
                buttons=list([
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(count=2, label="2Y", step="year", stepmode="backward"),
                    dict(count=3, label="3Y", step="year", stepmode="backward"),
                    dict(count=5, label="5Y", step="year", stepmode="backward"),
                    dict(step="all", label="ALL")
                ])
            )
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

def build_pe_chart(history: pd.DataFrame, financials: pd.DataFrame):
    """
    Calculates historical P/E by merging daily prices with annual EPS.
    """
    try:
        if financials is None or financials.empty:
            return None, None, None
            
        # 1. Find the Earnings Per Share (EPS) row
        eps_row = None
        for row in ['Diluted EPS', 'Basic EPS']:
            if row in financials.index:
                eps_row = financials.loc[row]
                break
                
        if eps_row is None or eps_row.isna().all():
            return None, None, None
            
        # 2. Format EPS data dates
        eps_df = eps_row.dropna().reset_index()
        eps_df.columns = ['Date', 'EPS']
        eps_df['Date'] = pd.to_datetime(eps_df['Date']).dt.tz_localize(None)
        eps_df = eps_df.sort_values('Date')
        
        # 3. Format Price data dates
        price_df = history[['Close']].copy().reset_index()
        price_df['Date'] = pd.to_datetime(price_df['Date']).dt.tz_localize(None)
        price_df = price_df.sort_values('Date')
        
        # 4. Merge daily prices with the most recent EPS available on that day
        merged = pd.merge_asof(price_df, eps_df, on='Date', direction='backward')
        merged = merged.dropna()
        
        if merged.empty:
            return None, None, None
            
        # 5. Calculate P/E
        merged['PE'] = merged['Close'] / merged['EPS']
        
        # Filter out negative earnings and extreme outliers to keep chart readable
        merged = merged[(merged['PE'] > 0) & (merged['PE'] < 250)]
        
        if merged.empty:
            return None, None, None
            
        median_pe = merged['PE'].median()
        current_pe = merged['PE'].iloc[-1]
        
        # 6. Build Plotly Chart
        fig = go.Figure()
        
        # The P/E Line
        fig.add_trace(go.Scatter(
            x=merged['Date'], y=merged['PE'],
            name="Trailing P/E",
            line=dict(color="#10b981", width=1.5), 
            fill="tozeroy",
            fillcolor="rgba(16, 185, 129, 0.08)",
            hovertemplate="<b>%{x|%d %b %Y}</b><br>P/E: %{y:.1f}x<extra></extra>",
        ))
        
        # The Median Target Line
        fig.add_hline(
            y=median_pe, 
            line_dash="dash", 
            line_color="#f59e0b", 
            annotation_text=f"Historical Median: {median_pe:.1f}x",
            annotation_position="top left",
            annotation_font_color="#f59e0b"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color="#8a9ab5"),
            margin=dict(l=0, r=0, t=75, b=0),
            height=320,
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
                type="date",
                rangeselector=dict(
                    x=0, y=1.16,
                    xanchor="left", yanchor="bottom",
                    bgcolor="#161b27", 
                    activecolor="#232a3b", 
                    font=dict(size=10, color="#8a9ab5"),
                    buttons=list([
                        dict(count=1, label="1Y", step="year", stepmode="backward"),
                        dict(count=2, label="2Y", step="year", stepmode="backward"),
                        dict(count=3, label="3Y", step="year", stepmode="backward"),
                        dict(count=5, label="5Y", step="year", stepmode="backward"),
                        dict(step="all", label="ALL")
                    ])
                )
            ),
            yaxis=dict(
                gridcolor="#1e2535",
                showline=False,
                tickfont=dict(size=11),
                ticksuffix="x",
            ),
            hovermode="x unified",
        )
        
        return fig, current_pe, median_pe
    except Exception:
        return None, None, None

def build_pe_chart(history: pd.DataFrame, financials: pd.DataFrame):
    """
    Calculates historical P/E by merging daily prices with annual EPS.
    """
    try:
        if financials is None or financials.empty:
            return None, None, None
            
        # 1. Find the Earnings Per Share (EPS) row
        eps_row = None
        for row in ['Diluted EPS', 'Basic EPS']:
            if row in financials.index:
                eps_row = financials.loc[row]
                break
                
        if eps_row is None or eps_row.isna().all():
            return None, None, None
            
        # 2. Format EPS data dates
        eps_df = eps_row.dropna().reset_index()
        eps_df.columns = ['Date', 'EPS']
        eps_df['Date'] = pd.to_datetime(eps_df['Date']).dt.tz_localize(None)
        eps_df = eps_df.sort_values('Date')
        
        # 3. Format Price data dates
        price_df = history[['Close']].copy().reset_index()
        price_df['Date'] = pd.to_datetime(price_df['Date']).dt.tz_localize(None)
        price_df = price_df.sort_values('Date')
        
        # 4. Merge daily prices with the most recent EPS available on that day
        merged = pd.merge_asof(price_df, eps_df, on='Date', direction='backward')
        merged = merged.dropna()
        
        if merged.empty:
            return None, None, None
            
        # 5. Calculate P/E
        merged['PE'] = merged['Close'] / merged['EPS']
        merged = merged[(merged['PE'] > 0) & (merged['PE'] < 250)]
        
        if merged.empty:
            return None, None, None
            
        median_pe = merged['PE'].median()
        current_pe = merged['PE'].iloc[-1]
        
        # 6. Build Plotly Chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=merged['Date'], y=merged['PE'], name="Trailing P/E", line=dict(color="#10b981", width=1.5), fill="tozeroy", fillcolor="rgba(16, 185, 129, 0.08)"))
        fig.add_hline(y=median_pe, line_dash="dash", line_color="#f59e0b", annotation_text=f"Median: {median_pe:.1f}x")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter", color="#8a9ab5"), height=320, xaxis=dict(gridcolor="#1e2535"), yaxis=dict(gridcolor="#1e2535", ticksuffix="x"), hovermode="x unified")
        
        return fig, current_pe, median_pe
    except Exception:
        return None, None, None

@st.cache_data(ttl=300, show_spinner=False)
def fetch_peer_data(tickers_str):
    """Fetches P/E and ROE for a comma-separated list of peer tickers."""
    tickers = [t.strip().upper() for t in tickers_str.split(',') if t.strip()]
    peer_data = []
    
    for t in tickers:
        if not t.endswith(".NS") and not t.endswith(".BO"):
            t += ".NS"
        try:
            info = yf.Ticker(t).info
            pe = info.get("trailingPE") or info.get("forwardPE") or 0
            roe = info.get("returnOnEquity") or 0
            name = info.get("shortName", t)
            
            if pe > 0 and roe != 0:
                peer_data.append({"Ticker": t, "Name": name, "P/E": pe, "ROE": roe * 100})
        except:
            pass
    return pd.DataFrame(peer_data)

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
        min_value=1, max_value=50, value=10, step=1,
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
    
    # 1. User types part of the company name (e.g., "ask") and hits Enter
    search_query = st.text_input(
        label="search",
        placeholder="e.g. Reliance, Tata Motors, Wipro...",
        label_visibility="collapsed",
    )
    
    # 2. Fetch live autocomplete suggestions dynamically
    suggestions = []
    if search_query.strip():
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={search_query.strip()}"
        headers = {'User-Agent': 'Mozilla/5.0'} 
        try:
            res = requests.get(url, headers=headers).json()
            for q in res.get('quotes', []):
                sym = q.get('symbol', '')
                if sym.endswith('.NS') or sym.endswith('.BO'):
                    name = q.get('longname') or q.get('shortname') or 'Unknown'
                    suggestions.append(f"{sym}  |  {name}")
        except Exception:
            pass

    # 3. Create a dropdown, automatically selecting the top match
    ticker_raw = ""
    if suggestions:
        selected_option = st.selectbox("Matches found (First match auto-selected):", suggestions)
        ticker_raw = selected_option.split("  |  ")[0]
    elif search_query.strip():
        ticker_raw = search_query.strip().upper()
        if not ticker_raw.endswith(".NS") and not ticker_raw.endswith(".BO"):
            ticker_raw += ".NS"

with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_clicked = st.button("Analyze →", use_container_width=True)

# ── Fetch data (AUTOMATICALLY on Enter) ────────────────────────────────────────
# Check what stock is currently loaded on the screen
current_loaded_ticker = None
if st.session_state.stock_data is not None:
    current_loaded_ticker = st.session_state.stock_data.get("ticker")

# Auto-Trigger: Fetch if they clicked the button OR if the selected ticker is new!
if ticker_raw and (analyze_clicked or ticker_raw != current_loaded_ticker):
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
            Search for an Indian company above and press <b style="color:#4a9eff">Enter ↵</b>
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
# ── Company Health Snapshot ───────────────────────────────────────────────────
st.markdown('<div class="section-title" style="margin-top:0;">🩺 Company Health Snapshot</div>', unsafe_allow_html=True)

info = data.get("info", {})

# Safely extract metrics
pe_ratio = info.get("trailingPE") or info.get("forwardPE")
pe_str = f"{pe_ratio:.1f}x" if pe_ratio is not None else "N/A"

profit_margin = info.get("profitMargins")
margin_str = f"{profit_margin * 100:.1f}%" if profit_margin is not None else "N/A"

roe = info.get("returnOnEquity")
roe_str = f"{roe * 100:.1f}%" if roe is not None else "N/A"

div_yield = info.get("dividendYield") or info.get("trailingAnnualDividendYield")
if div_yield is not None:
    div_str = f"{div_yield:.2f}%" if div_yield > 1 else f"{div_yield * 100:.2f}%"
else:
    div_str = "0.00%"

# --- NEW: Debt-to-Equity Calculation ---
debt_to_equity = info.get("debtToEquity")
d_e_str = f"{debt_to_equity / 100:.2f}x" if debt_to_equity is not None else "N/A"

# Create 5 columns now
h1, h2, h3, h4, h5 = st.columns(5)

with h1:
    st.markdown(f'<div class="metric-card"><div class="mc-label">P/E Ratio</div><div class="mc-value">{pe_str}</div></div>', unsafe_allow_html=True)
with h2:
    st.markdown(f'<div class="metric-card"><div class="mc-label">Net Margin</div><div class="mc-value" style="color:#22c55e">{margin_str}</div></div>', unsafe_allow_html=True)
with h3:
    st.markdown(f'<div class="metric-card"><div class="mc-label">ROE</div><div class="mc-value">{roe_str}</div></div>', unsafe_allow_html=True)
with h4:
    st.markdown(f'<div class="metric-card"><div class="mc-label">Div Yield</div><div class="mc-value">{div_str}</div></div>', unsafe_allow_html=True)
with h5:
    st.markdown(f"""
    <div class="metric-card">
      <div class="mc-label">Debt/Equity</div>
      <div class="mc-value" style="color:{'#ef4444' if debt_to_equity and debt_to_equity > 100 else '#22c55e'}">{d_e_str}</div>
      <div class="mc-sub">Safety check</div>
    </div>""", unsafe_allow_html=True)

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
# REVERSE DCF: MARKET EXPECTATIONS
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">🔍 Reverse DCF: What is the market expecting?</div>', unsafe_allow_html=True)

implied_g, req_sales = calculate_reverse_dcf(
    market_cap=market_cap,
    last_sales=last_sales,
    terminal_multiple=terminal_multiple,
    desired_return=desired_return,
    hold_years=hold_years
)

if implied_g > 0.25:
    g_color = "#e11d48" # Muted Rose (High expectation/caution)
    g_text = "The market is pricing in aggressive, high-risk growth."
elif implied_g < 0.12:
    g_color = "#059669" # Soft Emerald (Low bar to clear/value)
    g_text = "The market has set a very low bar for this company."
else:
    g_color = "#6366f1" # Slate Blue (Fair/Standard expectations)
    g_text = "The market expects steady, moderate growth."

r1, r2 = st.columns([1, 1.5])

with r1:
    # Completely left-aligned to prevent Streamlit Markdown spacing bugs
    st.markdown(f"""
<div style="background:#161b27; border:1px solid #232a3b; border-left:4px solid {g_color}; border-radius:8px; padding:1.5rem;">
    <div style="font-size:0.7rem; font-weight:600; letter-spacing:0.1em; color:#8a9ab5; text-transform:uppercase; margin-bottom:0.5rem;">
        Market Implied Growth Rate
    </div>
    <div style="font-family:'JetBrains Mono', monospace; font-size:2.2rem; font-weight:700; color:#e8eaf0; margin-bottom:0.5rem;">
        {implied_g * 100:.1f}% <span style="font-size:1rem; font-weight:400; color:#5a6a8a;">/ yr</span>
    </div>
    <div style="font-size:0.8rem; color:#8a9ab5;">
        {g_text}
    </div>
</div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown(f"""
<div style="background:rgba(30, 41, 59, 0.4); border:1px solid #232a3b; border-radius:8px; padding:1.5rem; height:100%;">
    <div style="font-size:0.85rem; color:#c9cfe0; line-height:1.6;">
        To deliver your <b>{desired_return*100:.0f}%</b> annual return from today's price, 
        this company must grow its revenue from <b>{fmt_crores(last_sales)}</b> today to 
        <b>{fmt_crores(req_sales)}</b> in {hold_years} years.
        <br><br>
        <i>Ask yourself:</i> Is a <b>{implied_g * 100:.1f}%</b> compounding growth rate realistic for this specific business model and industry?
    </div>
</div>
    """, unsafe_allow_html=True)

st.markdown('<div class="gg-divider"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FORENSIC QUALITY RADAR (F-SCORE)
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">🕵️ Forensic Quality Radar (F-Score)</div>', unsafe_allow_html=True)

bs = data.get("balance_sheet")
cf = data.get("cashflow")
fs = data.get("financials")

# Check if data exists AND is not empty
if bs is not None and cf is not None and fs is not None and not bs.empty and not cf.empty:
    f_score, f_verdict, f_color, f_details = calculate_f_score(fs, bs, cf)
    
    if f_score is not None:
        # Full grid HTML logic (No placeholders)
        grid_html = "<div style='display:grid; grid-template-columns:repeat(auto-fit, minmax(250px, 1fr)); gap:0.8rem; margin-top:1.5rem; padding-top:1.5rem; border-top:1px solid #232a3b;'>"
        for d in f_details:
            icon = "✅" if d['passed'] else "❌"
            color = "#22c55e" if d['passed'] else "#ef4444"
            bg_color = "rgba(34, 197, 94, 0.05)" if d['passed'] else "rgba(239, 68, 68, 0.05)"
            
            grid_html += f"<div style='background:{bg_color}; border:1px solid #232a3b; padding:0.8rem; border-radius:6px;'>"
            grid_html += f"<div style='font-size:0.75rem; font-weight:600; color:{color}; margin-bottom:0.2rem;'>{icon} {d['name']}</div>"
            grid_html += f"<div style='font-size:0.7rem; color:#8a9ab5; line-height:1.4;'>{d['desc']}</div>"
            grid_html += "</div>"
            
        grid_html += "</div>"

        # Render the main card + the grid (PUSHED COMPLETELY LEFT TO FIX MARKDOWN BUG)
        st.markdown(f"""
<div style="background:#161b27; border:1px solid #232a3b; border-left:4px solid {f_color}; border-radius:8px; padding:1.5rem;">
    <div style="display:flex; align-items:center; gap:2rem;">
        <div style="text-align:center; min-width:120px;">
            <div style="font-size:0.7rem; font-weight:600; letter-spacing:0.1em; color:#8a9ab5; text-transform:uppercase; margin-bottom:0.3rem;">
                Quality Score
            </div>
            <div style="font-family:'JetBrains Mono', monospace; font-size:2.8rem; font-weight:700; color:{f_color}; line-height:1;">
                {f_score}<span style="font-size:1.2rem; color:#5a6a8a;">/8</span>
            </div>
        </div>
        <div style="border-left:1px solid #232a3b; padding-left:2rem;">
            <div style="font-size:1.2rem; font-weight:600; color:#e8eaf0; margin-bottom:0.4rem;">
                {f_verdict}
            </div>
            <div style="font-size:0.85rem; color:#8a9ab5; line-height:1.5;">
                This score breaks down the underlying health of the business operations, checking if cash is actually flowing, if debt is under control, and if capital is being deployed efficiently.
            </div>
        </div>
    </div>
{grid_html}
</div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Could not generate F-Score: Data retrieved was incomplete.")
else:
    # PROFESSIONAL FALLBACK: Explain the limitation clearly
    st.markdown("""
<div style="background:#161b27; border:1px solid #232a3b; border-radius:8px; padding:1.2rem; color:#8a9ab5;">
    <div style="font-weight:600; color:#4a9eff; margin-bottom:0.3rem;">Data Coverage Note</div>
    <div style="font-size:0.85rem;">
        Advanced forensic metrics (Balance Sheet & Cash Flow) are only available for 
        large-cap companies that maintain consistent digital filings with major exchanges. 
        For this ticker, comprehensive forensic data is currently unavailable.
    </div>
</div>
    """, unsafe_allow_html=True)

st.markdown('<div class="gg-divider"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SHOP-FLOOR EFFICIENCY (CASH CONVERSION CYCLE)
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">⚙️ Operational Efficiency (Cash Conversion Cycle)</div>', unsafe_allow_html=True)
st.markdown(
    "<small style='color:#7b8cad'>"
    "Measures the underlying physical business. How fast does the company clear its inventory, collect cash from customers, and pay its vendors?</small><br><br>",
    unsafe_allow_html=True
)

bs = data.get("balance_sheet")
fs = data.get("financials")

if bs is not None and fs is not None and not bs.empty and not fs.empty:
    ccc_data = calculate_cash_conversion_cycle(fs, bs)
    
    if ccc_data is not None:
        dso, dio, dpo, ccc = ccc_data["dso"], ccc_data["dio"], ccc_data["dpo"], ccc_data["ccc"]
        
        # CCC color logic: Lower is better (negative is incredible)
        if ccc < 0: ccc_color, ccc_status = "#22c55e", "Excellent (Paid by customers before paying vendors)"
        elif ccc < 60: ccc_color, ccc_status = "#059669", "Healthy Operations"
        elif ccc < 120: ccc_color, ccc_status = "#d97706", "Average Cash Cycle"
        else: ccc_color, ccc_status = "#e11d48", "Warning: Capital tied up in operations"

        st.markdown(f"""
<div style="display:flex; gap:1rem; flex-wrap:wrap;">
<div style="flex:1; min-width:300px; background:#161b27; border:1px solid #232a3b; border-left:4px solid {ccc_color}; border-radius:8px; padding:1.5rem;">
<div style="font-size:0.7rem; font-weight:600; letter-spacing:0.1em; color:#8a9ab5; text-transform:uppercase; margin-bottom:0.5rem;">Cash Conversion Cycle</div>
<div style="font-family:'JetBrains Mono', monospace; font-size:2.4rem; font-weight:700; color:#e8eaf0; margin-bottom:0.2rem;">{ccc:.0f} <span style="font-size:1rem; font-weight:400; color:#5a6a8a;">Days</span></div>
<div style="font-size:0.8rem; color:{ccc_color}; font-weight:500;">{ccc_status}</div>
</div>
<div style="flex:2; display:grid; grid-template-columns:repeat(auto-fit, minmax(150px, 1fr)); gap:1rem;">
<div style="background:rgba(30, 41, 59, 0.4); border:1px solid #232a3b; border-radius:8px; padding:1.2rem;">
<div style="font-size:0.7rem; color:#8a9ab5; text-transform:uppercase; margin-bottom:0.3rem;">Inventory Days (DIO)</div>
<div style="font-family:'JetBrains Mono', monospace; font-size:1.4rem; font-weight:600; color:#e8eaf0;">{dio:.0f} <span style="font-size:0.8rem; color:#5a6a8a;">Days</span></div>
<div style="font-size:0.7rem; color:#5a6a8a; margin-top:0.2rem;">Time sitting in warehouse</div>
</div>
<div style="background:rgba(30, 41, 59, 0.4); border:1px solid #232a3b; border-radius:8px; padding:1.2rem;">
<div style="font-size:0.7rem; color:#8a9ab5; text-transform:uppercase; margin-bottom:0.3rem;">Receivable Days (DSO)</div>
<div style="font-family:'JetBrains Mono', monospace; font-size:1.4rem; font-weight:600; color:#e8eaf0;">{dso:.0f} <span style="font-size:0.8rem; color:#5a6a8a;">Days</span></div>
<div style="font-size:0.7rem; color:#5a6a8a; margin-top:0.2rem;">Time to collect from clients</div>
</div>
<div style="background:rgba(30, 41, 59, 0.4); border:1px solid #232a3b; border-radius:8px; padding:1.2rem;">
<div style="font-size:0.7rem; color:#8a9ab5; text-transform:uppercase; margin-bottom:0.3rem;">Payable Days (DPO)</div>
<div style="font-family:'JetBrains Mono', monospace; font-size:1.4rem; font-weight:600; color:#e8eaf0;">{dpo:.0f} <span style="font-size:0.8rem; color:#5a6a8a;">Days</span></div>
<div style="font-size:0.7rem; color:#5a6a8a; margin-top:0.2rem;">Time taken to pay vendors</div>
</div>
</div>
</div>
        """, unsafe_allow_html=True)
    else:
         st.warning("⚠️ Could not calculate operational efficiency: Missing specific line items.")
else:
    st.info("ℹ️ Advanced operational metrics unavailable for this ticker.")

st.markdown('<div class="gg-divider"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# COMPETITOR MATRIX (QUALITY VS. PRICE)
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">⚔️ The Compounding Engine vs. Value Trap Matrix</div>', unsafe_allow_html=True)
st.markdown(
    "<small style='color:#7b8cad'>"
    "Plot this company against its rivals. <b>High ROE + Low P/E</b> is the magic formula. <b>Low ROE + High P/E</b> is a value trap.</small><br><br>",
    unsafe_allow_html=True
)

# 1. Initialize a memory state to hold our selected competitors
if "peer_list" not in st.session_state:
    st.session_state.peer_list = []

# 2. Competitor Search & Add Bar
c_search, c_btn = st.columns([4, 1])
with c_search:
    peer_query = st.text_input("Search and add a competitor:", placeholder="Type company name...")
    
    # Live Yahoo Finance Autocomplete
    peer_suggestions = []
    if peer_query.strip():
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={peer_query.strip()}"
        headers = {'User-Agent': 'Mozilla/5.0'} 
        try:
            res = requests.get(url, headers=headers).json()
            for q in res.get('quotes', []):
                sym = q.get('symbol', '')
                if sym.endswith('.NS') or sym.endswith('.BO'):
                    name = q.get('longname') or q.get('shortname') or 'Unknown'
                    peer_suggestions.append(f"{sym}  |  {name}")
        except Exception:
            pass
            
    selected_peer_raw = ""
    if peer_suggestions:
        selected_peer_raw = st.selectbox("Matches found:", peer_suggestions)

with c_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("➕ Add", use_container_width=True):
        if selected_peer_raw:
            new_ticker = selected_peer_raw.split("  |  ")[0]
            # Prevent adding duplicates or the main company itself
            if new_ticker not in st.session_state.peer_list and new_ticker != data['ticker']:
                st.session_state.peer_list.append(new_ticker)
                st.rerun() # Instantly refresh the UI

# 3. Display selected competitors and Plot Matrix
if st.session_state.peer_list:
    # Allows the user to click the 'x' to remove a competitor
    st.session_state.peer_list = st.multiselect(
        "Selected Competitors:", 
        options=st.session_state.peer_list, 
        default=st.session_state.peer_list
    )
    
    if st.session_state.peer_list:
        with st.spinner("Plotting sector matrix..."):
            # Combine current stock + chosen peers
            full_peer_list = f"{data['ticker']}, {','.join(st.session_state.peer_list)}"
            peer_df = fetch_peer_data(full_peer_list)
            
            if not peer_df.empty:
                fig_scatter = go.Figure()
                
                # Highlight the main ticker in blue, peers in grey
                colors = ["#4a9eff" if t == data['ticker'] else "#5a6a8a" for t in peer_df["Ticker"]]
                sizes = [20 if t == data['ticker'] else 14 for t in peer_df["Ticker"]]
                
                fig_scatter.add_trace(go.Scatter(
                    x=peer_df["ROE"], 
                    y=peer_df["P/E"],
                    mode="markers+text",
                    text=peer_df["Ticker"],
                    textposition="top center",
                    marker=dict(size=sizes, color=colors, line=dict(width=1, color="#1e2535")),
                    hovertemplate="<b>%{text}</b><br>ROE: %{x:.1f}%<br>P/E: %{y:.1f}x<extra></extra>"
                ))
                
                # Draw Quadrant lines based on the group's median
                med_roe = peer_df["ROE"].median()
                med_pe = peer_df["P/E"].median()
                
                fig_scatter.add_vline(x=med_roe, line_dash="dash", line_color="#2a3550", annotation_text="Median ROE", annotation_position="bottom right", annotation_font_color="#5a6a8a")
                fig_scatter.add_hline(y=med_pe, line_dash="dash", line_color="#2a3550", annotation_text="Median P/E", annotation_position="top right", annotation_font_color="#5a6a8a")
                
                fig_scatter.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Inter, sans-serif", color="#8a9ab5"),
                    margin=dict(l=0, r=0, t=30, b=0),
                    height=400,
                    xaxis_title="Return on Equity (ROE %)",
                    yaxis_title="P/E Ratio (Valuation)",
                    xaxis=dict(gridcolor="#1e2535", showline=False, ticksuffix="%"),
                    yaxis=dict(gridcolor="#1e2535", showline=False, ticksuffix="x"),
                )
                
                st.plotly_chart(fig_scatter, use_container_width=True)
                
                # Interpretation Guide (Pushed left to avoid Markdown bug)
                st.markdown(f"""
<div style="display:flex; gap:1rem; margin-top:0.5rem; flex-wrap:wrap;">
<div style="flex:1; min-width:250px; background:rgba(34, 197, 94, 0.05); border:1px solid #232a3b; border-radius:8px; padding:1rem;">
<div style="font-size:0.75rem; font-weight:600; color:#22c55e;">Bottom-Right (Compounding Engines)</div>
<div style="font-size:0.75rem; color:#8a9ab5; margin-top:0.3rem;">High quality (High ROE), but cheap (Low P/E). This is where value is found.</div>
</div>
<div style="flex:1; min-width:250px; background:rgba(239, 68, 68, 0.05); border:1px solid #232a3b; border-radius:8px; padding:1rem;">
<div style="font-size:0.75rem; font-weight:600; color:#ef4444;">Top-Left (Value Traps)</div>
<div style="font-size:0.75rem; color:#8a9ab5; margin-top:0.3rem;">Low quality (Low ROE), but expensive (High P/E). High risk quadrant.</div>
</div>
</div>
                """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Could not fetch financial data for those competitors.")
else:
    st.info("ℹ️ Search and add competitor companies above to generate the comparison matrix.")

st.markdown('<div class="gg-divider"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 🐋 THE WHALE WATCHER (SMART MONEY FLOW)
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">🐋 The Whale Watcher (Smart Money Flow)</div>', unsafe_allow_html=True)
st.markdown(
    "<small style='color:#7b8cad'>"
    "Tracking 4-quarter momentum of Promoters & Institutions alongside Top Mutual Fund holdings.</small><br><br>",
    unsafe_allow_html=True
)

# 1. RUN THE SCRAPER FOR 4-QUARTER TREND
shp_df = fetch_shareholding_pattern(data['ticker'])

if shp_df is not None and not shp_df.empty:
    cols = shp_df.columns
    latest_q = cols[-1]
    prev_q = cols[-2]
    
    def get_val(cat):
        try:
            return float(str(shp_df.loc[cat, latest_q]).replace('%', ''))
        except: return 0.0
            
    def get_diff(cat):
        try:
            v1 = float(str(shp_df.loc[cat, latest_q]).replace('%', ''))
            v2 = float(str(shp_df.loc[cat, prev_q]).replace('%', ''))
            return v1 - v2
        except: return 0.0

    promoter_hold = get_val('Promoters')
    fii_hold = get_val('FIIs')
    dii_hold = get_val('DIIs')
    public_hold = get_val('Public')
    
    p_diff = get_diff('Promoters')
    f_diff = get_diff('FIIs')
    d_diff = get_diff('DIIs')
    
    smart_money = promoter_hold + fii_hold + dii_hold
    
    if smart_money > 75:
        sm_color, sm_title, sm_desc = "#059669", "🟢 Massive Smart Money Accumulation", f"Strong hands own {smart_money:.2f}% of this company. Retail float is extremely low."
    elif smart_money > 50:
        sm_color, sm_title, sm_desc = "#22c55e", "🟢 Healthy Institutional Backing", f"Smart money holds {smart_money:.2f}%. The stock has solid institutional trust."
    else:
        sm_color, sm_title, sm_desc = "#e11d48", "🔴 Retail Dominated (High Risk)", f"Weak hands (public) own {public_hold:.2f}% of this stock. Highly susceptible to panic selling."

    def format_qoq(val):
        if val > 0.01: return f"<span style='color:#22c55e; font-size:0.75rem; font-weight:700;'>▲ +{val:.2f}%</span>"
        elif val < -0.01: return f"<span style='color:#ef4444; font-size:0.75rem; font-weight:700;'>▼ {val:.2f}%</span>"
        else: return f"<span style='color:#5a6a8a; font-size:0.75rem; font-weight:700;'>▬ 0.00%</span>"

    # --- RENDER 3 MAIN CARDS ---
    st.markdown(f"""
<div style="background:#161b27; border:1px solid #232a3b; border-left:4px solid {sm_color}; border-radius:8px; padding:1.5rem; margin-bottom:1.5rem;">
<div style="font-size:1.1rem; font-weight:700; color:#ffffff; margin-bottom:0.3rem;">{sm_title}</div>
<div style="font-size:0.82rem; color:#8a9ab5;">{sm_desc}</div>
</div>

<div style="display:flex; gap:1rem; flex-wrap:wrap; margin-bottom:1.5rem;">
<div style="flex:1; min-width:200px; background:rgba(30, 41, 59, 0.4); border:1px solid #232a3b; border-radius:8px; padding:1.2rem;">
<div style="font-size:0.7rem; color:#8a9ab5; text-transform:uppercase; margin-bottom:0.3rem;">Skin in the Game (Promoters)</div>
<div style="font-family:'JetBrains Mono', monospace; font-size:1.5rem; font-weight:700; color:#4a9eff; display:flex; align-items:center; gap:0.6rem;">
    {promoter_hold:.2f}% {format_qoq(p_diff)}
</div>
</div>
<div style="flex:1; min-width:200px; background:rgba(30, 41, 59, 0.4); border:1px solid #232a3b; border-radius:8px; padding:1.2rem;">
<div style="font-size:0.7rem; color:#8a9ab5; text-transform:uppercase; margin-bottom:0.3rem;">Foreign Inst. (FII)</div>
<div style="font-family:'JetBrains Mono', monospace; font-size:1.5rem; font-weight:700; color:#a855f7; display:flex; align-items:center; gap:0.6rem;">
    {fii_hold:.2f}% {format_qoq(f_diff)}
</div>
</div>
<div style="flex:1; min-width:200px; background:rgba(30, 41, 59, 0.4); border:1px solid #232a3b; border-radius:8px; padding:1.2rem;">
<div style="font-size:0.7rem; color:#8a9ab5; text-transform:uppercase; margin-bottom:0.3rem;">Domestic Inst. (DII)</div>
<div style="font-family:'JetBrains Mono', monospace; font-size:1.5rem; font-weight:700; color:#059669; display:flex; align-items:center; gap:0.6rem;">
    {dii_hold:.2f}% {format_qoq(d_diff)}
</div>
</div>
</div>
    """, unsafe_allow_html=True)
    
    # --- RENDER 4-QUARTER TREND TABLE ---
    st.markdown('<div style="font-size:0.8rem; font-weight:600; color:#e8eaf0; margin-bottom:0.8rem; text-transform:uppercase; letter-spacing:0.05em;">📊 Last 4 Quarters Trend</div>', unsafe_allow_html=True)
    
    table_html = f"""
    <div style="border:1px solid #232a3b; border-radius:8px; overflow:hidden; margin-bottom:2rem;">
    <table style="width:100%; border-collapse:collapse; text-align:left; font-size:0.85rem; background-color:rgba(30, 41, 59, 0.2);">
        <thead>
            <tr style="background-color:#161b27; border-bottom:1px solid #232a3b;">
                <th style="padding:12px 16px; color:#7b8cad; font-weight:600; text-transform:uppercase; font-size:0.7rem;">Category</th>
                <th style="padding:12px 16px; color:#7b8cad; font-weight:600; text-transform:uppercase; font-size:0.7rem;">{cols[0]}</th>
                <th style="padding:12px 16px; color:#7b8cad; font-weight:600; text-transform:uppercase; font-size:0.7rem;">{cols[1]}</th>
                <th style="padding:12px 16px; color:#7b8cad; font-weight:600; text-transform:uppercase; font-size:0.7rem;">{cols[2]}</th>
                <th style="padding:12px 16px; color:#7b8cad; font-weight:600; text-transform:uppercase; font-size:0.7rem;">{cols[3]}</th>
            </tr>
        </thead>
        <tbody>
    """
    for index, row in shp_df.iterrows():
        table_html += f'<tr style="border-bottom:1px solid #1e2535;">'
        table_html += f'<td style="padding:12px 16px; color:#e8eaf0; font-weight:600;">{index}</td>'
        for c in cols:
            val = str(row[c]).replace('%', '')
            table_html += f'<td style="padding:12px 16px; color:#8a9ab5; font-family:\'JetBrains Mono\', monospace;">{val}%</td>'
        table_html += "</tr>"
    table_html += "</tbody></table></div>"
    st.markdown(table_html, unsafe_allow_html=True)
else:
    st.warning("⚠️ Screener.in bot-protection blocked the 4-quarter historical data request.")


# 2. RENDER THE MUTUAL FUND HOLDINGS FROM YFINANCE
mf_df = data.get("mf_holders")

if mf_df is not None and not mf_df.empty:
    st.markdown('<div style="font-size:0.8rem; font-weight:600; color:#e8eaf0; margin-bottom:0.8rem; text-transform:uppercase; letter-spacing:0.05em;">🏦 Top Mutual Funds Holding This Stock</div>', unsafe_allow_html=True)
    
    mf_html = """
    <div style="border:1px solid #232a3b; border-radius:8px; overflow:hidden; margin-bottom:1rem;">
    <table style="width:100%; border-collapse:collapse; text-align:left; font-size:0.85rem; background-color:rgba(30, 41, 59, 0.2);">
        <thead>
            <tr style="background-color:#161b27; border-bottom:1px solid #232a3b;">
                <th style="padding:12px 16px; color:#7b8cad; font-weight:600; text-transform:uppercase; font-size:0.7rem;">Fund Name</th>
                <th style="padding:12px 16px; color:#7b8cad; font-weight:600; text-transform:uppercase; font-size:0.7rem;">Shares Owned</th>
                <th style="padding:12px 16px; color:#7b8cad; font-weight:600; text-transform:uppercase; font-size:0.7rem;">% of Company</th>
            </tr>
        </thead>
        <tbody>
    """
    for index, row in mf_df.head(6).iterrows():
        holder = str(row.get("Holder", "Unknown Fund"))
        shares = row.get("Shares", 0)
        
        pct = 0.0
        if "pctHeld" in row and pd.notna(row["pctHeld"]): pct = float(row["pctHeld"])
        elif "% Out" in row and pd.notna(row["% Out"]): pct = float(row["% Out"])
        
        shares_str = f"{shares:,.0f}" if pd.notna(shares) and shares != 0 else "N/A"
        pct_str = f"{pct*100:.2f}%" if pct > 0 and pct < 1 else f"{pct:.2f}%" if pct > 0 else "N/A"
        
        mf_html += f"""
            <tr style="border-bottom:1px solid #1e2535;">
                <td style="padding:12px 16px; color:#e8eaf0; font-weight:500;">{holder}</td>
                <td style="padding:12px 16px; color:#8a9ab5; font-family:'JetBrains Mono', monospace;">{shares_str}</td>
                <td style="padding:12px 16px; color:#22c55e; font-weight:600; font-family:'JetBrains Mono', monospace;">{pct_str}</td>
            </tr>
        """
    mf_html += """
        </tbody>
    </table>
    </div>
    """
    st.markdown(mf_html, unsafe_allow_html=True)
else:
    st.info("ℹ️ Specific Mutual Fund breakdown is not available for this ticker via Yahoo Finance.")

st.markdown('<div class="gg-divider"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LIVE MARKET INTELLIGENCE (RECENT NEWS)
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">📰 Live Market Intelligence & News Radar</div>', unsafe_allow_html=True)
st.markdown(
    "<small style='color:#7b8cad'>"
    "Latest market headlines for this company. Stay ahead of the narrative driving the price.</small><br><br>",
    unsafe_allow_html=True
)

news_list = data.get("news")

if news_list and len(news_list) > 0:
    import datetime
    
    news_html = '<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:1rem; margin-bottom:2rem;">'
    valid_articles = 0
    
    for item in news_list:
        if valid_articles >= 6:
            break
            
        # 1. Bulletproof Parsing: Check for both old and new Yahoo Finance formats
        title = item.get("title") or item.get("content", {}).get("title", "")
        publisher = item.get("publisher") or item.get("content", {}).get("provider", {}).get("displayName", "Unknown")
        link = item.get("link") or item.get("content", {}).get("clickThroughUrl", {}).get("url", "#")
        
        # Skip empty/broken payload items so we don't draw blank cards
        if not title:
            continue
            
        timestamp = item.get("providerPublishTime")
        if timestamp:
            try:
                dt = datetime.datetime.fromtimestamp(timestamp)
                time_str = dt.strftime("%d %b %Y")
            except:
                time_str = "Recent"
        else:
            pub_date = item.get("content", {}).get("pubDate", "")
            time_str = pub_date.split("T")[0] if pub_date else "Recent"
            
        # 2. Mini-Sentiment Engine based on headline keywords
        tl = title.lower()
        if any(w in tl for w in ['surge', 'jump', 'gain', 'buy', 'up', 'high', 'bull', 'soar', 'beat', 'profit', 'upgrade']):
            badge = "<span style='background:rgba(34,197,94,0.1); color:#22c55e; border:1px solid rgba(34,197,94,0.2); padding:2px 6px; border-radius:4px; font-size:0.6rem; font-weight:600; text-transform:uppercase;'>Positive Tone</span>"
        elif any(w in tl for w in ['drop', 'fall', 'plunge', 'sell', 'down', 'low', 'bear', 'crash', 'miss', 'loss', 'warning', 'downgrade', 'penalty']):
            badge = "<span style='background:rgba(239,68,68,0.1); color:#ef4444; border:1px solid rgba(239,68,68,0.2); padding:2px 6px; border-radius:4px; font-size:0.6rem; font-weight:600; text-transform:uppercase;'>Negative Tone</span>"
        else:
            badge = "<span style='background:rgba(90,106,138,0.1); color:#8a9ab5; border:1px solid rgba(90,106,138,0.2); padding:2px 6px; border-radius:4px; font-size:0.6rem; font-weight:600; text-transform:uppercase;'>Neutral / Factual</span>"
            
        # Safely escape quotes in title so it doesn't break the HTML
        title_safe = title.replace('"', '&quot;').replace("'", "&#39;")
        
        # 3. Draw the UI Card (Zero indentation for Markdown safety)
        news_html += f"""
<a href="{link}" target="_blank" style="text-decoration:none; color:inherit;">
<div style="background:rgba(30, 41, 59, 0.4); border:1px solid #232a3b; border-radius:8px; padding:1.2rem; height:100%; transition:all 0.2s ease;">
<div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.8rem;">
<span style="font-size:0.7rem; color:#8a9ab5; font-weight:600; text-transform:uppercase; letter-spacing:0.05em;">{publisher}</span>
{badge}
</div>
<div style="font-size:0.95rem; font-weight:600; color:#e8eaf0; line-height:1.4; margin-bottom:0.8rem;">
{title_safe}
</div>
<div style="font-size:0.7rem; color:#5a6a8a; font-family:'JetBrains Mono', monospace;">
🕒 {time_str}
</div>
</div>
</a>
        """
        valid_articles += 1
        
    news_html += '</div>'
    
    if valid_articles > 0:
        st.markdown(news_html, unsafe_allow_html=True)
    else:
        st.info("ℹ️ No recent news articles found for this ticker on Yahoo Finance.")
else:
    st.info("ℹ️ No recent news articles found for this ticker on Yahoo Finance.")

st.markdown('<div class="gg-divider"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 🎙️ MANAGEMENT GUIDANCE & REALITY CHECK
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">🎙️ Management Guidance & Reality Check</div>', unsafe_allow_html=True)
st.markdown(
    "<small style='color:#7b8cad'>"
    "Connect the narrative to the math. Use the links below to access the latest conference call transcript, then enter management's growth guidance to see if it justifies today's stock price.</small><br><br>",
    unsafe_allow_html=True
)

c1, c2 = st.columns([1, 2])

with c1:
    # Clean the ticker to make it compatible with external Indian financial sites
    clean_ticker = data['ticker'].replace(".NS", "").replace(".BO", "")
    
    # 1-Click buttons to external transcript sources
    st.markdown(f"""
<div style="background:rgba(30, 41, 59, 0.4); border:1px solid #232a3b; border-radius:8px; padding:1.2rem; height:100%;">
<div style="font-size:0.8rem; color:#8a9ab5; text-transform:uppercase; margin-bottom:1rem; font-weight:600;">🔗 Direct Transcript Links</div>
<a href="https://www.screener.in/company/{clean_ticker}/consolidated/" target="_blank" style="display:block; text-decoration:none; background:#161b27; border:1px solid #2a3550; padding:0.8rem; border-radius:6px; color:#4a9eff; font-weight:600; margin-bottom:0.5rem; text-align:center; transition:0.2s;">📄 Screener.in (Concalls)</a>
<a href="https://trendlyne.com/equity/earnings-calls/{clean_ticker}/" target="_blank" style="display:block; text-decoration:none; background:#161b27; border:1px solid #2a3550; padding:0.8rem; border-radius:6px; color:#4a9eff; font-weight:600; margin-bottom:0.5rem; text-align:center; transition:0.2s;">🎙️ Trendlyne (Audio/Text)</a>
<a href="https://www.bseindia.com/stock-share-price/x/{clean_ticker}/" target="_blank" style="display:block; text-decoration:none; background:#161b27; border:1px solid #2a3550; padding:0.8rem; border-radius:6px; color:#4a9eff; font-weight:600; text-align:center; transition:0.2s;">🏛️ BSE India Filings</a>
</div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown('<div style="font-size:0.8rem; font-weight:600; color:#e8eaf0; margin-bottom:0.8rem; text-transform:uppercase; letter-spacing:0.05em;">⚖️ Guidance vs. Market Reality Test</div>', unsafe_allow_html=True)
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        # FIX 1: Explicit static key assigned to lock input stability
        mgmt_growth_input = st.number_input(
            "Management Growth Target (%)", 
            min_value=0.0, 
            max_value=100.0, 
            value=15.0, 
            step=1.0,
            key="fixed_mgmt_growth_input"
        )
        mgmt_growth = mgmt_growth_input / 100.0
    with col_g2:
        # FIX 2: Explicit static key assigned here as well
        mgmt_margin = st.number_input(
            "Management Margin Outlook (%)", 
            min_value=0.0, 
            max_value=100.0, 
            value=18.0, 
            step=1.0,
            key="fixed_mgmt_margin_input"
        )
        
    # Pull the required growth from the Reverse DCF calculation above
    try:
        req_g = implied_g 
    except:
        req_g = 0.15 
        
    diff = mgmt_growth - req_g
    
    # Grading Logic
    if diff >= 0.05:
        verdict_color, verdict_icon, verdict_text = "#22c55e", "🟢", "Highly Undervalued: Management expects growth significantly higher than what the current stock price demands."
    elif diff >= -0.02:
        verdict_color, verdict_icon, verdict_text = "#f59e0b", "🟡", "Fairly Priced: Management's guidance closely matches the growth rate already priced into the stock."
    else:
        verdict_color, verdict_icon, verdict_text = "#ef4444", "🔴", "Valuation Disconnect: The stock price requires a growth rate much higher than what management expects to deliver."
        
    st.markdown(f"""
<div style="background:#161b27; border:1px solid #232a3b; border-left:4px solid {verdict_color}; border-radius:8px; padding:1.2rem; margin-top:0.5rem;">
<div style="display:flex; justify-content:space-between; margin-bottom:0.8rem;">
<div>
<div style="font-size:0.7rem; color:#8a9ab5; text-transform:uppercase;">Market Requires</div>
<div style="font-family:'JetBrains Mono', monospace; font-size:1.4rem; font-weight:700; color:#e8eaf0;">{req_g*100:.1f}%</div>
</div>
<div style="text-align:right;">
<div style="font-size:0.7rem; color:#8a9ab5; text-transform:uppercase;">Management Guides</div>
<div style="font-family:'JetBrains Mono', monospace; font-size:1.4rem; font-weight:700; color:{verdict_color};">{mgmt_growth*100:.1f}%</div>
</div>
</div>
<div style="font-size:0.85rem; color:#c9cfe0; line-height:1.5; border-top:1px solid #232a3b; padding-top:0.8rem;">
<b>{verdict_icon} Verdict:</b> {verdict_text}
</div>
</div>
    """, unsafe_allow_html=True)
    
st.markdown('<div class="gg-divider"></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SECTION 4 — TECHNICAL ANALYSIS CHART
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">📉 Price History & Moving Averages </div>', unsafe_allow_html=True)
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
# SECTION 5 — VALUATION HISTORY (P/E VS MEDIAN)
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">⚖️ Historical P/E vs Median (Are we buying cheap?)</div>', unsafe_allow_html=True)
st.markdown(
    "<small style='color:#4a5570'>"
    "Compares the stock's current Price-to-Earnings ratio against its own historical baseline. "
    "Buying below the median line generally indicates better value.</small><br>",
    unsafe_allow_html=True
)

financials = data.get("financials")
if hist is not None and financials is not None:
    pe_fig, current_pe, median_pe = build_pe_chart(hist, financials)
    
    if pe_fig is not None:
        st.plotly_chart(pe_fig, use_container_width=True)
        
        # Quick interpretation boxes underneath the chart
        p1, p2, p3 = st.columns(3)
        with p1:
            st.markdown(f"""
            <div class="metric-card">
              <div class="mc-label">Current Trailing P/E</div>
              <div class="mc-value">{current_pe:.1f}x</div>
            </div>""", unsafe_allow_html=True)
        with p2:
            st.markdown(f"""
            <div class="metric-card">
              <div class="mc-label">Historical Median P/E</div>
              <div class="mc-value" style="color:#f59e0b">{median_pe:.1f}x</div>
            </div>""", unsafe_allow_html=True)
        with p3:
            discount = ((median_pe - current_pe) / median_pe) * 100
            is_cheap = current_pe < median_pe
            st.markdown(f"""
            <div class="metric-card">
              <div class="mc-label">Valuation Status</div>
              <div class="mc-value" style="color:{'#22c55e' if is_cheap else '#ef4444'}">
                {abs(discount):.1f}% {'Discount' if is_cheap else 'Premium'}
              </div>
              <div class="mc-sub">Compared to historical median</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("ℹ️ yfinance does not have enough historical EPS data for this specific company to build a P/E chart.")
else:
    st.info("ℹ️ Missing data required to build the historical valuation chart.")

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
