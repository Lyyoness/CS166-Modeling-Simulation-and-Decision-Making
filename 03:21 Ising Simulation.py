import matplotlib
matplotlib.use('TkAgg')

import pylab as plt
import random as rd
import scipy as sp
import numpy as np
from matplotlib.pyplot import cm

rd.seed()

n = 100

class Magnet():
	"""
	Description
	"""

	def __init__(self, T, size = 100):
		self.size = size
		self.temp = T

		self.config = sp.zeros([size, size])
		self.time = 0
		self.magnetized_frac = []


	def initialize(self):
		"""
		Randomly initializes the magnet's state and
		resets counting/plotting variables.
		"""
		self.time = 0
		self.config = sp.zeros([self.size, self.size])
		self.magnetized_frac = []

		for x in range(self.size):
			for y in range(self.size):

				if rd.random() < 0.5:
					state = -1
				else:
					state = 1

				self.config[y, x] = state

	def step(self):
		"""
		Updates the magnet and records the current magnetization.
		"""

		i, j = np.random.choice(range(self.size), 2)
		cell_val = self.config[i,j]
		neighbors = [self.config[(i-1)%self.size, j],
					 self.config[i, (j-1)%self.size],
					 self.config[(i+1)%self.size, j],
					 self.config[i, (j+1)%self.size]]

		energy = (cell_val * -1) * sum([n * cell_val for n in neighbors])

		if rd.uniform(0, 1) < min(1, np.exp(2 * energy / self.temp)):
			cell_val = cell_val * -1

		self.config[i,j] = cell_val

		if self.time % 10 == 0:		#records state every 20 steps
			self.magnetized_frac.append(np.mean(self.config))

		self.time += 1	


	def run(self, r):
		for _ in range(r):
			self.step()

	def draw(self):
		"""
		Visualizes the current state.
		"""
		plt.cla()
		plt.subplot(1,2,1)
		plt.pcolor(self.config, vmin = -1, vmax = 1, cmap = cm.coolwarm)
		plt.title('time = ' + str(self.time) + "steps    Temperature: " + str(self.temp))
		plt.subplot(1,2,2)
		plt.ylim(-1,1)
		plt.plot(self.magnetized_frac, 'b-')
		plt.show()


# print ("Test run! ")
# for temp in [1, 2, 3, 4, 5]:
# 	test_magnet = Magnet(T = temp, size = 10)
# 	test_magnet.initialize()
# 	test_magnet.run(100000)
# 	test_magnet.draw()

"""
For each of the T values above, plot a histogram over
the average magnetization of the final state.
You will need to run the simulation about 100 times
for each T, to get enough data for your histogram.
"""
print("Starting now")
for temp in [1, 2, 3, 4, 5]:
	final_magnetization = []
	print ("Current temp: " + str(temp))

	for run in range(30):
		magnet = Magnet(T = temp, size = 20)
		magnet.initialize()
		magnet.run(30000)
		final_magnetization.append(magnet.magnetized_frac[-1])

	plt.subplot(1,5,temp)
	plt.title("T = " + str(temp))
	plt.xlim(-1, 1)
	plt.hist(final_magnetization)

plt.suptitle("Final magnetizations with different values of T")
plt.show()

