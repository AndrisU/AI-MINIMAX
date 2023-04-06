import networkx as nx
import matplotlib.pyplot as plt

def generate_game_tree(num, max_depth, game_tree=None, depth=0, player=1):
    if game_tree is None:
        game_tree = nx.DiGraph()

    game_tree.add_node(num, player=player)

    if depth == max_depth or num == 7:
        return game_tree

    for divisor in [2, 3, 4]:
        if num % divisor == 0:
            child_num = num // divisor
            if not game_tree.has_node(child_num):
                game_tree.add_node(child_num, player=-player)
            if not game_tree.has_edge(num, child_num):
                game_tree.add_edge(num, child_num, divisor=divisor)
            generate_game_tree(child_num, max_depth, game_tree, depth + 1, -player)

    return game_tree

def calculate_prob(game_tree, node, memo=None):
    if memo is None:
        memo = {}

    if node == 7:
        return 1.0
    if node in memo:
        return memo[node]

    children = list(game_tree.successors(node))
    if not children:
        return 0.0

    winning_probs = [calculate_prob(game_tree, child, memo) for child in children]
    memo[node] = max(winning_probs) if game_tree.nodes[node]['player'] == 1 else 1 - max(winning_probs)

    return memo[node]

def find_best_path(game_tree, node, memo=None):
    if node == 7:
        return [7]
    if memo is None:
        memo = {}

    children = list(game_tree.successors(node))
    if not children:
        return []

    winning_probs = [calculate_prob(game_tree, child, memo) for child in children]
    best_child = children[winning_probs.index(max(winning_probs))]
    return [node] + find_best_path(game_tree, best_child, memo)

initial_number = 21504
max_depth = 10  # Adjust as needed to control the depth of the game tree

game_tree = generate_game_tree(initial_number, max_depth)

# Calculate winning probabilities for each path and find the best path
winning_prob = calculate_prob(game_tree, initial_number)
print("Highest chance of the computer winning:", winning_prob)
best_path = find_best_path(game_tree, initial_number)
print("Best path for the computer:", best_path)

# Visualize the game tree
G_dot = nx.drawing.nx_pydot.to_pydot(game_tree)
G_dot.set('splines', 'true')  # Avoid arrows going through nodes
pos = nx.drawing.nx_pydot.graphviz_layout(game_tree, prog="dot", root=str(initial_number))

nx.draw(game_tree, pos, with_labels=True, node_size=800, font_size=10, font_weight='bold', node_color='lightblue', edge_color='gray')

# Draw the best path in red
if best_path:
    edges = [(best_path[i], best_path[i + 1]) for i in range(len(best_path) - 1)]
    nx.draw_networkx_edges(game_tree, pos, edgelist=edges, edge_color='red', width=2)

edge_labels = nx.get_edge_attributes(game_tree, 'divisor')
nx.draw_networkx_edge_labels(game_tree, pos, edge_labels=edge_labels, font_size=10)

plt.show()
