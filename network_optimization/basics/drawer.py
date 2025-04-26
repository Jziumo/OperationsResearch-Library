import networkx as nx
import matplotlib.pyplot as plt 
import matplotlib.font_manager as fm
import os
import sys
import math
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

import readGraph

class Drawer: 
    """
    Draw the network. 
    """

    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        # Go up two levels to access fonts directory. 
        self.fonts_dir = os.path.join(self.BASE_DIR, '..', '..', 'fonts')  
        # Set the default fonts provided. 
        self.font_init()
        pass

    def draw_network(self, G : nx.Graph, figsize=(6,4.5), nx_layout='spring', custom_layers=None, with_labels=True, draw_edge_weight=True, node_size=600, node_color="#6677cc", edge_color="gray", edge_font_size=10, linewidths=1.0, font_size=13, font_family="Comic Code", arrowstyle='->', arrowsize=12): 
        """
        Draw the network with given parameters. 
        The network is represented by a networkX graph object. 

        Args:  
            G: The networkX graph object. 
        """
        # Assign positions based on given layout.
        pos = self.get_nx_pos(G, nx_layout) if custom_layers == None else self.get_custom_pos(layers=custom_layers)

        labels = {node: f'{node}' for node in G.nodes}
        font_color = FontColorChooser().choose_font_color(node_color)

        # Determine if the graph is weighted or not.
        weighted_graph = False
        for u, v, data in G.edges(data=True):
            if 'weight' in data: 
                weighted_graph = True

        # Modify the arrows parameters
        arrows = True
        if not nx.is_directed(G): 
            arrows = False 
            arrowstyle = '-|>’'

        # Draw the network
        plt.figure(figsize=figsize)
        nx.draw(G, pos, with_labels=with_labels, labels=labels, node_size=node_size, node_color=node_color, edge_color=edge_color, linewidths=linewidths, font_size=font_size, font_color=font_color, font_family=font_family, arrows=arrows, arrowstyle=arrowstyle, arrowsize=arrowsize)

        # If it is weighted graph, draw the edge weight.
        if weighted_graph and draw_edge_weight: 
            edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=edge_font_size, font_family=font_family)
        
        plt.title("Network Representation")
        plt.show()
        return 
    
    def draw_network_from_edges(self, edges : list, directed_graph=False, weighted_graph=False, figsize=(6,4.5), nx_layout='spring', custom_layers=None, with_labels=True, draw_edge_weight=True, node_size=600, node_color="#6677cc", edge_color="gray", edge_font_size=10, linewidths=1.0, font_size=13, font_family="Comic Code", arrowstyle='->', arrowsize=12): 
        """
        Draw the network with given parameters. 
        The network is represented by an edges list. 
        
        Args: 
            egdes: A list of edges. 
            directed_graph: indicates if the graph is directed. 
            weighted_graph: indicates if the graph is weighted. 
        """
        G = readGraph.get_nx_network(edges=edges, directed_graph=directed_graph, weighted_graph=weighted_graph)
        self.draw_network(G, figsize=figsize, nx_layout=nx_layout, custom_layers=custom_layers, with_labels=with_labels, draw_edge_weight=draw_edge_weight, node_size=node_size, node_color=node_color, edge_color=edge_color, edge_font_size=edge_font_size, linewidths=linewidths, font_size=font_size, font_family=font_family, arrowstyle=arrowstyle, arrowsize=arrowsize)
        return
    
    def draw_flow_network(self, G : nx.Graph, layers, start_color='#00FFFF', sink_color='#FF00FF', figsize=(6,4.5), with_labels=True, draw_edge_weight=True, node_size=600, node_color="#6677cc", edge_color="gray", edge_font_size=10, linewidths=1.0, font_size=13, font_family="Comic Code", arrowstyle='->', arrowsize=12): 
        """
        Draw the flow network where layers of vertices are required to specify. 
        The flow network must be a directed graph, but not necessary to be weighted. 
        The network is represented by a networkX graph object. 

        Args: 
            G: The networkX graph object. 
            layers: A list of layers. Each layer is a list of nodes in this layer. 
            
        """
        # Compute positions based on the given layers.
        pos = self.get_custom_pos(layers=layers)

        # Build the color list for all nodes.
        nodes_colors = []
        for node in G.nodes:
            if node in layers[0]:
                # If the node is the start
                nodes_colors.append(start_color)
            elif node in layers[-1]:
                # If the node is the sink
                nodes_colors.append(sink_color)
            else:
                # If the node is neither start nor sink
                nodes_colors.append(node_color)

        # Determine if the graph is weighted or not.
        weighted_graph = False
        for u, v, data in G.edges(data=True):
            if 'weight' in data: 
                weighted_graph = True

        # Modify the arrows parameters
        arrows = True
        if not nx.is_directed(G): 
            arrows = False 
            arrowstyle = '-|>’'

        # Draw the network without labels. 
        plt.figure(figsize=figsize)
        nx.draw(G, pos, with_labels=False, labels=None, node_size=node_size, node_color=nodes_colors, edge_color=edge_color, linewidths=linewidths, arrowstyle=arrowstyle, arrowsize=arrowsize)

        if with_labels: 
            # Labels for each node. 
            labels = {node: f'{node}' for node in G.nodes}
            # Font colors for the label text on each node. 
            font_color_map = {node: FontColorChooser().choose_font_color(nodes_colors[i]) for i, node in enumerate(G.nodes)}

            # Draw the labels of vertices.
            for node, label in labels.items():
                nx.draw_networkx_labels(G, pos, labels={node: label}, font_size=font_size, font_family=font_family, font_color=font_color_map[node])
        
        # If it is weighted graph, draw the edge weight.
        if weighted_graph and draw_edge_weight: 
            edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=edge_font_size, font_family=font_family)
        
        plt.title("Flow Network Representation")
        plt.show()
        return 
    
    def draw_flow_network_from_edges(self, edges : list, layers : list, weighted_graph=False,  start_color='#00FFFF', sink_color='#FF00FF', figsize=(6,4.5), with_labels=True, draw_edge_weight=True, node_size=600, node_color="#6677cc", edge_color="gray", edge_font_size=10, linewidths=1.0, font_size=13, font_family="Comic Code", arrowstyle='->', arrowsize=12): 
        """
        Draw the flow network where layers of vertices are required to specify. 
        The flow network must be a directed graph, but not necessary to be weighted. 
        The network is represented by a list of edges. 

        Args: 
            G: The networkX graph object. 
            layers: A list of layers. Each layer is a list of nodes in this layer. 
            
        """
        G = readGraph.get_nx_network(edges=edges, directed_graph=True, weighted_graph=weighted_graph)
        self.draw_flow_network(G=G, layers=layers, start_color=start_color, sink_color=sink_color, figsize=figsize, with_labels=with_labels, draw_edge_weight=draw_edge_weight, node_size=node_size, node_color=node_color, edge_color=edge_color, edge_font_size=edge_font_size, linewidths=linewidths, font_size=font_size, font_family=font_family, arrowstyle=arrowstyle, arrowsize=arrowsize)
        return
    
    def font_init(self):
        """
        Load the fonts under the directory './fonts'. 
        Fonts can be set at the parameters of `draw_network()` or `draw_flow_network()` function. 
        
        Current available fonts include: 
            - BRIANNETOD
            - Comic Code
            - Quicksand
        and other fonts installed on your system. 
        """
        fontnames = []
        fontpaths = []
        for filename in os.listdir(self.fonts_dir):
            filepath = os.path.join(self.fonts_dir, filename)
            if os.path.isfile(filepath):
                fontnames.append(filename.split('.')[0])
                fontpaths.append(filepath)

        for i in range(len(fontnames)):
            fontname = fontnames[i]
            fontpath = fontpaths[i]
            fm.fontManager.addfont(fontpath)
            plt.rcParams['font.family'] = fontname
        return

    
    def get_nx_pos(self, G, layout): 
        """
        Get positions provided by networkx library. 
        """
        options = {
            'spring': nx.spring_layout(G), 
            'plannar': nx.planar_layout(G)
        }
        return options[layout]
    
    def get_custom_pos(self, layers): 
        """
        Get positions given the layers of vertices from users.
        """
        n = len(layers)
        pos = {}
        x_space = math.sqrt(3)
        y_space = 2

        x_start = - (n - 1) * 1.0 * x_space / 2

        for i, layer in enumerate(layers):
            current_x = i * x_space + x_start
            layer_size = len(layer)
            y_start = (layer_size - 1) * 1.0 * y_space / 2
            for j, node in enumerate(layer): 
                current_y = y_start - j * y_space
                pos[node] = np.array([current_x, current_y])

        return pos

class FontColorChooser: 
    """
    Choose the foreground color (black/white) based on the background color. 
    """
    def __init__(self):
        pass

    def choose_font_color(self, color_hex):
        """Choose the font color to white or black based on the background color. 
        """
        rgb = tuple(int(color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

        luminance = self.calculate_luminance(rgb)
        
        # Choose the font color based on the luminance of the background color.
        if luminance > 0.179:
            return "#000000" 
        else:
            return "#FFFFFF"
        
    def calculate_luminance(self, rgb):
        """Calculate the luminance of given color. 
        """
        r, g, b = rgb
        r_linear = r / 255
        g_linear = g / 255
        b_linear = b / 255
        
        if r_linear <= 0.04045:
            r_linear /= 12.92
        else:
            r_linear = ((r_linear + 0.055) / 1.055) ** 2.4
            
        if g_linear <= 0.04045:
            g_linear /= 12.92
        else:
            g_linear = ((g_linear + 0.055) / 1.055) ** 2.4
            
        if b_linear <= 0.04045:
            b_linear /= 12.92
        else:
            b_linear = ((b_linear + 0.055) / 1.055) ** 2.4
            
        luminance = 0.2126 * r_linear + 0.7152 * g_linear + 0.0722 * b_linear
        return luminance


if __name__ == '__main__': 
    files_dir = './network_optimization/input_graph_examples/'
    # G = readGraph.get_nx_network(files_dir + 'flow_algorithm_example/flow_ex.csv', directed_graph=True, weighted_graph=True)
    layers = readGraph.read_layout_file(file_path=files_dir+'flow_complex_layout_example/layout.txt')
    G = readGraph.get_nx_network(files_dir + 'flow_complex_layout_example/flow.csv', directed_graph=True, weighted_graph=True)
    Drawer().draw_flow_network(G=G, layers=layers)

    G = readGraph.get_nx_network('./network_optimization/input/unweighted.csv', directed_graph=False, weighted_graph=False)
    Drawer().draw_network(G)
