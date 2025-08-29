# Step 1: Import libraries
from IPython.display import HTML, display
import pandas as pd

# Step 2: Inputs (you can modify these)
pre_conversion = 0.22  # 22%
post_conversion = 0.29  # 29%
avg_deal_value = 15000
deals_per_month = 50

# Step 3: Calculations
conversion_gain = post_conversion - pre_conversion
extra_deals = conversion_gain * deals_per_month
incremental_revenue = extra_deals * avg_deal_value
coaching_cost = (deals_per_month * avg_deal_value * 0.1)  # 10% of monthly revenue
roi = incremental_revenue / coaching_cost if coaching_cost > 0 else 0

# Format numbers
conversion_gain_pct = conversion_gain * 100
extra_deals_rounded = round(extra_deals, 1)
incremental_revenue_str = f"${incremental_revenue:,.0f}"
roi_str = f"{roi:.2f}x"

# Step 4: Generate HTML page
html_page = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Coaching Impact Calculator</title>
  <style>
    body {{
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: #f4f6f9;
      color: #333;
      padding: 20px;
    }}
    .container {{
      max-width: 900px;
      margin: auto;
      background: white;
      padding: 30px;
      border-radius: 12px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    header {{
      text-align: center;
      margin-bottom: 25px;
    }}
    h1 {{
      color: #1976D2;
      margin: 0;
      font-size: 28px;
    }}
    .subtitle {{
      color: #666;
      font-style: italic;
      margin: 5px 0 0;
    }}
    .card {{
      background: #f9f9f9;
      border-left: 5px solid #1976D2;
      padding: 15px;
      margin: 20px 0;
      border-radius: 0 8px 8px 0;
    }}
    .highlight {{
      font-weight: bold;
      color: #1976D2;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 25px 0;
    }}
    th, td {{
      padding: 12px;
      text-align: left;
      border-bottom: 1px solid #eee;
    }}
    th {{
      background-color: #1976D2;
      color: white;
    }}
    tr:hover {{
      background-color: #f5f5f5;
    }}
    .result {{
      font-size: 18px;
      font-weight: bold;
      color: #00796B;
    }}
    .metric {{
      text-align: center;
      padding: 15px;
      margin: 10px;
      background: #e3f2fd;
      border-radius: 8px;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }}
    .metrics {{
      display: flex;
      justify-content: space-between;
      flex-wrap: wrap;
    }}
    .metrics .metric {{
      width: 22%;
      min-width: 180px;
    }}
    .footer {{
      text-align: center;
      margin-top: 40px;
      color: #888;
      font-size: 12px;
    }}
    @media (max-width: 700px) {{
      .metrics .metric {{
        width: 45%;
      }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>📈 Coaching Impact Calculator</h1>
      <p class="subtitle">Quantify the ROI of sales coaching on conversion performance</p>
    </header>

    <div class="card">
      <strong>Scenario:</strong> 
      Conversion rate improved from <span class="highlight">{pre_conversion:.0%}</span> 
      to <span class="highlight">{post_conversion:.0%}</span> 
      after coaching. Avg deal size: <span class="highlight">${avg_deal_value:,}</span>, 
      {deals_per_month} deals/month.
    </div>

    <div class="metrics">
      <div class="metric">
        <div>Conversion Gain</div>
        <div class="result">{conversion_gain_pct:.1f}%</div>
      </div>
      <div class="metric">
        <div>Extra Deals/Month</div>
        <div class="result">{extra_deals_rounded}</div>
      </div>
      <div class="metric">
        <div>Incremental Revenue</div>
        <div class="result">{incremental_revenue_str}</div>
      </div>
      <div class="metric">
        <div>ROI (Coaching Cost = 10%)</div>
        <div class="result">{roi_str}</div>
      </div>
    </div>

    <h2>📊 Detailed Results</h2>
    <table>
      <thead>
        <tr>
          <th>Metric</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Pre-Coaching Conversion Rate</strong></td>
          <td>{pre_conversion:.1%}</td>
        </tr>
        <tr>
          <td><strong>Post-Coaching Conversion Rate</strong></td>
          <td>{post_conversion:.1%}</td>
        </tr>
        <tr>
          <td><strong>Conversion Gain</strong></td>
          <td>{conversion_gain_pct:.1f}%</td>
        </tr>
        <tr>
          <td><strong>Extra Deals per Month</strong></td>
          <td>{extra_deals_rounded}</td>
        </tr>
        <tr>
          <td><strong>Avg Deal Value</strong></td>
          <td>${avg_deal_value:,}</td>
        </tr>
        <tr>
          <td><strong>Incremental Revenue</strong></td>
          <td class="result">{incremental_revenue_str}</td>
        </tr>
        <tr>
          <td><strong>Estimated Coaching Cost</strong></td>
          <td>${coaching_cost:,.0f} (10% of pipeline)</td>
        </tr>
        <tr>
          <td><strong>Return on Investment (ROI)</strong></td>
          <td class="result">{roi_str}</td>
        </tr>
      </tbody>
    </table>

    <div class="card" style="background:#e8f5e8; border-color:#4CAF50;">
      <strong>🎯 Insight:</strong> 
      For every $1 invested in coaching, you generated <strong>${roi:.2f}</strong> in extra revenue. 
      This proves coaching directly fuels the <strong>Momentum Reservoir™</strong>.
    </div>

    <div class="footer">
      Coaching Impact Model • Sales Science Engine • Generated on {pd.Timestamp.now().strftime('%b %d, %Y')}
    </div>
  </div>
</body>
</html>
"""

# Step 5: Save and download
with open("coaching_impact_calculator.html", "w") as f:
    f.write(html_page)

print("✅ Coaching Impact Calculator generated!")
print("📥 Downloading file: coaching_impact_calculator.html")

# Auto-download in Colab
from google.colab import files
files.download("coaching_impact_calculator.html")