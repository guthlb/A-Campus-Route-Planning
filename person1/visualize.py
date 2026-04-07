import os
import networkx as nx
import matplotlib.pyplot as plt

# =========================
# LOAD GRAPH
# =========================
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(base_dir, "data", "mit_clean.graphml")

G = nx.read_graphml(path)

print("Graph loaded")

# =========================
# POSITIONS
# =========================
pos = {
    node: (float(data["x"]), float(data["y"]))
    for node, data in G.nodes(data=True)
}

# =========================
# LABELS (ONLY VALID ONES)
# =========================
labels = {
    node: data["label"]
    for node, data in G.nodes(data=True)
    if data.get("label") not in [None, "Unknown"]
}

print(f"Total labeled places: {len(labels)}")

# =========================
# DRAW GRAPH
# =========================
plt.figure(figsize=(20, 16))

# draw base graph
nx.draw(
    G,
    pos,
    node_size=15,
    alpha=0.4,
    edge_color="gray"
)

# highlight labeled nodes
nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=labels.keys(),
    node_color="skyblue",
    node_size=10
)

# draw labels
nx.draw_networkx_labels(
    G,
    pos,
    labels=labels,
    font_size=6,
    font_color="black",
    alpha=0.8  
)

plt.title("MIT Campus Graph (Unique Place Labels)")

# =========================
# SAVE IMAGE
# =========================
output_img = os.path.join(base_dir, "data", "labeled_map.png")
plt.savefig(output_img, dpi=300)

print("Saved image at:", output_img)