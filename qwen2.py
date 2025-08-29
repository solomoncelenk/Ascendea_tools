# Step 1: Import libraries
import pandas as pd
from google.colab import files

# Step 2: Simulate your CRM data (since we don't have crm_export.csv)
# Replace this with pd.read_csv('crm_export.csv') when you have real data
import numpy as np

np.random.seed(42)
crm_data = {
    'Stage': np.random.choice(['Closed Won', 'Open', 'Closed Lost'], size=100, p=[0.3, 0.5, 0.2]),
    'Deal Size': np.random.normal(21000, 5000, 100).astype(int),
    'Cycle Days': np.random.normal(50, 15, 100).astype(int)
}
df = pd.DataFrame(crm_data)

# Ensure no negative cycle days
df['Cycle Days'] = df['Cycle Days'].abs()

# Step 3: Calculate metrics
closed_won = df[df['Stage'] == 'Closed Won']
open_deals = df[df['Stage'] == 'Open']

opportunities = len(closed_won) + len(open_deals)
win_rate = len(closed_won) / len(df[df['Stage'].isin(['Closed Won', 'Closed Lost']) + open_deals]) if len(df[df['Stage'].isin(['Closed Won', 'Closed Lost'])]) > 0 else 0
avg_deal_size = closed_won['Deal Size'].mean() if len(closed_won) > 0 else 0
cycle_length = closed_won['Cycle Days'].mean() if len(closed_won) > 0 else 0
velocity = (opportunities * win_rate * avg_deal_size) / cycle_length if cycle_length > 0 else 0

# Step 4: Build scorecard
scorecard = pd.DataFrame({
    'KPI': [
        'Velocity ($/day)',
        'Win Rate (%)',
        'Avg Deal Size ($)',
        'Sales Cycle Length (days)'
    ],
    'Current': [
        round(velocity, 2),
        round(win_rate * 100, 1),
        round(avg_deal_size, 0),
        round(cycle_length, 1)
    ],
    'Target': [24000, 33, 20500, 45]
})

# Add Status (🟢 = on/above target, 🟡 = below)
def get_status(kpi, current, target):
    if kpi == 'Sales Cycle Length (days)':
        return '🟢' if current <= target else '🟡'
    else:
        return '🟢' if current >= target else '🟡'

scorecard['Status'] = scorecard.apply(lambda x: get_status(x['KPI'], x['Current'], x['Target']), axis=1)

# Step 5: Generate HTML web page
html_page = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Sales Velocity Scorecard</title>
  <style>
    body {{
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: #f3f5fa;
      color: #333;
      padding: 20px;
    }}
    .container {{
      max-width: 900px;
      margin: auto;
      background: white;
      padding: 30px;
      border-radius: 14px;
      box-shadow: 0 6px 20px rgba(0,0,0,0.1);
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
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 25px 0;
      font-size: 16px;
    }}
    th {{
      background-color: #1976D2;
      color: white;
      text-align: left;
      padding: 14px;
    }}
    td {{
      padding: 14px;
      border-bottom: 1px solid #eee;
    }}
    tr:hover {{
      background-color: #f8f9fd;
    }}
    .value {{
      font-weight: bold;
      text-align: right;
    }}
    .target {{
      color: #1976D2;
    }}
    .status {{
      font-size: 1.4em;
      text-align: center;
    }}
    .good {{
      color: #2E7D32;
    }}
    .warn {{
      color: #C62828;
    }}
    .summary-box {{
      background: #e3f2fd;
      border-left: 5px solid #1976D2;
      padding: 15px;
      margin: 20px 0;
      border-radius: 0 8px 8px 0;
      font-size: 15px;
    }}
    footer {{
      text-align: center;
      margin-top: 40px;
      color: #888;
      font-size: 12px;
    }}
    .highlight {{
      background-color: #fff3cd;
      padding: 2px 6px;
      border-radius: 4px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>📊 Sales Velocity Scorecard</h1>
      <p class="subtitle">Performance vs. Target | Updated {pd.Timestamp.now().strftime('%b %d, %Y')}</p>
    </header>

    <table>
      <thead>
        <tr>
          <th>KPI</th>
          <th class="value">Current</th>
          <th class="value target">Target</th>
          <th class="status">Status</th>
        </tr>
      </thead>
      <tbody>
"""

# Add rows to table
for _, row in scorecard.iterrows():
    status_class = "good" if row['Status'] == '🟢' else "warn"
    current = f"{row['Current']:,}" if 'Deal Size' in row['KPI'] else f"{row['Current']}"
    target = f"{row['Target']:,}" if 'Deal Size' in row['KPI'] else f"{row['Target']}"

    # Special formatting for %
    if 'Win Rate' in row['KPI']:
        current += "%"
        target += "%"
    elif 'Velocity' in row['KPI']:
        current = f"${float(row['Current']):,.0f}/day"
        target = f"${row['Target']}/day"
    elif 'Cycle Days' in row['KPI']:
        current += " days"
        target += " days"

    html_page += f"""
        <tr>
          <td><strong>{row['KPI']}</strong></td>
          <td class="value">{current}</td>
          <td class="value target">{target}</td>
          <td class="status {status_class}">{row['Status']}</td>
        </tr>
    """

html_page += """
      </tbody>
    </table>

    <div class="summary-box">
      <strong>Insight:</strong> 
      Sales Velocity = <span class="highlight">Opportunities × Win Rate × Avg Deal Size ÷ Cycle Length</span>. 
      Improve any lever to increase revenue output.
    </div>

    <footer>
      Powered by Python & Pandas • Sales Science Engine • Generated on """ + pd.Timestamp.now().strftime('%Y-%m-%d %H:%M') + """
    </footer>
  </div>
</body>
</html>
"""

# Step 6: Save and download
with open("sales_velocity_scorecard.html", "w") as f:
    f.write(html_page)

print("✅ Web page generated: sales_velocity_scorecard.html")
files.download("sales_velocity_scorecard.html")
