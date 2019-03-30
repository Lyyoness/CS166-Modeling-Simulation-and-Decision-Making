import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import networkx as nx
import random as rd

#----------------------
# PART 1
# SIS Model
#----------------------

n = 200		#nodes
p_e = 0.05	#connection probability
p_i = 0.04 	# infection probability
p_r = 0.5 	# recovery probability

def initialize():
    global g
    g = nx.erdos_renyi_graph(n, p_e)
    g.pos = nx.spring_layout(g)
    for i in g.nodes:
        g.nodes[i]['state'] = 1 if random() < .5 else 0

def observe():
    global g
    cla()
    nx.draw(g, vmin = 0, vmax = 1,
            node_color = [g.nodes[i]['state'] for i in g.nodes],
            pos = g.pos)

def update():
	'''
	Updated to account for simultaneous updating.
	'''
	global g
	all_nodes = list(g.nodes)

	for node in all_nodes:
		if g.nodes[node]['state'] == 0: 						# if susceptible
			neighbors = list(g.neighbors(node))
			for neig in neighbors:
				if g.nodes[neig]['state'] == 1: 				# if randomly chosen neighbor is infected
					g.nodes[neig]['state'] = 1 if random() < p_i else 0
				else: 													# if node is already infected
					g.nodes[neig]['state'] = 0 if random() < p_r else 1


import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])



#--------------------------------
# PART 2
# Friends of Friends Effect
#--------------------------------

# p_i = 0.04 	# infection probability
# p_r = 0.5 	# recovery probability
# n = 1000  	# we want 1000 nodes, ~20.000 connections

# def avg_degree(g, n):
# 	'''
# 	Calculates the average degree of a graph g 
# 	with n nodes. Edges*2/nodes
# 	'''
# 	total_edges = len(list(g.edges))
# 	avg_degr = total_edges * 2/ n

# 	print ("Total edges in the graph: ", total_edges)
# 	print ("Average degree: ", avg_degr)

# 	return avg_degr


# def avg_neighbor_degree(g):
# 	'''
# 	Iterates through all edges in the graph and all their attached
# 	nodes and calculates the average node degree.
# 	'''
# 	node_counter = 0
# 	total_degree = 0

# 	for edge in g.edges():
# 		for neighbor in edge:
# 			total_degree += len(g.edges(neighbor))
# 			node_counter += 1

# 	avg_neighbor_degr = total_degree/node_counter
# 	print ("Average neighbor degree: ", avg_neighbor_degr)
# 	return avg_neighbor_degr


# def generate_graph(graph_type='erdos'):
# 	if graph_type == "erdos":
# 		g = nx.erdos_renyi_graph(n, 0.04)			#edges = (n chose 2) * p_e
# 	elif graph_type == "watts":
# 		g = nx.watts_strogatz_graph(n, 40, 0.3)		#each node is connected to k neighbors (40)
# 	elif graph_type == "barabasi":
# 		g = nx.barabasi_albert_graph(n, 20)			#m = number of connections for each new node
# 	else:											#m = ~20-21 generates 20k edges
# 		print("Couldn't recognize your graph type!")
    												
# 	_ = avg_degree(g, n)							#check average degree
# 	_ = avg_neighbor_degree(g)						#returns avg degree of all neighbors


# generate_graph("erdos")
# generate_graph("watts")
# generate_graph("barabasi")
