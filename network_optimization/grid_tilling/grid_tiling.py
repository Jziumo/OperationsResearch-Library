import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
import matplotlib.font_manager as fm

grid_file_path = './network_ps2/example_grid.txt'
font_path = './fonts/BRIANNETOD.TTF'
font_prop = fm.FontProperties(fname=font_path)

def readGrid(file_path=grid_file_path):
    # read the file to a embedded list
    with open(file_path, 'r') as f:
        lines = f.readlines()
        # split by ','
        lines = [line.split(',') for line in lines]
        # to integer
        grid = [[int(x) for x in line] for line in lines]

    return grid

def getGraph(grid):
    m, n = len(grid), len(grid[0])
    G = nx.Graph()

    for r in range(m):
        for c in range(n):
            if grid[r][c] == 1:  # Only add nodes where there are filled cells
                G.add_node((r, c))
                # Connect to the left
                if c > 0 and grid[r][c - 1] == 1:
                    G.add_edge((r, c), (r, c - 1))
                # Connect to the top
                if r > 0 and grid[r - 1][c] == 1:
                    G.add_edge((r, c), (r - 1, c))
    return G

def drawGrid(grid):
    m, n = len(grid), len(grid[0])
    G = nx.Graph()

    # Add nodes and edges for the grid
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 1:  # Only add nodes where there are filled cells
                G.add_node((r, c))
                # Connect to the left
                if c > 0 and grid[r][c - 1] == 1:
                    G.add_edge((r, c), (r, c - 1))
                # Connect to the top
                if r > 0 and grid[r - 1][c] == 1:
                    G.add_edge((r, c), (r - 1, c))

    # Draw the graph
    plt.figure(figsize=(6, 6))
    pos = {(r, c): (c, -r) for r, c in G.nodes()}  # Adjust positions to match grid 
    nx.draw(G, pos, with_labels=False, node_size=300, node_color="black", edge_color="gray")
    
    plt.title("Grid Network Representation")
    plt.show()
    return

def drawBipartite(grid, red_nodes, blue_nodes):
    m, n = len(grid), len(grid[0])

    G = nx.Graph()

    # Add nodes and edges for the grid
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 1:  # Only add nodes where there are filled cells
                G.add_node((r, c))
                # Connect to the left
                if c > 0 and grid[r][c - 1] == 1:
                    G.add_edge((r, c), (r, c - 1))
                # Connect to the top
                if r > 0 and grid[r - 1][c] == 1:
                    G.add_edge((r, c), (r - 1, c))

    # Draw the graph
    plt.figure(figsize=(6, 6))
    pos = {(r, c): (c, -r) for r, c in G.nodes()}  # Adjust positions to match grid 
    color_map = ["red" if (r, c) in red_nodes else "blue" for (r, c) in G.nodes()]
    nx.draw(G, pos, with_labels=False, node_size=300, node_color=color_map, edge_color="gray")

    # show the number of red and blue nodes
    plt.text(4, 0, f"Red nodes number: {len(red_nodes)}", fontproperties=font_prop, fontsize=12, color='red', ha='left')
    plt.text(4, -0.4, f"Blue nodes number: {len(blue_nodes)}", fontproperties=font_prop, fontsize=12, color='blue', ha='left')
    
    plt.title("Grid Network Representation")
    plt.show()
    return

def bfsDye(grid, start=(2, 0)):
    red_nodes = []
    blue_nodes = []
    
    m, n = len(grid), len(grid[0])

    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
    visit = set()  # To track visited nodes
    queue = deque([start])  # BFS queue
    visit.add(start)  # Mark start as visited
    # True for red, false for blue
    current_color = True 

    while queue:
        level_size = len(queue)
        for i in range(level_size):
            r, c = queue.popleft()
            if current_color:
                red_nodes.append((r, c))
            else:
                blue_nodes.append((r, c))
            
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc  # Neighboring cell
                
                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1 and (nr, nc) not in visit:
                    queue.append((nr, nc))
                    visit.add((nr, nc))

        current_color = not current_color  # Switch color

    return red_nodes, blue_nodes

def findPerfectMatching(G, red_nodes):
    
    def dfs(u, visited):
        matching = {}
        for v in G[u]:  # Iterate over adjacent nodes
            if v not in visited:
                visited.add(v)
                if v not in matching or dfs(matching[v], visited):
                    matching[v] = u
                    matching[u] = v
                    return True, matching
        return False, None

    # Try to find matches for every node in the left partition
    for node in red_nodes:
        visit = set()
        found, matching = dfs(node, visit)
        if found == True:
            return matching
        else:
            return None

    return None

def main(): 
    grid = readGrid()
    G = getGraph(grid)
    drawGrid(grid)
    red_nodes, blue_nodes = bfsDye(grid)
    # print(red_list)
    # print(blue_nodes)
    # drawBipartite(grid, red_nodes=red_nodes, blue_nodes=blue_nodes)
    matching = findPerfectMatching(G, red_nodes=red_nodes)
    print(matching)
    
    return

if __name__ == '__main__':
    main()