import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Circle
import numpy as np

# Enhanced Theory Mapping
theories_full = {
    "Senge": "Stewardship",
    "Meadows": "Leverage Points",
    "Wheatley": "Self-Organization",
    "Taleb": "Antifragility",
    "Stacey": "Sense-making"
}

anchors = ["Legitimacy", "Responsibility", "Influence"]

# Colors - Ascendia-Inspired Dark Theme
bg_color = "#12151B"
node_theory_color = "#00E4AB"      # Vibrant teal for theories
node_anchor_color = "#F2A900"      # Warm gold for anchors
edge_color = "#D7DCE3"
text_color = "#FBF8EF"
highlight_color = "#F2003C"        # For emphasis

# Create graph
G = nx.Graph()

# Add nodes with attributes
for t in theories_full:
    G.add_node(t, group="Theory", label=t, title=theories_full[t])

for a in anchors:
    G.add_node(a, group="Anchor", label=a, title=a)

# Add edges
edges = [
    ("Senge", "Responsibility"),
    ("Meadows", "Responsibility"),
    ("Wheatley", "Influence"),
    ("Taleb", "Influence"),
    ("Stacey", "Legitimacy"),
    ("Stacey", "Influence")
]
G.add_edges_from(edges)

# Layout: Place anchors in a triangle, theories inside
pos = {}

# Circular layout for anchors
anchor_pos = nx.circular_layout(anchors, scale=1.0, center=(0, 0))
for a in anchors:
    pos[a] = anchor_pos[a] * 1.8  # Spread out

# Place theories near center, slightly offset for clarity
theta = np.linspace(0, 2*np.pi, len(theories_full)+1)[:-1]
for i, t in enumerate(theories_full):
    r = 0.8
    angle = theta[i]
    pos[t] = np.array([r * np.cos(angle), r * np.sin(angle)])

# Styling
plt.figure(figsize=(12, 10), dpi=150)
ax = plt.gca()
ax.set_facecolor(bg_color)
plt.gcf().set_facecolor(bg_color)

# Draw edges with curvature
for edge in G.edges():
    start = pos[edge[0]]
    end = pos[edge[1]]
    # Use slight curve for visual separation
    arc_radius = 0.2
    nx.draw_networkx_edges(G, pos, edgelist=[edge], 
                           edge_color=edge_color, 
                           width=2,
                           alpha=0.7,
                           ax=ax,
                           connectionstyle=f'arc3, rad={arc_radius * np.random.choice([-1,1])}',
                           arrows=False)

# Draw nodes
node_sizes = [5000 if G.nodes[n]['group'] == 'Theory' else 6000 for n in G.nodes]
node_colors = [node_theory_color if G.nodes[n]['group'] == 'Theory' else node_anchor_color for n in G.nodes]

nx.draw_networkx_nodes(G, pos, 
                       node_size=node_sizes, 
                       node_color=node_colors, 
                       edgecolors='white', 
                       linewidths=1.5, 
                       alpha=0.9, 
                       ax=ax)

# Labels
theory_labels = {t: f"{t}\n{theories_full[t]}" for t in theories_full}
anchor_labels = {a: a for a in anchors}
all_labels = {**theory_labels, **anchor_labels}

nx.draw_networkx_labels(G, pos, 
                        labels=all_labels, 
                        font_size=10, 
                        font_family='sans-serif',
                        font_weight='bold',
                        bbox=dict(boxstyle="round, pad=0.3", 
                                  facecolor=bg_color, 
                                  edgecolor='none', 
                                  alpha=0.85),
                        verticalalignment='center',
                        horizontalalignment='center',
                        fontcolor=text_color)

# Legend
theory_patch = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=node_theory_color, markersize=12, label='Leadership Theory')
anchor_patch = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=node_anchor_color, markersize=12, label='Core Anchor')

legend = ax.legend(handles=[theory_patch, anchor_patch], 
                   loc='upper right', 
                   fontsize=11,
                   frameon=True,
                   fancybox=True,
                   shadow=False,
                   facecolor=bg_color,
                   edgecolor='none',
                   labelcolor=text_color)
legend.get_frame().set_alpha(0.1)

# Title & Subtitle
plt.title("Systems Leadership: Theories Mapped to Foundational Anchors", 
          fontsize=16, 
          fontweight='bold', 
          color=text_color, 
          pad=20,
          fontfamily='Montserrat')

plt.figtext(0.5, 0.90, "Connecting seminal frameworks to principles of legitimacy, responsibility, and influence", 
            fontsize=11, 
            color='#AEB6C2', 
            ha='center', 
            fontfamily='Inter')

# Annotation: Highlight Stacey's dual connection
stacey_pos = pos['Stacey']
ax.annotate('Dual influence\non legitimacy\nand influence', 
            xy=stacey_pos, 
            xytext=(-100, 50), 
            textcoords='offset points',
            bbox=dict(boxstyle="round,pad=0.4", facecolor=highlight_color, alpha=0.2, edgecolor=highlight_color),
            arrowprops=dict(arrowstyle='->', color=highlight_color, alpha=0.7),
            fontsize=9,
            color='white',
            ha='center')

# Remove axes
ax.axis('off')
plt.tight_layout()

# Save high-quality image
plt.savefig("systems_leadership_map.png", dpi=300, bbox_inches='tight', facecolor=bg_color, edgecolor='none')

# Show
plt.show()