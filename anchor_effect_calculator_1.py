import streamlit as st
import plotly.graph_objects as go
import math

# --- 1. Ascendea Style Definitions ---
ASCENDEA_STYLES = {
    'bg_gradient': 'linear-gradient(115deg, #11453f 0%, #0a0e17 45%, #5e1b2d 100%)',
    'text_main': '#ffffff',
    'text_muted': '#949aa5',
    'accent': '#fffcb7',
    'glass_bg': 'rgba(255, 255, 255, 0.05)',
    'glass_border': 'rgba(255, 255, 255, 0.1)',
    'status_sweetspot': '#27a353',
    'status_valuetrap': '#cc9700',
    'status_disruption': '#922b39',
    'color_substitute': '#922b39', 
    'color_competitor': '#cc9700', 
    'color_offer': '#27a353', 
    'color_premium': '#0088cc', 
    'chart_grid': 'rgba(255, 255, 255, 0.1)',
    # FIX: Added the missing 'bg_mid' key for Plotly line coloring
    'bg_mid': '#0a0e17', 
}

# Injecting Custom CSS to mimic the Ascendea theme
st.markdown(
    f"""
    <style>
    /* Use Inter font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="stApp"] {{
        font-family: 'Inter', sans-serif !important;
        color: {ASCENDEA_STYLES['text_main']};
    }}

    /* Apply the dark gradient background */
    .stApp {{
        background: {ASCENDEA_STYLES['bg_gradient']};
    }}

    /* Global Typography */
    h1 {{ color: {ASCENDEA_STYLES['accent']}; font-weight: 800; font-size: 2.5em; line-height: 1.2; }}
    h2, h3, h4 {{ color: {ASCENDEA_STYLES['text_main']} !important; font-weight: 600; }}

    /* Glass Card Styling (applied to Streamlit containers) */
    .asc-glass-card {{
        background: {ASCENDEA_STYLES['glass_bg']};
        backdrop-filter: blur(20px); 
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid {ASCENDEA_STYLES['glass_border']};
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.4);
        margin-bottom: 25px;
    }}
    
    /* Input Styling Adjustments */
    div[data-testid="stNumberInput"] label p {{
        color: {ASCENDEA_STYLES['text_muted']};
        font-weight: 500;
    }}

    /* Metric Box Styles (must use Streamlit columns/containers) */
    .metric-container {{
        background: {ASCENDEA_STYLES['glass_bg']};
        border: 1px solid {ASCENDEA_STYLES['glass_border']};
        border-radius: 8px;
        padding: 20px;
        position: relative;
        overflow: hidden;
    }}

    .metric-container::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: var(--status-color, {ASCENDEA_STYLES['accent']});
    }}

    .metric-label {{
        color: {ASCENDEA_STYLES['text_muted']};
        font-size: 0.9em;
        margin-bottom: 5px;
    }}

    .metric-value {{
        font-size: 1.8em; 
        font-weight: 700;
        color: var(--status-color, {ASCENDEA_STYLES['accent']});
    }}
    
    /* Rating Box Styling */
    .rating-title {{
        font-size: 2.2em;
        font-weight: 800;
        color: var(--status-color, {ASCENDEA_STYLES['accent']});
        margin: 10px 0 5px;
    }}
    .rating-summary {{
        font-size: 1.05em;
        color: {ASCENDEA_STYLES['text_main']};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- 2. Core Calculation Functions (Reused) ---

def get_strategic_rating(pbf, offer_price, comp_price, premium_price):
    """Determines the strategic positioning based on PBF and price relationships."""
    
    pbf_num = float(f"{pbf:.2f}")

    if offer_price < comp_price * 0.95 and pbf_num > 0.75:
        title = "Value Trap ⚠️"
        summary = f"Your price is significantly lower than the competitor, resulting in a high PBF ({pbf_num}). You are likely leaving significant margin on the table. **Raise your price or enhance justification.**"
        status = 'disruption'  # Mapped to 'disruption' for red/high caution
        status_color = ASCENDEA_STYLES['status_valuetrap']
    elif offer_price > premium_price * 0.9 or pbf_num < 0.25:
        title = "Disruption Point 🚩"
        summary = "Your price is too close to the Premium Anchor (or beyond it). You need an **exceptionally strong value proposition** to justify this high price point."
        status = 'disruption'
        status_color = ASCENDEA_STYLES['status_disruption']
    else:
        title = "Sweet Spot ✅"
        summary = f"Your price is optimally positioned in the perceived value zone. The PBF ({pbf_num}) balances value delivery with premium aspiration. **Proceed with confidence.**"
        status = 'sweetspot'
        status_color = ASCENDEA_STYLES['status_sweetspot']

    return {'title': title, 'summary': summary, 'status': status, 'color': status_color}

def calculate_anchor_metrics(sub_price, comp_price, premium_price, offer_price):
    """Calculates all key pricing metrics."""
    
    if premium_price <= sub_price:
        rating = get_strategic_rating(0, offer_price, comp_price, premium_price)
        return {
            'pbf': "N/A", 'comp_gap': "N/A", 'premium_proximity': "N/A",
            'rating': {'title': "Invalid Range", 'summary': "Premium Price must be greater than Substitute Price.", 'status': 'disruption', 'color': ASCENDEA_STYLES['status_disruption']}
        }

    range_val = premium_price - sub_price
    
    # 1. Perceived Bargain Factor (PBF)
    pbf = 1 - (offer_price - sub_price) / range_val
    pbf = max(0, min(1, pbf))
    
    # 2. Competitor Gap
    comp_gap = ((offer_price / comp_price) * 100 - 100) if comp_price > 0 else 0
    
    # 3. Premium Proximity
    premium_proximity = ((offer_price - sub_price) / range_val * 100)

    # 4. Strategic Rating
    rating = get_strategic_rating(pbf, offer_price, comp_price, premium_price)
    
    return {
        'pbf': f"{pbf:.2f}",
        'comp_gap': f"{comp_gap:.0f}%",
        'premium_proximity': f"{premium_proximity:.0f}%",
        'rating': rating,
        'prices': [sub_price, comp_price, offer_price, premium_price]
    }

def generate_plotly_figure(metrics):
    """Generates the Plotly figure object for the price spectrum."""
    
    prices = metrics['prices']
    labels = ["Substitute", "Competitor", "Your Offer", "Premium"]
    
    colors = [
        ASCENDEA_STYLES['color_substitute'],
        ASCENDEA_STYLES['color_competitor'],
        ASCENDEA_STYLES['color_offer'],
        ASCENDEA_STYLES['color_premium']
    ]

    # Horizontal Price Line
    trace_range = go.Scatter(
        x=[prices[0], prices[3]],
        y=[0, 0],
        mode='lines',
        line={'color': ASCENDEA_STYLES['chart_grid'], 'width': 4},
        hoverinfo='none',
        showlegend=False
    )

    # Price Points (Markers) - Your Offer point is slightly raised for emphasis (0.1)
    trace_points = go.Scatter(
        x=prices,
        y=[0, 0, 0.1, 0],
        text=[f"{l}<br>(${(p):,.0f})" for l, p in zip(labels, prices)],
        mode='markers+text',
        marker={
            'size': 18, 
            'color': colors,
            # FIX applied here: ASCENDEA_STYLES['bg_mid'] is now available
            'line': {'color': ASCENDEA_STYLES['bg_mid'], 'width': 3} 
        },
        textposition='top center',
        name='Prices',
        textfont={'family': 'Inter, sans-serif', 'size': 13, 'color': ASCENDEA_STYLES['text_muted']}
    )

    data = [trace_range, trace_points]

    layout = go.Layout(
        template='plotly_dark',
        title=False,
        xaxis={
            'title': False,
            'range': [min(prices) * 0.9, max(prices) * 1.1],
            'tickformat': '$,.0f',
            'tickfont': {'color': ASCENDEA_STYLES['text_muted']},
            'linecolor': ASCENDEA_STYLES['chart_grid'],
            'showgrid': False,
            'zeroline': False
        },
        yaxis={
            'visible': False,
            'range': [-0.5, 0.5], 
            'zeroline': False
        },
        showlegend=False,
        hovermode='closest',
        margin={'t': 50, 'b': 50, 'l': 30, 'r': 30},
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
    )

    fig = go.Figure(data=data, layout=layout)
    return fig

# --- 3. Streamlit Application Layout ---

def app():
    """Defines the Streamlit application structure and logic."""

    # Page Title
    st.title("Anchor Effect Strategy Report")
    
    # --- STEP 1: INPUT BENCHMARKS ---
    with st.container(border=True): # Simulates the asc-glass-card style
        st.markdown(f'<div class="asc-glass-card">', unsafe_allow_html=True)
        st.markdown("## 1. Define Your Price Anchors")
        st.markdown(f"<p style='color: {ASCENDEA_STYLES['text_muted']}'>Enter the prices that define the ceiling and floor of your market's perception.</p>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            sub_price = st.number_input("Substitute Price ($) - The Floor", value=50, min_value=0)
        with col2:
            comp_price = st.number_input("Competitor Price ($) - The Primary Benchmark", value=500, min_value=0)
        with col3:
            premium_price = st.number_input("Premium Anchor ($) - The Ceiling", value=5000, min_value=0)
        with col4:
            offer_price = st.number_input("Your Offer Price ($) - The Focal Point", value=2000, min_value=0)
        
        st.markdown(f'</div>', unsafe_allow_html=True)


    # Calculate metrics based on current inputs
    metrics = calculate_anchor_metrics(sub_price, comp_price, premium_price, offer_price)
    rating = metrics['rating']
    status_color = rating['color']
    
    
    # --- STEP 2: STRATEGIC INSIGHTS & METRICS ---
    with st.container(border=True): # Simulates the asc-glass-card style
        st.markdown(f'<div class="asc-glass-card">', unsafe_allow_html=True)
        st.markdown("## 2. Strategic Insights & Metrics")

        # Strategic Rating Box (Full Width)
        st.markdown(
            f"""
            <div class="metric-container" style="text-align: center; margin-bottom: 25px; --status-color: {status_color}">
                <h4 style="margin: 0;">Price Sensitivity Rating</h4>
                <div class="rating-title" style="color: {status_color}">{rating['title']}</div>
                <p class="rating-summary">{rating['summary']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Key Strategic Metrics Grid
        col_pbf, col_comp, col_prox = st.columns(3)

        # PBF Metric
        with col_pbf:
            st.markdown(
                f"""
                <div class="metric-container" style="--status-color: {status_color}">
                    <div class="metric-label">Perceived Bargain Factor (PBF)</div>
                    <div class="metric-value" style="color: {status_color}">{metrics['pbf']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Competitor Gap Metric
        with col_comp:
            st.markdown(
                f"""
                <div class="metric-container" style="--status-color: {status_color}">
                    <div class="metric-label">Competitor Gap (Offer vs. Competitor)</div>
                    <div class="metric-value" style="color: {status_color}">{metrics['comp_gap']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Premium Proximity Metric
        with col_prox:
            st.markdown(
                f"""
                <div class="metric-container" style="--status-color: {status_color}">
                    <div class="metric-label">Premium Proximity (Distance to Ceiling)</div>
                    <div class="metric-value" style="color: {status_color}">{metrics['premium_proximity']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown(f'</div>', unsafe_allow_html=True)


    # --- STEP 3: VISUALIZATION ---
    with st.container(border=True):
        st.markdown(f'<div class="asc-glass-card">', unsafe_allow_html=True)
        st.markdown("## 3. Price Spectrum Visualization")
        st.markdown(f"<p style='color: {ASCENDEA_STYLES['text_muted']}'>Visualizing your position relative to the three critical market anchors.</p>", unsafe_allow_html=True)

        # Generate and display the Plotly chart
        if metrics['pbf'] != "N/A":
            fig = generate_plotly_figure(metrics)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.error("Cannot render chart: Premium Anchor must be greater than Substitute Price.")
            
        st.markdown(f'</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    # Configure wide layout
    st.set_page_config(layout="wide")
    app()
