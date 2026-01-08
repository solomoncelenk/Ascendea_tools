import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(page_title="Ascendea OS // LDI Console", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM ASCENDEA STYLING (STREAMLIT UI) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap');
    
    .main { background-color: #080a0c; color: #fffcb7; }
    .stApp { background-color: #080a0c; }
    [data-testid="stSidebar"] { background-color: #0c0f12; border-right: 1px solid rgba(0, 228, 171, 0.1); }
    .stSlider [data-baseweb="slider"] { margin-top: 20px; }
    h1, h2, h3, p { font-family: 'Inter', sans-serif !important; }
    .stMarkdown { color: #fffcb7; }
    </style>
    """, unsafe_allow_view_rule=True)

# --- APP LOGIC ---
st.sidebar.image("https://via.placeholder.com/150x50/080a0c/00e4ab?text=ASCENDEA+OS", width=200) # Placeholder for your logo
st.sidebar.markdown("### **System Inputs**")

stage = st.sidebar.selectbox(
    "Select Revenue Stage",
    ["Stage 1: Founder-Led ($0-$1M)", 
     "Stage 2: Process-Led ($1M-$5M)", 
     "Stage 3: Team-Driven ($5M-$10M)", 
     "Stage 4: Sovereign System ($10M+)"]
)

execution_hours = st.sidebar.slider("Monthly Hours: Execution (Closing/Deals)", 0, 200, 80)
system_hours = st.sidebar.slider("Monthly Hours: Systems (Architecture/Ops)", 0, 200, 20)

# Calculations
total_hours = execution_hours + system_hours
ldi_actual = (system_hours / total_hours * 100) if total_hours > 0 else 0

# Targets based on framework
stage_map = {
    "Stage 1: Founder-Led ($0-$1M)": 20,
    "Stage 2: Process-Led ($1M-$5M)": 50,
    "Stage 3: Team-Driven ($5M-$10M)": 75,
    "Stage 4: Sovereign System ($10M+)": 90
}
ldi_target = stage_map[stage]
gap = ldi_target - ldi_actual
status = "CRITICAL BOTTLENECK" if gap > 20 else "OPTIMIZING" if gap > 0 else "SYSTEMIC SOVEREIGNTY"
status_color = "#ee4128" if gap > 20 else "#fffcb7" if gap > 0 else "#00e4ab"

# --- THE HIGH-END SIMULATOR UI (HTML/SVG/JS) ---
# We inject the Python variables directly into the JS string
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
        .hud-bracket {{
            position: absolute; width: 30px; height: 30px; border: 3px solid var(--accent);
        }}
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
            background: {status_color}33; color: {status_color}; border: 1px solid {status_color};
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
                
                <svg viewBox="0 0 400 40" style="margin-top: 30px;">
                    <rect width="400" height="12" rx="6" fill="rgba(255,255,255,0.05)" />
                    <rect width="{ldi_actual * 4}" height="12" rx="6" fill="var(--accent)" class="glow" />
                    <line x1="{ldi_target * 4}" y1="0" x2="{ldi_target * 4}" y2="30" stroke="var(--warning)" stroke-width="2" stroke-dasharray="4 2" />
                    <text x="{ldi_target * 4}" y="45" text-anchor="middle" fill="var(--warning)" font-size="10" font-weight="900">TARGET: {ldi_target}%</text>
                </svg>
            </div>

            <div class="metric-box">
                <p class="metric-label">Efficiency Diagnostic</p>
                <svg viewBox="0 0 300 200">
                    <circle cx="150" cy="180" r="120" fill="none" stroke="var(--border)" stroke-width="10" stroke-dasharray="2 2" />
                    <path d="M 30 180 A 120 120 0 0 1 270 180" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="20" stroke-linecap="round" />
                    <path d="M 30 180 A 120 120 0 0 1 {30 + (ldi_actual * 2.4)} 180" fill="none" stroke="var(--accent)" stroke-width="20" stroke-linecap="round" class="glow" />
                    
                    <text x="150" y="150" text-anchor="middle" fill="#fff" font-size="40" font-weight="900">{int(ldi_actual)}</text>
                    <text x="150" y="175" text-anchor="middle" fill="var(--accent)" font-size="10" font-weight="900">INDEX SCORE</text>
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

# Render the component
components.html(html_code, height=700)

# --- ACTIONABLE NEXT STEPS (PYTHON UI) ---
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### **The Diagnosis**")
    if gap > 20:
        st.error(f"**Action Required:** You are currently {gap:.1f}% below the System-Focus target for {stage.split(':')[0]}.")
    elif gap > 0:
        st.warning(f"**Optimization window:** You are approaching the inflection point. Start displacing execution tasks now.")
    else:
        st.success(f"**Elite Alignment:** Your displacement index is healthy. Focus on maintaining system integrity.")

with col2:
    st.markdown("### **Deployment Step**")
    st.button("Generate Architectural Upgrade Plan")
