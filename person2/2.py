import networkx as nx
import matplotlib.pyplot as plt
import os

# ---------------- LOAD CLEAN GRAPH ----------------
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "../person1/mit_clean.graphml")
G = nx.read_graphml(file_path)
G = G.to_undirected()

print(f"Nodes: {len(G.nodes)}")
print(f"Edges: {len(G.edges)}")

# ---------------- CREATE LABEL MAP ----------------
def generate_label(index):
    label = ""
    while True:
        label = chr(ord('A') + (index % 26)) + label
        index = index // 26 - 1
        if index < 0:
            break
    return label

label_to_node = {}
node_to_label = {}

for i, node in enumerate(G.nodes):
    label = generate_label(i)
    label_to_node[label] = node
    node_to_label[node] = label

# ---------------- TAKE INPUT ----------------
print("\nEnter node labels (like A, B, AA, etc.)")

start_label = input("Enter START node: ").strip().upper()
goal_label = input("Enter GOAL node: ").strip().upper()

if start_label not in label_to_node or goal_label not in label_to_node:
    print("Invalid label entered!")
    exit()

start = label_to_node[start_label]
goal = label_to_node[goal_label]

print(f"\nStart: {start_label}")
print(f"Goal: {goal_label}")

# ---------------- POSITIONS ----------------
pos = {n: (float(G.nodes[n]['x']), float(G.nodes[n]['y'])) for n in G.nodes}

# ---------------- BFS ----------------
def run_bfs(G, start, goal):
    try:
        return nx.shortest_path(G, start, goal)
    except:
        return []

# ---------------- DFS ----------------
def run_dfs(G, start, goal):
    visited = set()
    stack = [(start, [start])]

    while stack:
        node, path = stack.pop()

        if node == goal:
            return path

        if node not in visited:
            visited.add(node)
            for neighbor in G.neighbors(node):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))

    return []

# ---------------- PATH COST ----------------
def path_cost(G, path):
    cost = 0
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]

        if isinstance(G[u][v], dict):
            edge_data = list(G[u][v].values())[0]
            cost += float(edge_data.get('length', 1.0))
        else:
            cost += float(G[u][v].get('length', 1.0))

    return cost

# ---------------- RUN ----------------
bfs_path = run_bfs(G, start, goal)
dfs_path = run_dfs(G, start, goal)

# ---------------- RESULTS ----------------
print("\n--- RESULTS ---")
print("BFS Nodes:", len(bfs_path), "| Cost:", round(path_cost(G, bfs_path), 2))
print("DFS Nodes:", len(dfs_path), "| Cost:", round(path_cost(G, dfs_path), 2))

# ---------------- VISUALIZATION ----------------
plt.figure(figsize=(10, 10))

# Base graph
nx.draw(G, pos, node_size=5, edge_color='lightgray', alpha=0.6)

# BFS
if bfs_path:
    nx.draw_networkx_edges(
        G, pos,
        edgelist=list(zip(bfs_path, bfs_path[1:])),
        edge_color='yellow',
        width=2,
        label="BFS"
    )

# DFS
if dfs_path:
    nx.draw_networkx_edges(
        G, pos,
        edgelist=list(zip(dfs_path, dfs_path[1:])),
        edge_color='blue',
        width=2,
        label="DFS"
    )

# Start & Goal
nx.draw_networkx_nodes(G, pos, nodelist=[start], node_color='green', node_size=80)
nx.draw_networkx_nodes(G, pos, nodelist=[goal], node_color='red', node_size=80)

# Labels only for start & goal
nx.draw_networkx_labels(G, pos, {
    start: start_label,
    goal: goal_label
}, font_size=10)

plt.title(
    f"BFS: {len(bfs_path)} nodes (Cost {round(path_cost(G, bfs_path),2)}) | "
    f"DFS: {len(dfs_path)} nodes (Cost {round(path_cost(G, dfs_path),2)})"
)

plt.legend()
plt.show()