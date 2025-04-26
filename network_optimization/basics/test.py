import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def read_layout(file_path):
    """Read node positions from a text file and create a custom layout."""
    layout = {}
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                nodes = line.strip().split(",")
                for j, node in enumerate(nodes):
                    layout[node.strip()] = np.array([i, j])
    except FileNotFoundError:
        print("File not found.")
        return None
    return layout

def read_layout_from_string(str):
    """Read node positions from a text file and create a custom layout."""
    layout = {}
    lines = str.split("\n")
    for i, line in enumerate(lines):
        # print(line)
        nodes = line.strip().split(",")
        for j, node in enumerate(nodes):
            layout[node.strip()] = np.array([i, j])
            print(node, ':', i, j)
    return layout

def draw_flow_network_with_custom_layout(edges, layout):
    """Draw a flow network with a custom layout."""
    # Create a directed graph
    G = nx.DiGraph()

    # Add edges with weights
    for u, v, weight in edges:
        G.add_edge(u, v, weight=weight)

    # Draw the graph
    nx.draw(G, pos=layout, with_labels=True, node_size=1500, node_color='lightblue', linewidths=2, arrowsize=20)

    # Draw edge labels (weights)
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=edge_labels)

    # Show the plot
    plt.axis('off')
    plt.show()

# Example usage
edges = [
    ('s', 'a', 10),
    ('s', 'c', 10),
    ('a', 'c', 2),
    ('a', 'b', 4),
    ('a', 'd', 8),
    ('c', 'd', 9),
    ('d', 'b', 6),
    ('b', 't', 10),
    ('d', 't', 10)
]

# Simulate reading from a layout file
layout_file_content = 's\na, c\nb, d\nt'
layout = read_layout_from_string(layout_file_content)  # Use the helper function to parse layout

draw_flow_network_with_custom_layout(edges, layout)
