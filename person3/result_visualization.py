import matplotlib.pyplot as plt

def compare_path_lengths(astar_len,bfs_len,dfs_len):
    algorithms=['A*', 'BFS', 'DFS']
    lengths=[astar_len,bfs_len,dfs_len]
    plt.figure(figsize=(8,6))
    plt.bar(algorithms, lengths, color=['blue', 'green', 'orange'])
    plt.xlabel('Algorithms')
    plt.ylabel('Path Length')
    plt.title('Comparison of Path Lengths')
    plt.savefig('path_length_comparison.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    compare_path_lengths(120,180,250)