import random
import networkx as nx
import matplotlib.pyplot as plt

g= nx.grid_graph([5,5])
state = random.choice(list(g.nodes()))
states = []
node_colors = {x:0 for x in g.nodes}
edge_colors = {x:0 for x in g.edges}
node_colors[state]=1
nx.draw(g,pos = {x:x for x in g.nodes()}, node_color = [node_colors[x] for x in g.nodes()],edge_color = [edge_colors[x] for x in g.edges()],
        width =3, cmap="jet")
for i in range(5):
    node_colors = {x:0 for x in g.nodes}
    edge_colors = {x:0 for x in g.edges}
    old_state = state
    states.append(state)   
    state = random.choice(list(g.neighbors(state)))
    edge_colors[(old_state, state)]= 1
    edge_colors[(state, old_state)]= 1
    node_colors[old_state] = 2
    node_colors[state]=1
    plt.figure()
    nx.draw(g,pos = {x:x for x in g.nodes()}, node_color = [node_colors[x] for x in g.nodes()],edge_color = [edge_colors[x] for x in g.edges()],
        width =3, cmap="jet")
    plt.show()
