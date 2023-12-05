import networkx as nx
import matplotlib.pyplot as plt
import heapq
import math
from random import randint


def a_star_search(graph, start, end):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    prec = {start: None}
    dist = {start: 0}
    pq = []
    heapq.heappush(pq, (0, start))

    while pq:
        curr = heapq.heappop(pq)[1]

        if curr == end:
            path = []
            while curr != start_node:
                path.append(curr)
                curr = prec[curr]
            path.append(start_node)
            path.reverse()
            
            path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            
            return path, path_edges, dist[end]

        for nxt in graph.neighbors(curr):
            nD = dist[curr] + 1
            if nxt not in dist or nD < dist[nxt]:
                prec[nxt] = curr
                dist[nxt] = nD
                heapq.heappush(pq, (nD + heuristic(end, nxt), nxt))

    return [], -1


def getRandomStartAndEnd(N):
    start_node = (randint(0, N), randint(0, N))
    end_node = (randint(0, N), randint(0, N))
    while end_node == start_node:
        end_node = (randint(0, N), randint(0, N))
    return start_node, end_node


if __name__ == "__main__":
    # Crate net graph
    N = 5
    G = nx.grid_2d_graph(N, N)
    
    # Add diagonals
    G.add_edges_from([
        ((x, y), (x+1, y+1))
        for x in range(N - 1)
        for y in range(N - 1)
    ] + [
        ((x+1, y), (x, y+1))
        for x in range(N - 1)
        for y in range(N - 1)
    ], weight=math.sqrt(2))
    
    # Get start and end and solve
    start_node, end_node = getRandomStartAndEnd(N - 1)
    path, path_edges, _ = a_star_search(G, start_node, end_node)

    # Node drawing options
    pos = {(x, y): (x, y) for x, y in G.nodes()}
    node_options = {
        "node_size": 100,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 1
    }

    # Draw all nodes and edges with default parameters
    nx.draw_networkx_nodes(G, pos, **node_options)
    nx.draw_networkx_edges(G, pos, edge_color="black", width=1)

    # Highlight the path nodes and edges in blue
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color="blue")
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="blue", width=2)

    # Highlight the start node in green and the end node in red
    nx.draw_networkx_nodes(G, pos, nodelist=[start_node], node_color="green")
    nx.draw_networkx_nodes(G, pos, nodelist=[end_node], node_color="red")
    
    # Annotate the path nodes with their coordinates
    for point in path:
        plt.text(point[0], point[1], str(point), fontsize=9, ha='right', va='bottom')

    # Turn off axis labels
    ax = plt.gca()
    ax.margins(0.05)
    plt.axis("off")
    plt.show()