import os
import networkx as nx
import matplotlib.pyplot as plt

# =========================
# LOAD LABELED GRAPH
# =========================
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(base_dir, "data", "mit_labeled.graphml")

G = nx.read_graphml(path)

# =========================
# POSITIONS
# =========================
pos = {
    node: (float(data["x"]), float(data["y"]))
    for node, data in G.nodes(data=True)
}

# =========================
# LABELS
# =========================
labels = {}
seen = set()

for node, data in G.nodes(data=True):
    name = data.get("label")
    
    if name and name != "Unknown" and name not in seen:
        labels[node] = name
        seen.add(name)
# =========================
# PLOT
# =========================
plt.figure(figsize=(14,12))

nx.draw(G, pos, node_size=20, alpha=0.6)

nx.draw_networkx_labels(
    G,
    pos,
    labels=labels,
    font_size=6
)

plt.title("Labeled Campus Graph")
output_img = os.path.join(base_dir, "data", "labeledgraph.png")
plt.savefig(output_img, dpi=300)
print("Graph saved at:", output_img)