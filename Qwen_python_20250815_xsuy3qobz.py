# Step 1: Import libraries
import pandas as pd

# Step 2: Your original data
data = {
    'Rep': ['Alice', 'Bob', 'Charlie'],
    'Velocity': [19500, 17800, 20500],
    'Target': [20000, 20000, 20000]
}
df = pd.DataFrame(data)
df['Variance'] = df['Velocity'] - df['Target']
df['Variance %'] = (df['Variance'] / df['Target']) * 100
df['Variance %'] = df['Variance %'].round(1)  # Clean formatting

# Step 3: Identify underperformers
alerts = df[df['Variance %'] < -10]

# Step 4: Generate HTML page
html_page = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Rep Velocity Monitoring Dashboard</title>
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
    h1 {{
      text-align: center;
      color: #1976D2;
      margin-bottom: 10px;
    }}
    p.subtitle {{
      text-align: center;
      color: #666;
      font-style: italic;
      margin-bottom: 30px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
    }}
    th, td {{
      padding: 12px;
      text-align: left;
      border-bottom: 1px solid #ddd;
    }}
    th {{
      background-color: #1976D2;
      color: white;
    }}
    tr:hover {{
      background-color: #f5f5f5;
    }}
    .positive {{
      color: #2E7D32;
      font-weight: bold;
    }}
    .negative {{
      color: #C62828;
      font-weight: bold;
    }}
    .alert-box {{
      background: #ffebee;
      border: 1px solid #ef9a9a;
      border-radius: 8px;
      padding: 15px;
      margin: 20px 0;
      color: #c62828;
    }}
    .alert-box h3 {{
      margin-top: 0;
      color: #b71c1c;
    }}
    .all-good {{
      background: #e8f5e8;
      border: 1px solid #a5d6a7;
      border-radius: 8px;
      padding: 15px;
      text-align: center;
      color: #2e7d32;
      font-weight: bold;
    }}
    footer {{
      text-align: center;
      margin-top: 40px;
      color: #888;
      font-size: 12px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>📊 Rep Velocity Monitoring Dashboard</h1>
    <p class="subtitle">Real-time performance vs. target | Updated {pd.Timestamp.now().strftime('%b %d, %Y')}</p>

    <h2>Performance Overview</h2>
    <table>
      <thead>
        <tr>
          <th>Rep</th>
          <th>Velocity ($)</th>
          <th>Target ($)</th>
          <th>Variance ($)</th>
          <th>Variance %</th>
        </tr>
      </thead>
      <tbody>
"""

# Add table rows
for _, row in df.iterrows():
    var_class = "positive" if row['Variance'] >= 0 else "negative"
    html_page += f"""
        <tr>
          <td><strong>{row['Rep']}</strong></td>
          <td>${row['Velocity']:,.0f}</td>
          <td>${row['Target']:,.0f}</td>
          <td class='{var_class}'>${row['Variance']:,.0f}</td>
          <td class='{var_class}'>{row['Variance %']:+.1f}%</td>
        </tr>
    """

html_page += """
      </tbody>
    </table>

    <h2>⚠️ Alerts – Action Required</h2>
"""

# Add alerts
if alerts.empty:
    html_page += '<div class="all-good">✅ All reps are on or above target. No action needed.</div>'
else:
    html_page += f"""
    <div class="alert-box">
      <h3>🚨 Underperforming Reps (Below Target by >10%)</h3>
      <ul>
"""
    for _, row in alerts.iterrows():
        html_page += f"<li><strong>{row['Rep']}</strong>: {row['Variance %']:+.1f}% variance — coaching recommended</li>"
    html_page += """
      </ul>
    </div>
"""

# Close HTML
html_page += f"""
    <footer>
      Powered by Python & Pandas • Generated on {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}
    </footer>
  </div>
</body>
</html>
"""

# Step 5: Save HTML file
with open("rep_velocity_dashboard.html", "w") as f:
    f.write(html_page)

print("✅ Web page generated: rep_velocity_dashboard.html")

# Optional: Auto-download in Colab
from google.colab import files
files.download("rep_velocity_dashboard.html")