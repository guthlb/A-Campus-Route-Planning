import matplotlib.pyplot as plt
import pandas as pd

# ---------------- LOAD RESULTS ----------------
try:
    df = pd.read_csv("../person4/experiment_results.csv")
    print("Results loaded successfully")
except:
    print("Error: experiment_results.csv not found. Run Person 4 code first.")
    exit()

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
    ]
})

print("\nAverage Results:")
print(avg_results)

# ---------------- SAVE SUMMARY ----------------
avg_results.to_csv("summary_results.csv", index=False)
print("Summary saved to summary_results.csv")

# ---------------- GRAPHS ----------------

plt.figure()
plt.bar(avg_results["Algorithm"], avg_results["Avg Time (ms)"])
plt.title("Average Execution Time")
plt.xlabel("Algorithm")
plt.ylabel("Time (ms)")
plt.savefig("time_comparison.png")
plt.close()

plt.figure()
plt.bar(avg_results["Algorithm"], avg_results["Avg Path Cost"])
plt.title("Average Path Cost")
plt.xlabel("Algorithm")
plt.ylabel("Cost")
plt.savefig("cost_comparison.png")
plt.close()

plt.figure()
plt.bar(avg_results["Algorithm"], avg_results["Avg Path Length"])
plt.title("Average Path Length")
plt.xlabel("Algorithm")
plt.ylabel("Length")
plt.savefig("length_comparison.png")
plt.close()

plt.figure()
df[["astar_time","bfs_time","dfs_time"]].boxplot()
plt.title("Execution Time Distribution")
plt.ylabel("Time (ms)")
plt.savefig("distribution.png")
plt.close()

print("Graphs saved successfully!")

# ---------------- FINAL ANALYSIS ----------------
print("\n===== FINAL ANALYSIS =====")

fastest = avg_results.loc[avg_results["Avg Time (ms)"].idxmin(), "Algorithm"]
best_cost = avg_results.loc[avg_results["Avg Path Cost"].idxmin(), "Algorithm"]
shortest = avg_results.loc[avg_results["Avg Path Length"].idxmin(), "Algorithm"]

print(f"Fastest Algorithm: {fastest}")
print(f"Lowest Cost Path: {best_cost}")
print(f"Shortest Path Length: {shortest}")

print("\nConclusion:")
print("A* performs best due to heuristic optimization.")
print("BFS guarantees shortest path but may take more time.")
print("DFS is not suitable for shortest path problems.")