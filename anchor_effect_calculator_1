import plotly.graph_objects as go
import math

# --- Ascendea Style Definitions (Used for HTML Output) ---
ASCENDEA_STYLES = {
    'bg_gradient': 'linear-gradient(115deg, #11453f 0%, #0a0e17 45%, #5e1b2d 100%)',
    'text_main': '#ffffff',
    'text_muted': '#949aa5',
    'accent': '#fffcb7',  # H1 color
    'glass_bg': 'rgba(255, 255, 255, 0.05)',
    'glass_border': 'rgba(255, 255, 255, 0.1)',
    'status_sweetspot': '#27a353',
    'status_valuetrap': '#cc9700',
    'status_disruption': '#922b39',
    # Chart Point Colors
    'color_substitute': '#922b39', 
    'color_competitor': '#cc9700', 
    'color_offer': '#27a353', 
    'color_premium': '#0088cc', 
    'chart_grid': 'rgba(255, 255, 255, 0.1)',
}

def calculate_anchor_metrics(sub_price, comp_price, premium_price, offer_price):
    """Calculates all key pricing metrics."""
    
    if premium_price <= sub_price:
        return {
            'pbf': "N/A", 'comp_gap': "N/A", 'premium_proximity': "N/A",
            'rating': {'title': "Invalid Range", 'summary': "Premium Price must be greater than Substitute Price.", 'status': 'disruption'}
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

def get_strategic_rating(pbf, offer_price, comp_price, premium_price):
    """Determines the strategic positioning based on PBF and price relationships."""
    
    pbf_num = float(f"{pbf:.2f}")

    if offer_price < comp_price * 0.95 and pbf_num > 0.75:
        title = "Value Trap ⚠️"
        summary = f"Your price is significantly lower than the competitor, resulting in a high PBF ({pbf_num}). You are likely leaving significant margin on the table. **Raise your price or enhance justification.**"
        status = 'valuetrap'
    elif offer_price > premium_price * 0.9 or pbf_num < 0.25:
        title = "Disruption Point 🚩"
        summary = "Your price is too close to the Premium Anchor (or beyond it). You need an **exceptionally strong value proposition** to justify this high price point."
        status = 'disruption'
    else:
        title = "Sweet Spot ✅"
        summary = f"Your price is optimally positioned in the perceived value zone. The PBF ({pbf_num}) balances value delivery with premium aspiration. **Proceed with confidence.**"
        status = 'sweetspot'

    return {'title': title, 'summary': summary, 'status': status}

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
            'line': {'color': ASCENDEA_STYLES['bg_mid'], 'width': 3} # Use dark BG color for inner line
        },
        textposition='top center',
        name='Prices',
        textfont={'family': 'Inter, sans-serif', 'size': 13, 'color': ASCENDEA_STYLES['text_muted']}
    )

    data = [trace_range, trace_points]

    layout = go.Layout(
        template='plotly_dark',  # Start with dark template
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
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent plot area
        paper_bgcolor='rgba(0, 0, 0, 0)', # Transparent paper area
    )

    fig = go.Figure(data=data, layout=layout)
    return fig

def generate_html_dashboard(metrics, fig):
    """Generates the final HTML dashboard file."""
    
    # Get the Plotly HTML Div
    chart_div = fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    # Map status to color variable
    status_color = ASCENDEA_STYLES[f"status_{metrics['rating']['status']}"]
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Anchor Effect Analysis Report</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            :root {{
                --asc-bg-gradient: {ASCENDEA_STYLES['bg_gradient']};
                --asc-text-main: {ASCENDEA_STYLES['text_main']};
                --asc-text-muted: {ASCENDEA_STYLES['text_muted']};
                --asc-accent: {ASCENDEA_STYLES['accent']};
                --asc-glass-bg: {ASCENDEA_STYLES['glass_bg']};
                --asc-glass-border: {ASCENDEA_STYLES['glass_border']};
                --status-color: {status_color};
            }}

            body {{
                font-family: 'Inter', sans-serif;
                margin: 0;
                padding: 0;
                background: var(--asc-bg-gradient);
                color: var(--asc-text-main);
                min-height: 100vh;
                padding: 40px 20px;
            }}

            h1, h2, h3, h4 {{ 
                margin: 0 0 10px;
                line-height: 1.2;
            }}

            h1 {{ color: var(--asc-accent); font-weight: 800; font-size: 2.5em; }}
            h2, h3, h4 {{ color: var(--asc-text-main); font-weight: 600; }}

            .container {{
                max-width: 1200px;
                margin: 0 auto;
                display: flex;
                flex-direction: column;
                gap: 25px;
            }}

            .asc-glass-card {{
                background: var(--asc-glass-bg);
                backdrop-filter: blur(20px); 
                -webkit-backdrop-filter: blur(20px);
                border: 1px solid var(--asc-glass-border);
                border-radius: 16px;
                padding: 30px;
                box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.4);
            }}

            .metrics-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
            }}
            
            .metric-box {{
                background-color: var(--asc-glass-bg); 
                border: 1px solid var(--asc-glass-border);
                border-radius: 8px;
                padding: 20px;
                position: relative;
                overflow: hidden;
            }}
            
            .metric-box::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 5px;
                height: 100%;
                background: var(--status-color);
            }}

            .metric-label {{
                font-size: 0.9em;
                color: var(--asc-text-muted);
                margin-bottom: 5px;
            }}

            .metric-value {{
                font-size: 1.8em; 
                font-weight: 700;
                color: var(--status-color);
            }}

            #strategicRatingBox {{
                grid-column: 1 / -1;
                text-align: center;
            }}
            
            .rating-title {{
                font-size: 2.2em;
                font-weight: 800;
                color: var(--status-color);
                margin: 10px 0 5px;
                text-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
            }}
            
            .rating-summary {{
                font-size: 1.05em;
                color: var(--asc-text-main);
                max-width: 700px;
                margin: 0 auto;
            }}

            .input-summary {{
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 1px solid var(--asc-glass-border);
            }}

            .input-item strong {{
                color: var(--asc-accent);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Anchor Effect Strategy Report</h1>
            
            <div class="asc-glass-card">
                <h2>Input Benchmarks</h2>
                <div class="input-summary">
                    <div class="input-item">Substitute Price: <strong>${(metrics['prices'][0]):,.0f}</strong></div>
                    <div class="input-item">Competitor Price: <strong>${(metrics['prices'][1]):,.0f}</strong></div>
                    <div class="input-item">Premium Anchor: <strong>${(metrics['prices'][3]):,.0f}</strong></div>
                    <div class="input-item">Your Offer Price: <strong>${(metrics['prices'][2]):,.0f}</strong></div>
                </div>
                
                <div id="strategicRatingBox" class="metric-box">
                    <h4>Price Sensitivity Rating</h4>
                    <div class="rating-title">{metrics['rating']['title']}</div>
                    <p class="rating-summary">{metrics['rating']['summary']}</p>
                </div>
            </div>
            
            <div class="asc-glass-card">
                <h2>Key Strategic Metrics</h2>
                <div class="metrics-grid">
                    <div class="metric-box" style="--status-color: {status_color};">
                        <div class="metric-label">Perceived Bargain Factor (PBF)</div>
                        <div class="metric-value">{metrics['pbf']}</div>
                    </div>
                    
                    <div class="metric-box" style="--status-color: {status_color};">
                        <div class="metric-label">Competitor Gap (Offer vs. Competitor)</div>
                        <div class="metric-value">{metrics['comp_gap']}</div>
                    </div>
                    
                    <div class="metric-box" style="--status-color: {status_color};">
                        <div class="metric-label">Premium Proximity (Distance to Ceiling)</div>
                        <div class="metric-value">{metrics['premium_proximity']}</div>
                    </div>
                </div>
            </div>
            
            <div class="asc-glass-card">
                <h2>Price Spectrum Visualization</h2>
                <p style="color: var(--asc-text-muted);">Visualizing your position relative to the three critical market anchors.</p>
                {chart_div}
            </div>
            
        </div>
    </body>
    </html>
    """
    
    # Save the file
    filename = "anchor_results.html"
    with open(filename, "w") as f:
        f.write(html_content)
    
    print(f"\n--- Report Generated ---")
    print(f"The interactive report has been saved as {filename}")
    print(f"Open {filename} in your browser to view the Ascendea dashboard.")

def main():
    """Main function to handle user input and generate the report."""
    print("--- Ascendea Strategic Anchor Effect Calculator ---")
    print("Define your four anchor prices for market analysis.")
    print("-" * 40)
    
    try:
        sub_price = float(input("1. Enter Substitute Price (The Floor): $"))
        comp_price = float(input("2. Enter Competitor Price (The Primary Benchmark): $"))
        premium_price = float(input("3. Enter Premium Anchor (The Ceiling): $"))
        offer_price = float(input("4. Enter Your Offer Price (The Focal Point): $"))
    except ValueError:
        print("\nInvalid input. Please enter valid numbers for all prices.")
        return

    # Check for negative prices
    if any(p < 0 for p in [sub_price, comp_price, premium_price, offer_price]):
        print("\nPrices cannot be negative. Please restart with valid inputs.")
        return
        
    # Check for zero competitor price before processing
    if comp_price <= 0:
        print("\nWarning: Competitor Price should be greater than zero for accurate gap analysis.")

    # Calculate metrics
    metrics = calculate_anchor_metrics(sub_price, comp_price, premium_price, offer_price)
    
    # Generate visualization
    fig = generate_plotly_figure(metrics)
    
    # Generate HTML report
    generate_html_dashboard(metrics, fig)

if __name__ == "__main__":
    main()
