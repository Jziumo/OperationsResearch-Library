import pandas as pd
from collections import deque

file_path = './network_ps4/example_tree.csv'

def readWeightedUndirectedGraph(file_path): 
    # read csv file
    df = pd.read_csv(file_path, header=0)
    
    # store data into the list of edges
    edges = []
    for i in range(df.shape[0]):
        edges.append([df.iloc[i,0], df.iloc[i,1], df.iloc[i,2]])

    return edges

# get adjacency list from edge list
def buildAdjList(edges): 
    adjList = {}
    for edge in edges:
        u = edge[0]
        v = edge[1]
        weight = edge[2]

        if u not in adjList:
            adjList[u] = []
        
        if v not in adjList:
            adjList[v] = []
        
        adjList[u].append((v, weight))
        adjList[v].append((u, weight))
        
    return adjList

# use leveling traverse based on BFS to color nodes (assign to two sets)
def bfsDye(adjList, start=0): 
    red_nodes = []
    blue_nodes = []
    
    visit = set()
    queue = deque([start])  # BFS queue
    visit.add(start)

    current_color = True

    while queue: 
        level_size = len(queue)
        for i in range(level_size):
            current = queue.popleft()
            
            if current_color:
                red_nodes.append(current)
            else: 
                blue_nodes.append(current)
            
            for (neighbor, weight) in adjList[current]:
                if neighbor not in visit:
                    queue.append(neighbor)
                    visit.add(neighbor)

        current_color = not current_color  # Switch color

    return red_nodes, blue_nodes

def getMaximumCut(edges):
    total_weight = 0
    for [u, v, weight] in edges:
        total_weight += weight
    return total_weight


def main(): 
    edges = readWeightedUndirectedGraph(file_path=file_path)
    adjList = buildAdjList(edges)

    red_nodes, blue_nodes = bfsDye(adjList, start=1)
    maximum_cut = getMaximumCut(edges)
    
    print(f'nodes in S: {red_nodes}')
    print(f'nodes in V\S: {blue_nodes}')
    print(f'maximum cut: {maximum_cut}')

    return 

if __name__ == '__main__':
    main()