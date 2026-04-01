import sys
import os
import time
import random
import statistics
import matplotlib.pyplot as plt

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from person1.astar import (
    load_graph,
    preprocess_graph,
    get_connected_graph,
    compute_astar_path
)

from person2.bfs_dfs import run_bfs, run_dfs


# ---------------- RUN EXPERIMENT ----------------
def run_analysis(num_runs=30):
    G = load_graph()
    G = preprocess_graph(G)
    G = get_connected_graph(G)

    nodes = list(G.nodes)

    astar_times = []
    bfs_times = []
    dfs_times = []

    for _ in range(num_runs):
        start, goal = random.sample(nodes, 2)

        # A*
        t0 = time.time()
        compute_astar_path(G, start, goal)
        astar_times.append(time.time() - t0)

        # BFS
        t0 = time.time()
        run_bfs(G, start, goal)
        bfs_times.append(time.time() - t0)

        # DFS
        t0 = time.time()
        run_dfs(G, start, goal)
        dfs_times.append(time.time() - t0)

    return astar_times, bfs_times, dfs_times


# ---------------- METRICS ----------------
def compute_metrics(times):
    return {
        "average": sum(times) / len(times),
        "minimum": min(times),
        "maximum": max(times),
        "std_dev": statistics.stdev(times)
    }


# ---------------- PRINT RESULTS ----------------
def print_analysis(name, metrics):
    print(f"\n{name} ANALYSIS:")
    print(f"Average Time: {metrics['average']:.6f} sec")
    print(f"Minimum Time (Best Case): {metrics['minimum']:.6f} sec")
    print(f"Maximum Time (Worst Case): {metrics['maximum']:.6f} sec")
    print(f"Standard Deviation: {metrics['std_dev']:.6f}")


# ---------------- VISUALIZATION ----------------
def plot_visual_analysis(astar_metrics, bfs_metrics, dfs_metrics):
    labels = ["A*", "BFS", "DFS"]
    colors = ['#7ED37E', '#FF8C5A', '#8FB6C4']

    avg_times = [
        astar_metrics["average"],
        bfs_metrics["average"],
        dfs_metrics["average"]
    ]

    std_devs = [
        astar_metrics["std_dev"],
        bfs_metrics["std_dev"],
        dfs_metrics["std_dev"]
    ]

    min_times = [
        astar_metrics["minimum"],
        bfs_metrics["minimum"],
        dfs_metrics["minimum"]
    ]

    max_times = [
        astar_metrics["maximum"],
        bfs_metrics["maximum"],
        dfs_metrics["maximum"]
    ]

    # -------- Average Time --------
    plt.figure()
    plt.bar(labels, avg_times, color=colors)
    plt.title("Average Execution Time Comparison")
    plt.xlabel("Algorithms")
    plt.ylabel("Time (seconds)")
    plt.savefig("average_time.png")
    plt.show()

    # -------- Std Dev (Error Bars) --------
    plt.figure()
    plt.bar(labels, avg_times, yerr=std_devs, capsize=5, color=colors)
    plt.title("Execution Time with Variability (Std Dev)")
    plt.xlabel("Algorithms")
    plt.ylabel("Time (seconds)")
    plt.savefig("std_dev_comparison.png")
    plt.show()

    # -------- Min vs Max --------
    plt.figure()
    x = range(len(labels))

    plt.plot(x, min_times, marker='o', color='#4CAF50', label="Minimum Time")
    plt.plot(x, max_times, marker='o', color='#E74C3C', label="Maximum Time")

    plt.xticks(x, labels)
    plt.title("Best Case vs Worst Case Performance")
    plt.xlabel("Algorithms")
    plt.ylabel("Time (seconds)")
    plt.legend()

    plt.savefig("min_max_comparison.png")
    plt.show()

# ---------------- MAIN ----------------
if __name__ == "__main__":
    astar, bfs, dfs = run_analysis(30)

    astar_metrics = compute_metrics(astar)
    bfs_metrics = compute_metrics(bfs)
    dfs_metrics = compute_metrics(dfs)

    print("\n========== PERFORMANCE ANALYSIS ==========")

    print_analysis("A*", astar_metrics)
    print_analysis("BFS", bfs_metrics)
    print_analysis("DFS", dfs_metrics)

    # Generate graphs
    plot_visual_analysis(astar_metrics, bfs_metrics, dfs_metrics)