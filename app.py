import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------
st.set_page_config(
    page_title="AI Receipt Intelligence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------
# COMPLETE DARK UI SYSTEM
# -------------------------------------------------------
st.markdown("""
<style>

/* Remove default elements */
header, footer, #MainMenu {
    visibility: hidden;
}

[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"] {
    display: none !important;
}

/* Remove spacing gap */
.block-container {
    padding-top: 0rem !important;
    margin-top: -50px !important;
}

/* Main background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg,#0f172a,#020617) !important;
}

html, body {
    background: #020617 !important;
    color: #cbd5e1 !important;
    font-family: 'Inter', sans-serif;
}

/* Sidebar redesign */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0f172a,#111827);
    border-right: 1px solid rgba(255,255,255,0.05);
    padding-top: 2rem;
}

/* Sidebar text ALL DARK STYLE */
section[data-testid="stSidebar"] * {
    color: #cbd5e1 !important;
    font-weight: 600 !important;
}

/* Sidebar card look */
.sidebar-card {
    background: rgba(255,255,255,0.05);
    padding: 18px;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 20px;
}

/* Dark input */
section[data-testid="stSidebar"] input {
    background-color: #1e293b !important;
    color: #e2e8f0 !important;
    border: 1px solid #334155 !important;
}

/* Title */
.header-text {
    background: linear-gradient(90deg,#38bdf8,#818cf8,#c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3.4rem;
    font-weight: 900;
    text-align: center;
}

/* Cards */
.section-card {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 28px;
    border-radius: 18px;
    margin-top: 20px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

.section-card h3, 
.section-card h4, 
.section-card p {
    color: #e2e8f0 !important;
}

/* Metrics */
[data-testid="stMetricValue"] {
    color: #38bdf8 !important;
    font-weight: 900 !important;
    font-size: 1.6rem !important;
}

[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
}

/* Dataframe */
[data-testid="stDataFrame"] td {
    color: #e2e8f0 !important;
}

/* Progress */
.stProgress > div > div {
    background: linear-gradient(90deg,#38bdf8,#818cf8);
}

/* Alert */
.budget-alert {
    padding: 15px;
    border-radius: 14px;
    margin-top: 20px;
    font-weight: 800;
    text-align: center;
    font-size: 1.05rem;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# SIDEBAR CONTENT (UPGRADED)
# -------------------------------------------------------
with st.sidebar:

    st.markdown("## 💎 AI Financial Engine")

    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    st.markdown("### 👤 Financial Profile")

    user_income = st.number_input(
        "Monthly Income ($)",
        min_value=0.0,
        value=0.0,
        step=100.0
    )

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    st.markdown("### 🚀 About This Project")

    st.write("""
    **AI-Powered Receipt Analyzer** is an end-to-end intelligent
    financial insight system.

    🔍 OCR extracts item-level data  
    🧠 AI categorizes expenses  
    📊 Spending patterns analyzed  
    💡 LLM generates budgeting advice  

    Built for intelligent, automated personal finance tracking.
    """)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    st.markdown("### 🧠 AI Pipeline")

    st.write("""
    1. Image Preprocessing  
    2. OCR Text Extraction  
    3. Data Structuring  
    4. Expense Categorization  
    5. Spending Analytics  
    6. LLM Financial Insight Generation  
    """)

    st.markdown('</div>', unsafe_allow_html=True)

    st.caption("Version 4.0 | Hackathon Edition")

# -------------------------------------------------------
# HERO SECTION
# -------------------------------------------------------
st.markdown('<h1 class="header-text">AI Powered Receipt Intelligence</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#94a3b8;'>Multimodal OCR + AI Financial Insight System</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Receipt Image", type=["jpg", "png", "jpeg"])

# -------------------------------------------------------
# MAIN LOGIC
# -------------------------------------------------------
if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}

    try:
        response = requests.post("http://127.0.0.1:8000/process", files=files)

        if response.status_code == 200:
            data = response.json()

            spent = float(data.get("total", 0))
            remaining = user_income - spent
            percent = (spent / user_income * 100) if user_income > 0 else 0

            # Spend Analysis
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("### 📊 Real-Time Financial Analysis")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Merchant", data.get("merchant", "N/A"))
            c2.metric("Income", f"${user_income:,.2f}")
            c3.metric("Receipt Total", f"${spent:,.2f}")
            c4.metric("Remaining", f"${remaining:,.2f}")

            if percent > 85:
                bg = "linear-gradient(90deg,#7f1d1d,#b91c1c)"
                msg = f"🚨 Critical Spending: {percent:.1f}% of income used"
            elif percent > 50:
                bg = "linear-gradient(90deg,#78350f,#f59e0b)"
                msg = f"⚠️ Moderate Utilization: {percent:.1f}% used"
            else:
                bg = "linear-gradient(90deg,#064e3b,#10b981)"
                msg = f"✅ Healthy Budget Usage: {percent:.1f}% used"

            st.markdown(
                f'<div class="budget-alert" style="background:{bg}; color:white;">{msg}</div>',
                unsafe_allow_html=True
            )

            st.progress(min(percent / 100, 1.0))
            st.markdown('</div>', unsafe_allow_html=True)

            # Charts + AI
            col1, col2 = st.columns([1.2, 1])

            with col1:
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown("#### 📊 Category Distribution")

                cat_data = data.get("category_totals", {})
                if cat_data:
                    fig = px.pie(
                        values=list(cat_data.values()),
                        names=list(cat_data.keys()),
                        hole=0.6,
                        template="plotly_dark"
                    )
                    fig.update_layout(height=350)
                    st.plotly_chart(fig, use_container_width=True)

                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown("#### 🤖 AI Financial Recommendation")
                st.write(data.get("financial_advice", "Analysis complete."))

                if data.get("anomalies"):
                    for anomaly in data["anomalies"]:
                        st.error(anomaly)

                st.markdown('</div>', unsafe_allow_html=True)

            # Items
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("#### 🛒 Itemized Breakdown")
            st.dataframe(pd.DataFrame(data.get("items", [])), use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.error("Backend error.")

    except Exception as e:
        st.error(f"Backend Offline: {e}")

else:
    st.info("Upload a receipt to generate AI-powered financial insights.")
