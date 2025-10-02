from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

def user_interaction(): 
    
    pass

def get_directed_option():
    """Get the user's option of a directed or undirected graph.
    """
    completer = WordCompleter(['directed', 'undirected'], ignore_case=True)
    session = PromptSession("Enter graph type (directed/undirected) [d/u]: \n>> ", completer=completer)
    print('\n')
    
    while True:
        graph_type = session.prompt().strip().lower()
        # Accept the abbreviation. 
        if graph_type == 'd': 
            graph_type = 'directed'
        elif graph_type == 'u': 
            graph_type = 'undirected'

        if graph_type in ['directed', 'undirected']:
            # print out confirm messages
            print(f'You select {graph_type} graph. ')
            return graph_type
        else:
            print("Invalid input. Please type 'directed', 'undirected', 'd' or 'u'.\n")

def get_weighted_option():
    """Get the user's option of a weighted or unweighted graph. 
    """
    completer = WordCompleter(['weighted', 'unweighted'], ignore_case=True)
    session = PromptSession("Enter whether the graph is weighted (weighted/unweighted) [w/u]: \n>> ", completer=completer)
    print('\n')

    while True:
        weighted = session.prompt().strip().lower()
        # Accept the abbreviation. 
        if weighted == 'w': 
            weighted = 'weighted'
        elif weighted == 'u': 
            weighted = 'unweighted'
        
        if weighted in ['directed', 'undirected']:
            # print out confirm messages
            print(f'You select {weighted} graph. ')
            return weighted
        else:
            print("Invalid input. Please type 'weighted', 'unweighted', 'w' or 'u'.\n")


if __name__ == '__main__': 
    # Example usage
    graph_type = get_directed_option()
    print(f"Selected graph type: {graph_type}")