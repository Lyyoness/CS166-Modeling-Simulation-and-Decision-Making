import numpy as np
import random as rd
import matplotlib.pyplot as plt


#-------------------------------
# BIASED COIN - RANDOM WALK
#-------------------------------
# Use a biased coin (P(H)=0.6, P(T)=0.4) to simulate a walk of 30
# steps. If the coin comes up heads, take a step to the right, tails
# one to the left.
# a) plot a sample path
# b) histogram for 200 walks
# c) sample mean and variance (simulated & exact values)
#---------------------------------------------------------------------

def biased_coin_flip(p_heads):
	if rd.uniform(0,1) < p_heads:
		return -1
	else:
		return 1


def plot_sample_path(p_heads):
	steps = range(0,31)
	sample_locations = []
	cur_loc = 0

	for step in steps:
		direction = biased_coin_flip(p_heads)
		cur_loc += direction
		sample_locations.append(cur_loc)

	plt.plot(steps, sample_locations)
	plt.xlabel("Number of Steps Taken")
	plt.ylabel("Location (negative numbers are to the right)")
	plt.ylim(-20,15)
	plt.show()


def simulate_rand_walks(runs, p_heads, bins = 10, plot = False):
	steps = range(0,31)
	final_locations = []

	for r in range(runs):
		cur_loc = 0
		for step in steps:
			cur_loc += biased_coin_flip(p_heads)
		final_locations.append(cur_loc)

	if plot:
		plt.hist(final_locations, bins = bins)
		plt.suptitle("Random walks of %d samples" %runs)
		plt.show()

	mean = np.mean(final_locations)
	variance = np.var(final_locations)
	print ("The sample mean is %f. The variance is %f."
			%(mean, variance))


# plot_sample_path(0.6)
simulate_rand_walks(200, 0.4, plot = True)	
simulate_rand_walks(100000, 0.4, bins = 15, plot = True)		

		