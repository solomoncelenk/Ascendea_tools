import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Ascendea OS // LDI Console", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- CUSTOM ASCENDEA STYLING (FIXED) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap');
    
    /* Global Styles */
    .stApp { background-color: #080a0c; }
    header { background-color: rgba(0,0,0,0) !important; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { 
        background-color: #0c0f12; 
        border-right: 1px solid rgba(0, 228, 171, 0.1); 
    }
    
    /* Typography */
    h1, h2, h3, p, span, label { 
        font-family: 'Inter', sans-serif !important; 
        color: #fffcb7 !important; 
    }
    
    /* Input Styling */
    .stSelectbox label, .stSlider label {
        font-weight: 800 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        font-size: 12px !important;
        color: #00e4ab !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR CONTROLS ---
st.sidebar.markdown("## **ASCENDEA OS**")
st.sidebar.markdown("---")

stage = st.sidebar.selectbox(
    "Revenue Stage",
    ["Stage 1: Founder-Led ($0-$1M)", 
     "Stage 2: Process-Led ($1M-$5M)", 
     "Stage 3: Team-Driven ($5M-$10M)", 
     "Stage 4: Sovereign System ($10M+)"]
)

st.sidebar.markdown("### **Time Allocation**")
execution_hours = st.sidebar.slider("Execution (Closing / Deals)", 0, 200, 80)
system_hours = st.sidebar.slider("Systems (Ops / Architecture)", 0, 200, 20)

# Calculations
total_hours = execution_hours + system_hours
ldi_actual = (system_hours / total_hours * 100) if total_hours > 0 else 0

# Framework Targets
stage_targets = {
    "Stage 1: Founder-Led ($0-$1M)": 20,
    "Stage 2: Process-Led ($1M-$5M)": 50,
    "Stage 3: Team-Driven ($5M-$10M)": 75,
    "Stage 4: Sovereign System ($10M+)": 90
}
ldi_target = stage_targets[stage]
gap = ldi_target - ldi_actual

# Status Logic
if gap > 20:
    status, status_color = "CRITICAL BOTTLENECK", "#ee4128"
elif gap > 0:
    status, status_color = "OPTIMIZING SYSTEM", "#fffcb7"
else:
    status, status_color = "SYSTEMIC SOVEREIGNTY", "#00e4ab"

# --- THE COMMAND CONSOLE (HTML/SVG/JS) ---
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #080a0c;
            --accent: #00e4ab;
            --warning: #fffcb7;
            --danger: #ee4128;
            --border: rgba(255, 255, 255, 0.08);
        }}
        body {{ 
            background: var(--bg); 
            color: var(--warning); 
            font-family: 'Inter', sans-serif; 
            margin: 0; padding: 20px;
            overflow: hidden;
        }}
        .console-frame {{
            border: 1px solid var(--border);
            padding: 40px;
            position: relative;
            background: radial-gradient(circle at 50% 50%, rgba(0, 228, 171, 0.03), transparent 80%);
            border-radius: 20px;
        }}
        .hud-bracket {{ position: absolute; width: 30px; height: 30px; border: 3px solid var(--accent); }}
        .tl {{ top: -2px; left: -2px; border-right: none; border-bottom: none; }}
        .tr {{ top: -2px; right: -2px; border-left: none; border-bottom: none; }}
        .bl {{ bottom: -2px; left: -2px; border-right: none; border-top: none; }}
        .br {{ bottom: -2px; right: -2px; border-left: none; border-top: none; }}
        
        .header {{ display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 40px; }}
        .kicker {{ font-size: 12px; font-weight: 900; letter-spacing: 0.4em; text-transform: uppercase; color: var(--accent); }}
        .title {{ font-size: 48px; font-weight: 900; margin: 0; letter-spacing: -0.04em; color: #fff; }}
        
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 40px; }}
        .metric-box {{ background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 30px; border-radius: 16px; }}
        .metric-label {{ font-size: 11px; font-weight: 800; letter-spacing: 0.2em; text-transform: uppercase; color: var(--accent); margin-bottom: 10px; }}
        .metric-value {{ font-size: 64px; font-weight: 900; color: #fff; }}
        
        .status-badge {{
            display: inline-block; padding: 10px 20px; border-radius: 4px;
            font-weight: 900; font-size: 14px; letter-spacing: 0.2em;
            background: {status_color}22; color: {status_color}; border: 1px solid {status_color};
        }}
        svg {{ overflow: visible; width: 100%; height: auto; }}
        .glow {{ filter: drop-shadow(0 0 10px var(--accent)); }}
    </style>
</head>
<body>
    <div class="console-frame">
        <div class="hud-bracket tl"></div><div class="hud-bracket tr"></div>
        <div class="hud-bracket bl"></div><div class="hud-bracket br"></div>

        <div class="header">
            <div>
                <p class="kicker">Leadership Displacement Index</p>
                <h1 class="title">Command Console</h1>
            </div>
            <div class="status-badge">{status}</div>
        </div>

        <div class="grid">
            <div class="metric-box">
                <p class="metric-label">Actual LDI</p>
                <div class="metric-value">{ldi_actual:.1f}%</div>
                <p style="font-size: 12px; opacity: 0.5; margin-top: 10px;">SYSTEM FOCUS RATIO</p>
                
                <svg viewBox="0 0 400 60" style="margin-top: 30px;">
                    <rect width="400" height="12" rx="6" fill="rgba(255,255,255,0.05)" />
                    <rect width="{ldi_actual * 4}" height="12" rx="6" fill="var(--accent)" class="glow" />
                    <line x1="{ldi_target * 4}" y1="-10" x2="{ldi_target * 4}" y2="22" stroke="var(--warning)" stroke-width="2" stroke-dasharray="4 2" />
                    <text x="{ldi_target * 4}" y="45" text-anchor="middle" fill="var(--warning)" font-size="10" font-weight="900">STAGE TARGET: {ldi_target}%</text>
                </svg>
            </div>

            <div class="metric-box">
                <p class="metric-label">Efficiency Diagnostic</p>
                <svg viewBox="0 0 300 180">
                    <path d="M 50 150 A 100 100 0 0 1 250 150" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="20" stroke-linecap="round" />
                    <path d="M 50 150 A 100 100 0 0 1 {50 + (ldi_actual * 2)} 150" fill="none" stroke="var(--accent)" stroke-width="20" stroke-linecap="round" class="glow" />
                    
                    <text x="150" y="130" text-anchor="middle" fill="#fff" font-size="42" font-weight="900">{int(ldi_actual)}</text>
                    <text x="150" y="155" text-anchor="middle" fill="var(--accent)" font-size="10" font-weight="900">INDEX SCORE</text>
                </svg>
            </div>
        </div>

        <div style="margin-top: 40px; border-top: 1px solid var(--border); padding-top: 20px; display: flex; justify-content: space-between; font-size: 11px; letter-spacing: 0.3em; opacity: 0.4;">
            <div>OS VERSION: 2026.V4</div>
            <div>STATUS: STANDBY // DATA ENCRYPTED</div>
        </div>
    </div>
</body>
</html>
"""

# Render the Command Console
components.html(html_code, height=650)

# --- LOWER ACTION PANEL ---
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### **Diagnostic Result**")
    if gap > 20:
        st.error(f"**Critical Gap:** You are operating {gap:.1f}% below the efficiency required for your revenue stage. Founder bandwidth is currently the primary ceiling on growth.")
    elif gap > 0:
        st.warning(f"**Optimization Window:** You are {gap:.1f}% off-target. Transition of manual deal-work to the RevOps system should be prioritized this quarter.")
    else:
        st.success(f"**Sovereign State:** Your displacement ratio is optimized. Focus on market coverage and leadership development.")

with col2:
    st.markdown("### **Architectural Next Step**")
    if stage.startswith("Stage 1"):
        st.info("Commit to: **The Sales Evolution Matrix.** Standardize your core deal motion before hiring.")
    elif stage.startswith("Stage 2"):
        st.info("Commit to: **The RevOps Foundation.** Migrate deal tracking from founder-memory to a unified data source.")
    elif stage.startswith("Stage 3"):
        st.info("Commit to: **Management Enablement.** Shift your time from coaching reps to coaching the coaches.")
    else:
        st.info("Commit to: **System Governance.** Audit your national territory models and forecasting risk weightings.")

st.button("Export Full Deployment Plan (PDF)")
