# Maximum Cut for Tree

## Problem Description

In the maximum cut problem, we are given an undirected, weighted network $G = (V, E)$, and our goal is to ﬁnd a subset $S ⊂ V$ that maximizes the sum of the weights of all the edges crossing $S$, that is, we want to solve the problem, 

$$
\text{maximize}_{s\subset V} \quad \sum_{(i,j) \in E : i \in S, j \notin S}
$$
Show how to solve the maximum cut problem optimally when $G$ is a **tree**.

## Convert the Problem

**Conclusion:** the maximum cut value of a tree is equal to the sum of the weights of all edges in $G$, i.e., 
$$
\max(\sum_{(i,j) \in E : i \in S, j \notin S} c_{ij}) = \sum_{(u,v)\in E} c_{uv}
$$
**Proof.** 

A tree can be seem as a bipartite, so any pair of two adjacent nodes can be divided into two different sets. 

Thus, every edge can contribute to the cut. 

**Algorithm to find maximum cut:** 

To compute the maximum cut value, we can simply sum the weights of all edges, since every edge contributes to the cut. 

To determine the subset $S$, we can use a leveling traverse strategy based on Breadth-First Search (BFS) to assign nodes into two sets, and one of these two sets can be chosen as $S$.  

## Implementation

See [Code](./maximum_cut_tree.py) here. 

Here's the core function `bfsDye()` for partitioning the nodes into two sets: 

```python
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
```

## Example Results

Excute the file: 

```
python .\network_ps4\maximum_cut_tree.py
```

Below is an example tree with weighted edges, 

```
u, v, weight
1, 2, 3
1, 3, 4
2, 4, 2
2, 5, 1
```

Here is the result: 

```
nodes in S: [1, 4, 5]
nodes in V\S: [2, 3]
maximum cut: 10
```

