import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

def get_zoom_limits(pos,path,margin=0.0005):
    """
    Calculate zoom limits for a given path
    """
    xs = [pos[n][0] for n in path]
    ys = [pos[n][1] for n in path]

    return (min(xs)-margin, max(xs)+margin, min(ys)-margin, max(ys)+margin)

def visualize_full_graph(G, pos, start, goal, astar_path):

    """
    Draw the full graph with the A* path highlighted
    """
    plt.figure(figsize=(12,12))

    nx.draw(
        G.to_undirected(),
        pos,
        node_size=2,
        edge_color="#bbbbbb",
        width=0.7,
        alpha=1
    )

    path_edges = list(zip(astar_path, astar_path[1:]))

    nx.draw_networkx_edges(
        G.to_undirected(),
        pos,
        edgelist=path_edges,
        edge_color='blue',
        width=4,
        alpha=0.7
    )

    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=[start],
        node_color='green',
        node_size=120
    )

    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=[goal],
        node_color='red',
        node_size= 120
    )

    plt.title("Full Campus Route using A*")
    plt.axis('off')
    plt.savefig("full_campus_route.png", dpi=300,bbox_inches='tight')
    plt.show()

#from person1 import astar
def visualize_paths(G, pos,start,goal,astar_path,bfs_path,dfs_path):
    """Draw zoomed in views of the paths found by A*, BFS, and DFS
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 6)) 

    def draw_subplot(ax,path,title,color):
        nx.draw(
            G.to_undirected(),
            pos,
            node_size=3,
            edge_color="#bbbbbb",
            width =0.7,
            alpha=1,
            ax=ax
        )

        edges=list(zip(path, path[1:])) 
        nx.draw_networkx_edges(G.to_undirected(), 
                               pos,
                            edgelist=edges,
                            edge_color=color,
                            width=4,
                            alpha=0.7,
                            ax=ax)

        nx.draw_networkx_nodes(G, 
                           pos, 
                           nodelist=[start,goal], 
                           node_color=['green','red'], 
                           node_size=150, 
                           ax=ax)   
        
        xmin, xmax, ymin, ymax = get_zoom_limits(pos, path)
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)         
        ax.set_title(title)
        ax.axis('off')  

    draw_subplot(axes[0], astar_path, "A* Path", 'blue')
    draw_subplot(axes[1], bfs_path, "BFS Path", 'green')
    draw_subplot(axes[2], dfs_path, "DFS Path", 'orange')
    astar_legend = mlines.Line2D([], [], color='blue', linewidth=4, label='A* Path')
    bfs_legend   = mlines.Line2D([], [], color='green', linewidth=4, label='BFS Path')
    dfs_legend   = mlines.Line2D([], [], color='orange', linewidth=4, label='DFS Path')

    fig.legend(handles=[astar_legend, bfs_legend, dfs_legend], loc='upper center',bbox_to_anchor=(0.5, 1.0), ncol=3,fontsize=11)
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig("algorithm_comparison.png", dpi=300,bbox_inches="tight")
    plt.show()


if __name__ == "__main__":

    import networkx as nx

    G = nx.read_graphml("person1/mit_clean.graphml")

    pos = {
        n: (float(G.nodes[n]['x']),
            float(G.nodes[n]['y']))
        for n in G.nodes
    }

    nodes = list(G.nodes)

    start = nodes[0]
    goal = nodes[-1]

    # TEMP dummy paths
    astar_path = nx.shortest_path(G, start, goal)
    bfs_path = astar_path[::-1]
    dfs_path = astar_path[:]

    visualize_full_graph(G, pos, start, goal, astar_path)

    visualize_paths(G, pos, start, goal,
                    astar_path, bfs_path, dfs_path)







