import networkx as nx
import matplotlib.pyplot as plt
import random
import time
import pandas as pd
import os
import sys

# Allow imports from project root
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from person2.bfs_dfs import run_bfs, run_dfs
from person1.astar import (
    load_graph,
    preprocess_graph,
    get_connected_graph,
    compute_astar_path,
    compute_path_length
)

# ---------------- LOAD + PREPROCESS GRAPH ----------------
original_graph = load_graph()
original_graph = preprocess_graph(original_graph)
original_graph = get_connected_graph(original_graph)

# ---------- CONVERT TO SIMPLE UNDIRECTED GRAPH ----------
G = nx.Graph()

#  FIRST copy nodes with attributes
for node, data in original_graph.nodes(data=True):
    G.add_node(node, **data)

# THEN add edges with minimum weight
for u, v, data in original_graph.edges(data=True):
    w = float(data.get("length", 1.0))

    if G.has_edge(u, v):
        if w < G[u][v]["length"]:
            G[u][v]["length"] = w
    else:
        G.add_edge(u, v, length=w)

print("Graph loaded and cleaned")
print("Nodes:", len(G.nodes))
print("Edges:", len(G.edges))

# ---------------- EXPERIMENTS ----------------
NUM_RUNS = 20
nodes = list(G.nodes)

results = []

astar_success = 0
bfs_success = 0
dfs_success = 0

print("\nRunning experiments...\n")

for i in range(NUM_RUNS):
    start = random.choice(nodes)
    goal = random.choice(nodes)

    while start == goal: 
        goal = random.choice(nodes)

    # -------- A* --------
    t0 = time.perf_counter()
    
    astar_path = compute_astar_path(G, start, goal)
    astar_time = (time.perf_counter() - t0) * 1000
    astar_cost = compute_path_length(G, astar_path)
    astar_len = len(astar_path) - 1
    astar_success += 1
    

    # -------- BFS --------
    bfs_result = run_bfs(G, start, goal)
    bfs_time = bfs_result["time"]
    bfs_cost = bfs_result["cost"]
    bfs_len = len(bfs_result["path"]) - 1
    bfs_nodes=bfs_result["nodes_traversed"]
    bfs_success += 1

    # -------- DFS --------
    dfs_result = run_dfs(G, start, goal)
    dfs_time = dfs_result["time"]
    dfs_cost = dfs_result["cost"]
    dfs_len = len(dfs_result["path"]) - 1
    dfs_nodes=dfs_result["nodes_traversed"]
    dfs_success += 1
    

    # -------- STORE RESULTS --------
    results.append({
        "astar_time": astar_time,
        "astar_cost": astar_cost,
        "astar_length": astar_len,

        "bfs_time": bfs_time,
        "bfs_cost": bfs_cost,
        "bfs_length": bfs_len,
        "bfs_nodes": bfs_nodes,

        "dfs_time": dfs_time,
        "dfs_cost": dfs_cost,
        "dfs_length": dfs_len,
        "dfs_nodes": dfs_nodes
    })

print("Experiments finished")

# ---------------- RESULTS TABLE ----------------
df = pd.DataFrame(results)
print("\nResults Table:")
print(df)

# ---------------- AVERAGE RESULTS ----------------
avg_results = pd.DataFrame({
    "Algorithm": ["A*", "BFS", "DFS"],
    "Avg Time (ms)": [
        df["astar_time"].mean(),
        df["bfs_time"].mean(),
        df["dfs_time"].mean()
    ],
    "Avg Path Cost": [
        df["astar_cost"].mean(),
        df["bfs_cost"].mean(),
        df["dfs_cost"].mean()
    ],
    "Avg Path Length": [
        df["astar_length"].mean(),
        df["bfs_length"].mean(),
        df["dfs_length"].mean()
    ],
    "Avg Nodes Traversed": [
        None,
        df["bfs_nodes"].mean(),
        df["dfs_nodes"].mean()
    ],

    "Success Rate (%)": [
        astar_success / NUM_RUNS * 100,
        bfs_success / NUM_RUNS * 100,
        dfs_success / NUM_RUNS * 100
    ]
})

print("\nAverage Results:")
print(avg_results)

# ---------------- GRAPHS ----------------
plt.figure()
plt.bar(avg_results["Algorithm"], avg_results["Avg Time (ms)"])
plt.title("Average Execution Time Comparison")
plt.ylabel("Time (ms)")
plt.xlabel("Algorithm")
plt.show()

plt.figure()
plt.bar(avg_results["Algorithm"], avg_results["Avg Path Cost"])
plt.title("Average Path Cost Comparison(Distance)")
plt.ylabel("Cost(meters)")
plt.xlabel("Algorithm")
plt.show()

plt.figure()
plt.bar(avg_results["Algorithm"], avg_results["Avg Path Length"])
plt.title("Average Path Length Comparison(edges)")
plt.ylabel("Length(edges)")
plt.xlabel("Algorithm")
plt.show()

plt.figure()
plt.bar(["BFS","DFS"],[avg_results["Avg Nodes Traversed"][1],avg_results["Avg Nodes Traversed"][2]])
plt.title("Average Nodes Traversed Comparison")
plt.ylabel("Nodes Traversed")
plt.xlabel("Algorithm")
plt.show()

plt.figure()
df[["astar_time","bfs_time","dfs_time"]].boxplot()
plt.title("Execution Time Distribution")
plt.ylabel("Time (ms)")
plt.show()