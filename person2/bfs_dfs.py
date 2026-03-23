# ---------------- WEIGHTED PATH COST ----------------
def compute_weighted_cost(G, path):
    total = 0.0

    for u, v in zip(path, path[1:]):
        edge_data = G.get_edge_data(u, v)

        if isinstance(edge_data, dict):
            total += float(edge_data.get("length", 1.0))
        else:
            total += float(edge_data)

    return total
# ---------------- BFS ----------------
def run_bfs(G, start, goal):
    from collections import deque
    import time

    start_time = time.perf_counter()

    visited = set()
    queue = deque([(start, [start])])
    nodes_traversed = 0

    while queue:
        node, path = queue.popleft()
        nodes_traversed += 1

        if node == goal:
            end_time = time.perf_counter()
            return {
                "path": path,
                "cost": compute_weighted_cost(G, path),
                "nodes_traversed": nodes_traversed,
                "time": round((end_time - start_time) * 1000, 4)  # ms
            }

        if node not in visited:
            visited.add(node)

            for neighbor in G.neighbors(node):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

    return None


# ---------------- DFS ----------------
def run_dfs(G, start, goal):
    import time
    #MAX_DEPTH = 40  
    start_time = time.perf_counter()

    visited = set()
    stack = [(start, [start])]
    nodes_traversed = 0

    while stack:
        node, path = stack.pop()
        nodes_traversed += 1

        if node == goal:
            end_time = time.perf_counter()
            return {
                "path": path,
                "cost": compute_weighted_cost(G, path),
                "nodes_traversed": nodes_traversed,
                "time": round((end_time - start_time) * 1000, 4)
            }

        if node not in visited:
            visited.add(node)

            for neighbor in G.neighbors(node):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))

    return None


# ---------------- USER TEST BLOCK ----------------
'''if __name__ == "__main__":
    import networkx as nx

    print("TEST MODE")

    # Small sample graph
    G = nx.Graph()
    G.add_edges_from([
        ('A', 'B'), ('A', 'C'),
        ('B', 'D'), ('C', 'D'),
        ('D', 'E')
    ])

    start = input("Enter START node: ").strip()
    goal = input("Enter GOAL node: ").strip()

    bfs_result = run_bfs(G, start, goal)
    dfs_result = run_dfs(G, start, goal)

    print("\n--- BFS RESULT ---")
    if bfs_result:
        print(bfs_result)
    else:
        print("No path found")

    print("\n--- DFS RESULT ---")
    if dfs_result:
        print(dfs_result)
    else:
        print("No path found")'''