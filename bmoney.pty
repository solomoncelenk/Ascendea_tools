
# Create a visual reference guide showing the layout structure
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(14, 10))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Color scheme
colors = {
    'navy': '#213052',
    'teal': '#5fc3db', 
    'teal_dark': '#417d9a',
    'white': '#ffffff',
    'gray': '#f1f5f9',
    'text': '#475569'
}

def draw_box(ax, x, y, width, height, color, text, text_color='white', alpha=1.0, radius=0.02):
    box = FancyBboxPatch((x, y), width, height, 
                         boxstyle=f"round,pad=0.02,rounding_size={radius}",
                         facecolor=color, edgecolor='none', alpha=alpha, zorder=2)
    ax.add_patch(box)
    ax.text(x + width/2, y + height/2, text, ha='center', va='center', 
            fontsize=9, color=text_color, weight='bold', wrap=True, zorder=3)

# Header
draw_box(ax, 0, 92, 100, 8, colors['navy'], 'PROPERTY PRINCIPLES - DEAL CRUNCH CALCULATOR', 
         colors['white'], radius=0)
ax.text(50, 96, 'Investment Grade Property Acquisition', ha='center', va='center', 
        fontsize=8, color=colors['teal'], weight='bold')

# Sidebar (inputs)
draw_box(ax, 0, 10, 20, 82, colors['gray'], '', colors['text'], alpha=0.5, radius=0)
ax.text(10, 88, 'INPUTS', ha='center', va='center', fontsize=10, color=colors['navy'], weight='bold')
ax.text(10, 84, '• Purchase Price\n• Deposit %\n• Interest Rate\n• Rent (Low/High)\n• Operating Costs\n• Assumptions', 
        ha='center', va='top', fontsize=7, color=colors['text'])

# 5 Metrics Cards (Top row)
metric_width = 15
start_x = 22
for i, metric in enumerate(['Gross Yield\n3.99%', 'Cash on Cash\n-1.74%', 'Total Return\n12.59%', 
                            'Net Profit\n10.86%', 'Equity\n$293K']):
    x = start_x + i * (metric_width + 1)
    draw_box(ax, x, 80, metric_width, 10, colors['white'], metric, colors['navy'], 
             alpha=0.95)
    # Add teal accent line
    accent = Rectangle((x, 88), metric_width, 2, facecolor=colors['teal'], zorder=3)
    ax.add_patch(accent)

# Tabs
draw_box(ax, 22, 72, 76, 6, colors['gray'], 'Deal Analysis | What If Scenario | Deposit Required', 
         colors['text'], alpha=0.3)

# Main content area - Split view
draw_box(ax, 22, 35, 37, 35, colors['white'], '', colors['text'], alpha=0.8)
ax.text(40.5, 68, 'CASH FLOW ANALYSIS', ha='center', va='center', fontsize=9, 
        color=colors['white'], weight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=colors['navy'], edgecolor='none'))
ax.text(40.5, 60, 'Monthly Rent: $1,800 - $2,200\nExpenses: $1,005 - $1,046\nMortgage: $1,416\nCash Flow: -$471 to -$38', 
        ha='center', va='center', fontsize=7, color=colors['text'])

# Right side - Acquisition costs
draw_box(ax, 61, 35, 37, 35, colors['white'], '', colors['text'], alpha=0.8)
ax.text(79.5, 68, 'ACQUISITION COSTS', ha='center', va='center', fontsize=9, 
        color=colors['white'], weight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=colors['navy'], edgecolor='none'))
ax.text(79.5, 58, 'Purchase: $586,000\nDeposit: $117,200\nStamp Duty: $30,230\nLMI: $0\nLegal: $2,000\nTotal Cash: $149,430', 
        ha='center', va='center', fontsize=7, color=colors['text'])

# What If Table Section
draw_box(ax, 22, 10, 76, 23, colors['white'], '', colors['text'], alpha=0.8)
ax.text(60, 31, 'WHAT IF SCENARIO ANALYSIS', ha='center', va='center', fontsize=9, 
        color=colors['white'], weight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=colors['navy'], edgecolor='none'))

# Table headers
headers = ['Scenario', 'Loan Amt', 'Interest', 'Cash Return']
for i, h in enumerate(headers):
    x = 24 + i * 18
    draw_box(ax, x, 26, 16, 3, colors['navy'], h, colors['white'], radius=0.01)

# Table rows (sample)
scenarios = [
    ('80% @ 6%', '$469K', '$28K', '-$16,790'),
    ('90% @ 6%', '$527K', '$32K', '-$20,306'),
    ('100% @ 7%', '$586K', '$41K', '-$29,682')
]

for row_idx, (scenario, loan, interest, cash) in enumerate(scenarios):
    y = 23 - row_idx * 4
    values = [scenario, loan, interest, cash]
    bg_color = colors['teal'] if '80%' in scenario else colors['white']
    text_color = colors['white'] if '80%' in scenario else colors['text']
    
    for col_idx, val in enumerate(values):
        x = 24 + col_idx * 18
        draw_box(ax, x, y, 16, 3.5, bg_color if col_idx == 0 else colors['white'], 
                val, colors['teal_dark'] if col_idx == 3 and '-' in val else text_color, 
                alpha=0.9 if col_idx == 0 else 0.7, radius=0.01)

# Footer
draw_box(ax, 0, 0, 100, 8, colors['gray'], 
         'Disclaimer: All calculations are estimates. Seek professional financial advice.\n© 2025 Property Principles | Investment Grade Property Acquisition', 
         colors['text'], alpha=0.5, radius=0)

# Title
plt.title('Property Principles Deal Crunch Simulator - Interface Preview', 
          fontsize=14, weight='bold', color=colors['navy'], pad=20)

# Legend/Color Key
legend_elements = [
    mpatches.Patch(facecolor=colors['navy'], label='Navy #213052 - Headers/Trust'),
    mpatches.Patch(facecolor=colors['teal'], label='Teal #5fc3db - Accents/Interactive'),
    mpatches.Patch(facecolor=colors['teal_dark'], label='Teal Dark #417d9a - Secondary'),
    mpatches.Patch(facecolor=colors['white'], label='White #ffffff - Cards/Background')
]
ax.legend(handles=legend_elements, loc='lower right', bbox_to_anchor=(0.98, 0.02), 
         fontsize=7, framealpha=0.9)

plt.tight_layout()
plt.savefig('/mnt/kimi/output/interface_preview.png', dpi=150, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
plt.show()

print("✅ Interface preview generated!")
