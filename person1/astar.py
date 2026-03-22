import networkx as nx
import math
import os


# =========================
# LOAD GRAPH
# =========================
def load_graph():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "mit_campus.graphml")
    G = nx.read_graphml(file_path)
    return G


# =========================
# PREPROCESS GRAPH
# =========================
def preprocess_graph(G):
    for n in G.nodes:
        G.nodes[n]['x'] = float(G.nodes[n]['x'])
        G.nodes[n]['y'] = float(G.nodes[n]['y'])

    for u, v, d in G.edges(data=True):
        try:
            d['length'] = float(d.get('length', 1.0))
        except:
            d['length'] = 1.0

    return G


# =========================
# CONNECT GRAPH
# =========================
def get_connected_graph(G):
    largest_cc = max(nx.connected_components(G.to_undirected()), key=len)
    return G.subgraph(largest_cc).copy()


# =========================
# LABEL GENERATION
# =========================
def generate_label(index):
    label = ""
    while True:
        label = chr(ord('A') + (index % 26)) + label
        index = index // 26 - 1
        if index < 0:
            break
    return label


def label_nodes(G):
    for i, node in enumerate(G.nodes):
        G.nodes[node]['label'] = generate_label(i)
    return G


# =========================
# POSITION MAPPING
# =========================
def get_positions(G):
    return {n: (G.nodes[n]['x'], G.nodes[n]['y']) for n in G.nodes}


# =========================
# SAVE CLEAN GRAPH
# =========================
def save_graph(G, filename="mit_clean.graphml"):
    nx.write_graphml(G, filename)


# =========================
# LABEL ↔ NODE MAPPING
# =========================
def create_label_mappings(G):
    label_to_node = {}
    node_to_label = {}

    for n in G.nodes:
        label = G.nodes[n]['label']
        label_to_node[label] = n
        node_to_label[n] = label

    return label_to_node, node_to_label


# =========================
# HEURISTIC FUNCTION
# =========================
def heuristic(G, n1, n2):
    x1, y1 = G.nodes[n1]['x'], G.nodes[n1]['y']
    x2, y2 = G.nodes[n2]['x'], G.nodes[n2]['y']
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


# =========================
# A* PATH
# =========================
def compute_astar_path(G, start, goal):
    return nx.astar_path(
        G,
        start,
        goal,
        heuristic=lambda a, b: heuristic(G, a, b),
        weight='length'
    )


# =========================
# PATH LENGTH
# =========================
def compute_path_length(G, path):
    total_length = 0.0

    for u, v in zip(path, path[1:]):
        edge_data = G.get_edge_data(u, v)
        
        # Handle multigraph (sometimes multiple edges)
        if isinstance(edge_data, dict):
            edge_data = list(edge_data.values())[0]

        total_length += float(edge_data.get('length', 1.0))

    return total_length