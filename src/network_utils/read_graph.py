import pandas as pd
import networkx as nx

def read_graph_file(file_path, force_unweighted=False): 
    """Read the edges from .csv file and return the list of edges. 
    """
    df = pd.read_csv(file_path, header=0)

    # If the vertices are represented by string, make sure to delete whitespaces. 
    df.iloc[:, :2] = df.iloc[:, :2].applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Detect the number of columns to determine if the graph is weighted or not
    weighted_graph = True if df.shape[1] == 3 else False
    
    # If the user wants to force the graph to be unweighted, set the flag to False
    if force_unweighted: 
        weighted_graph = False
    
    # Store data into the list of edges
    edges = []
    for i in range(df.shape[0]):
        if weighted_graph:
            edges.append([df.iloc[i,0], df.iloc[i,1], df.iloc[i,2]])
        else: 
            edges.append([df.iloc[i,0], df.iloc[i,1]])

    return edges

def create_adj_list(edges, directed_graph=False):
    """
    Create an adjacency list based on the edges list. 
    """
    # determine if the graph is weighted or not
    weighted_graph = True if len(edges[0]) == 3 else False 

    adjList = {}
    
    for edge in edges: 
        u = edge[0]
        v = edge[1]
        # record the weight of the edge only if the graph is weighted
        weight = edge[2] if weighted_graph else 0
        
        if u not in adjList:
            adjList[u] = []
        
        if weighted_graph:
            adjList[u].append((v, weight))
        else:
            adjList[u].append(v)

        # If the graph is not directed, add the edge in the opposite direction
        if not directed_graph:
            if v not in adjList:
                adjList[v] = []

            if weighted_graph:
                adjList[v].append((u, weight))
            else:
                adjList[v].append(u)

    return adjList

def create_dist_matrix(edges, directed_graph=False):
    """
    Create a distance matrix (dict of dicts) from the list of edges.
    If the graph is unweighted, all weights default to 1.
    """
    weighted_graph = True if len(edges[0]) == 3 else False

    # Collect all nodes
    nodes = set()
    for edge in edges:
        nodes.add(edge[0])
        nodes.add(edge[1])
    nodes = list(nodes)

    # Initialize distance matrix with infinities
    dist = {u: {v: float('inf') for v in nodes} for u in nodes}
    for u in nodes:
        dist[u][u] = 0  # distance to self is 0

    # Fill in edge distances
    for edge in edges:
        u, v = edge[0], edge[1]
        w = edge[2] if weighted_graph else 1

        dist[u][v] = w
        if not directed_graph:
            dist[v][u] = w

    return dist

def get_adj_list(file_path, directed_graph=False, force_unweighted=False):
    """
    Get adjacency list from the file with given path. 
    """
    return create_adj_list(read_graph_file(file_path, force_unweighted), directed_graph)

def get_adj_list_from_edges(edges, directed_graph=False): 
    """
    Get adjacency list from the list of edges. 
    """
    return create_adj_list(edges=edges, directed_graph=directed_graph)

def get_dist_matrix_from_edges(edges, directed_graph=False): 
    """
    Get distance matrix (dict of dicts) from the list of edges. 
    """
    return create_dist_matrix(edges=edges, directed_graph=directed_graph)

def get_nx_network(file_path, directed_graph=False, weighted_graph=False):
    """
    Get NetworkX network object from the given file path. 
    """
    edges = read_graph_file(file_path, force_unweighted=False) if weighted_graph else read_graph_file(file_path, force_unweighted=True)
    G = nx.Graph() if not directed_graph else nx.DiGraph()

    if not weighted_graph:
        G.add_edges_from(edges)
    else:
        G.add_weighted_edges_from(edges)

    return G

def get_nx_network(edges, directed_graph=False, weighted_graph=False):
    """
    Get NetworkX network object from the given edges list. 
    """
    G = nx.Graph() if not directed_graph else nx.DiGraph()

    if not weighted_graph:
        G.add_edges_from(edges)
    else:
        G.add_weighted_edges_from(edges)

    return G


def read_layout_file(file_path): 
    """
    Read the user customized layout file. 
    """
    layers = []
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                layer_nodes = line.split(",")
                layer_nodes = [node.strip() for node in layer_nodes]
                layers.append(layer_nodes)
    except FileNotFoundError:
        print("File not found.")
        return None
    return layers


if __name__ == '__main__':
    # main()
    pass
