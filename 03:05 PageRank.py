import networkx as nx
import matplotlib.pyplot as plt
import numpy as np 
import random as rd


#----------------------------
# SIMULATING THE SURFER
#----------------------------
def generate_graph():
	'''
	Generates our graph and initiates the visits attribute to 0.
	'''
	g = nx.erdos_renyi_graph(30, 0.05, directed=True, seed=123)
	for node in g.nodes:
		g.nodes[node]['visits'] = 0

	return g

def calculate_page_rank(g, n):
	'''
	Updates the pagerank attribute for each node and also 
	generates a pagerank dict that can be passed into the
	calculate_difference() function.
	'''
	page_rank = []
	for i in g.nodes():
		score = g.nodes[i]['visits'] / n

		g.nodes[i]['pagerank'] = score
		page_rank.append(score)

	return g, page_rank

def calculate_difference(g, ranking):
	'''
	Get the difference between our current ranking and
	the real one (networkx-generated).
	'''
	page_rank_dict = nx.pagerank(g)
	page_rank = [page_rank_dict[k] for k in range(len(page_rank_dict))]

	error = 0

	for real, approx in zip(page_rank, ranking):
		error += abs(real - approx)

	return error


def surfer(g = generate_graph(), alpha = 0.85, N = 1000):
	'''
	Does an N-step random walk over the graph and then returns the
	error between the predicted page rank and the actual page rank
	every 10 iterations.
	'''
	x = []
	error_y = []

	surfer_loc = rd.choice(list(g.nodes))		#pick random starting node
	g.nodes[surfer_loc]['visits'] += 1

	for n in range(1, N):
		neighbors = [n for n in g.neighbors(surfer_loc)]
											#if no neighbor or > alpha
											#jump to random other page
		if np.random.uniform() > alpha or neighbors == []:
			surfer_loc = rd.choice(list(g.nodes))		
			g.nodes[surfer_loc]['visits'] += 1
		else:								#move to neighbor node normally
			surfer_loc = rd.choice(neighbors)
			g.nodes[surfer_loc]['visits'] += 1

		if n % 10 == 0:
			g, cur_rank = calculate_page_rank(g, n)
			error = calculate_difference(g, cur_rank)

			x.append(n)
			error_y.append(error)

	return g, x, error_y
	
#----------------------------
# PLOT ERROR REDUCTION
#----------------------------

final_graph, x, y = surfer()
# plt.plot(x, y)
# plt.xlabel("Number of steps")
# plt.ylabel("Error")
# plt.show()


#----------------------------
# PLOTTING PAGE RANK BY COLOR
#----------------------------
_, rankings = calculate_page_rank(final_graph, 1000)
page_rankings = nx.pagerank(final_graph)
page_rankings = [v for k, v in page_rankings.items()]

plt.figure()
plt.subplot(1,2,1)
plt.title("Page Rank")
nx.draw(final_graph, cmap=plt.get_cmap('Reds'), pos=nx.kamada_kawai_layout(final_graph),
		node_color=page_rankings)

plt.subplot(1,2,2)
plt.title("Random Walk")
nx.draw(final_graph, cmap=plt.get_cmap('Reds'), pos=nx.kamada_kawai_layout(final_graph),
		node_color=rankings)

plt.show()

