import random
import networkx as nx
import matplotlib.pyplot as plt

g= nx.grid_graph([5,5])
scores = {x:1+x[0]+x[1] for x in g.nodes()}
visits = {x:0 for x in g.nodes()}
state = random.choice(list(g.nodes()))
states = []
node_colors = {x:0 for x in g.nodes}
edge_colors = {x:0 for x in g.edges}
node_colors[state]=1
nx.draw(g,pos = {x:x for x in g.nodes()}, node_color = [node_colors[x] for x in g.nodes()],edge_color = [edge_colors[x] for x in g.edges()],
        width =3, cmap="jet")
for i in range(10000):
    node_colors = {x:0 for x in g.nodes}
    edge_colors = {x:0 for x in g.edges}
    
    old_state = state
    states.append(state)
    visits[state]+=1
    
    proposal = random.choice(list(g.neighbors(state)))
    
    alpha = (scores[proposal]/scores[old_state])*(len(list(g.neighbors(old_state)))/len(list(g.neighbors(proposal))))
    
    if random.random() < alpha:
        state = proposal
    
    else:
        state = old_state
    
    
    
    edge_colors[(old_state, state)]= 1
    edge_colors[(state, old_state)]= 1
    node_colors[old_state] = 2
    node_colors[state]=1
    #plt.figure()
    #nx.draw(g,pos = {x:x for x in g.nodes()}, node_color = [node_colors[x] for x in g.nodes()],edge_color = [edge_colors[x] for x in g.edges()],
    #    width =3, cmap="jet")
    #plt.show()
    
    
plt.figure()
nx.draw(g,pos = {x:x for x in g.nodes()}, node_color = [visits[x] for x in g.nodes()],edge_color = [edge_colors[x] for x in g.edges()],
        width =3, cmap ="jet")
plt.show()
