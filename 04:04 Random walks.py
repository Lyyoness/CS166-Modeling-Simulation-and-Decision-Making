import random as rd
import numpy as np
import pylab as plt

"""
------------------------------------------------------------------
EXERCISE 1: Write a random walk.
------------------------------------------------------------------
"""

def random_walk_1d(steps, bias = 0):
	X = 0
	for _ in range(steps):
		dx = rd.choice([-1+bias, 1+bias])
		X += dx
	return X


# #without bias
# dist_rand_walk = []
# for _ in range(500):
# 	dist_rand_walk.append(random_walk_1d(100))

# plt.hist(dist_rand_walk)
# plt.show()

# #with bias
# dist_rand_walk = []
# for _ in range(500):
# 	dist_rand_walk.append(random_walk_1d(100, 0.1))

# plt.hist(dist_rand_walk)
# plt.show()

"""
------------------------------------------------------------------
EXERCISE 2: Write an unbiased random walk with obstacles.
a) reflection barrier at x = -4 (bounce off)
b) partial block at x = 6 (0.25 chance of passing through)
------------------------------------------------------------------
"""
def rw_obstacles(steps, barrier = -4, block = 6):
	"""
	Note: barriers would overwrite blocks, since they
	can never be passed.
	"""
	if barrier == block:
		print("Don't do that!")
		return

	X = 0
	for _ in range(steps):
		dx = rd.choice([-1, 1])

		if X == block:
			if X > 0:
				if rd.uniform(0,1) < 0.25:
					X += 1
				else:
					X -= 1
			else:
				if rd.uniform(0,1) < 0.25:
					X -= 1
				else:
					X += 1
		#barrier (either on right or left side)
		elif X == barrier:
			if X > 0:
				X -= 1
			else:
				X += 1
		else:
			X += dx

	return X

# #random walk with obstacles at default
# dist_rand_walk = []
# for _ in range(10000):
# 	dist_rand_walk.append(rw_obstacles(100))

# plt.hist(dist_rand_walk, bins=15)
# plt.show()

# #random walk with obstacles at 10 and 2
# dist_rand_walk = []
# for _ in range(10000):
# 	dist_rand_walk.append(rw_obstacles(100, 10, 2))

# plt.hist(dist_rand_walk, bins=20)
# plt.show()


"""
------------------------------------------------------------------
EXERCISE 3: Simulate a random walk in 2 continuous dimensions.
1) Start at origin.
2) Choose a direction from 0 to 360 degrees.
3) Choose step size according to a Gaussian (0, sigma)
4) Advance in that direction and continue.

Take Sigma^2 to be 0.5, 1, 2 and evaluate the effect.
Take n to be 20, 400, 1600 and evaluate the effect.
Plot one typical path for n=1600.
Show density plots for several walkers.
------------------------------------------------------------------
"""
def contin_walk(steps, sigma = 1, history=False):
	#1) start at origin
	X, Y = 0, 0

	if history:
		x_hist, y_hist = [], []

	for _ in range(steps):

		#2-3) choose direction and step size
		(dX, dY) = np.random.normal(0, np.sqrt(sigma), 2)

		#4) advance in direction
		X += dX
		Y += dY

		if history:
			x_hist.append(X)
			y_hist.append(Y)

	if history:
		return(x_hist, y_hist)
	else:
		return(X, Y)


# #plotting a single random walk
# x_loc, y_loc = contin_walk(1600, history=True)
# plt.plot(x_loc, y_loc, linewidth = 0.4)
# plt.show()

# #plotting different types of walkers
# steps = [20, 400, 1600]
# sigma = [0.5, 1, 2]

# sigma_marker = ['blue', 'green', 'red']

# for m, step in enumerate(steps):
# 	for n, sig in enumerate(sigma):
# 		x_loc, y_loc = [], []
# 		for _ in range(150):
# 			(x_new, y_new) = contin_walk(step, sig)
# 			x_loc.append(x_new)
# 			y_loc.append(y_new)
# 		plt.scatter(x_loc, y_loc, color = sigma_marker[n], alpha = 0.3,
# 					s = 4, label=str(sig))
# 	plt.legend(["Sigma 0.5", "Sigma 1", "Sigma 2"])
# 	plt.title("Steps: %d" %(step))
# 	plt.xlim(-100, 100)
# 	plt.ylim(-100, 100)
# 	plt.show()


"""
------------------------------------------------------------------
EXERCISE 4: Diffusion in a plane with a hole.

Starting at the origin, carry out a random walk over a 40x40 plane.
Assume there is a square hole whose boundaries are (13,7), (14,7),
(14,8) and (13,8). Walks that reach the hole (or it's boundary)
are absorbed.
Show the distribution of final positions for walks of various steps
and the fraction that enters the hole.
------------------------------------------------------------------
"""
def rw_contin_hole(n_walkers, steps, hole_x = (0,20), hole_y=(0,20)):
	"""
	This simply modifies the original model with a hole.
	Now returns only the final state, since we don't need
	the history for a histogram (funny, isn't it?)
	"""
	#1) start at origin
	X_final, Y_final = [], []
	walkers_in_hole = 0
	hole_len = abs(hole_x[0] - hole_x[1])
	hole_wid = abs(hole_y[0] - hole_y[1])

	for walker in range(0, n_walkers):
		X, Y = 0, 0

		for _ in range(0, steps):

			# choose direction and step size
			(dX, dY) = np.random.normal(0, 1, 2)

			# advance in direction
			X += dX
			Y += dY

			#make sure our walkers don't run off
			if X > 20:
				X = 20
			elif X < -20:
				X = -20
			if Y > 20:
				Y = 20
			elif Y < -20:
				Y = -20

			#check if they disappear in the hole!
			if ((X > hole_x[0]) and (X <hole_x[1]) and
				(Y > hole_y[0]) and (Y < hole_y[1])):
				walkers_in_hole += 1
				X, Y = np.mean(hole_x)+rd.uniform(0,hole_len//3), np.mean(hole_y)+rd.uniform(0,hole_wid//3)
				break

		X_final.append(X)
		Y_final.append(Y)
	lost_walkers = walkers_in_hole/float(n_walkers)

	return(X_final, Y_final, lost_walkers)

n = 100
s = 100000

fig, ax = plt.subplots(1)

X, Y, lost_walkers = rw_contin_hole(n, s, (13,14), (7,8))
plt.title(f'After {s} steps, with {n} walkers, we lost {100*lost_walkers:.1f} percent.')
plt.scatter(X,Y, s = 5)
plt.xlim(-20, 20)
plt.ylim(-20, 20)
plt.show()
