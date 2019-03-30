import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import networkx as nx
import random as rd
import numpy as np

#-------------------------
# WATTS-STROGATZ MODEL
# grid structure
#-------------------------

# num_nodes = 30 # number of nodes

# def initialize(n = num_nodes):
#     global g
#     g = nx.Graph()
#     #determining how many nodes to plot and the grid
#     #dimensions for a nice rectangular grid
#     width = np.ceil(np.sqrt(n))
#     height = np.floor(np.sqrt(n))
#     n = width * height

#     for i in range(int(n)):
#         if not (i < width):
#             g.add_edge(i, i - width)    #adds vertical connections   

#         if i % width != 0:      
#             g.add_edge(i, i - 1)        #adds horizontal connections
     
#     g.pos = nx.spring_layout(g)
#     g.count = 0

# def observe():
#     global g
#     cla()
#     nx.draw(g, pos = g.pos)
#     plt.show()

# def update():
#     global g
#     g.count += 1
#     if g.count % 20 == 0: # rewiring once in every 20 steps
#         nds = list(g.nodes)
#         i = rd.choice(nds)
#         if g.degree[i] > 0:
#             g.remove_edge(i, rd.choice(list(g.neighbors(i))))
#             nds.remove(i)
#             for j in g.neighbors(i):
#                 nds.remove(j)
#             g.add_edge(i, rd.choice(nds))

#     # simulation of node movement
#     g.pos = nx.spring_layout(g, pos = g.pos, iterations = 5)

# import pycxsimulator
# pycxsimulator.GUI().start(func=[initialize, observe, update])

#-------------------------
# BARABASI-ALBERT MODEL
#
#-------------------------

m0 = 5 # number of nodes in initial condition
m = 5 # number of edges per new node

def initialize():
    global g
    g = nx.complete_graph(m0)
    g.pos = nx.spring_layout(g)
    g.count = 0

def observe():
    global g
    cla()
    nx.draw(g, pos = g.pos)

def pref_select(nds):
    global g
    r = uniform(0, sum(g.degree(i) for i in nds))
    x=0
    for i in nds:
        x += g.degree[i]
        if r <= x:
            return i

def update():
    global g
    g.count += 1
    if g.count % 20 == 0: # network growth once in every 20 steps
        nds = list(g.nodes)
        newcomer = max(nds) + 1
        for i in range(m):
            j = pref_select(nds)
            g.add_edge(newcomer, j)
            nds.remove(j)
        g.pos[newcomer] = (0, 0)

    # simulation of node movement
    g.pos = nx.spring_layout(g, pos = g.pos, iterations = 5)

import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])
