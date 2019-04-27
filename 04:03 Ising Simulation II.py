import matplotlib
matplotlib.use('TkAgg')

import pylab as plt
import random as rd
import scipy as sp
import numpy as np
from matplotlib.pyplot import cm

rd.seed()


class Magnet():
	"""
	Description
	"""
	J = 6.34369e-21  # Interaction constant for iron [Joule]
	kB = 1.38065e-23  # Boltzmann constant [Joule / Kelvin]

	def __init__(self, T, size = 100):
		self.size = size
		self.temp = float(T)

		self.config = sp.zeros([size, size])
		self.time = 0


	def initialize(self):
		"""
		Randomly initializes the magnet's state and
		resets counting/plotting variables.
		"""
		self.time = 0
		self.config = sp.random.choice([-1, +1], size=(self.size, self.size))
		self.magnetized_frac = []


	def change_temperature(self, T):
		self.temp = float(T)


	def step(self):
		"""
		Updates the magnet and records the current magnetization.
		"""
		i, j = sp.random.randint(self.size, size=2)
		cell = self.config[i,j]

		# Change in energy from current state to next state
		delta_E = 2 * self.J * cell * (
			self.config[(i + 1) % self.size, j] +
			self.config[(i - 1) % self.size, j] +
			self.config[i, (j + 1) % self.size] +
			self.config[i, (j - 1) % self.size])

		# Log probability of changing state
		log_p = - delta_E / (self.temp * self.kB)

		if sp.log(sp.random.uniform(0, 1)) < log_p:
			self.config[i,j] = cell * -1

		if self.time % 100 == 0:		#records state every 20 steps
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


print ("Test run! ")
for temp in [1, 1043, 2000]:
	test_magnet = Magnet(T = temp, size = 5)
	test_magnet.initialize()
	test_magnet.run(300000)
print (test_magnet.config)
	# test_magnet.draw()

"""
Histogram for simulation.
"""

# final_magnetization = []
# magnet = Magnet(T = 1, size = 20)

# for _ in range(60):
# 	magnet.initialize()
# 	magnet.run(50000)
# 	final_magnetization.append(magnet.magnetized_frac[-1])
# 	# magnet.draw()

# plt.xlim(-1, 1)
# plt.hist(final_magnetization)
# plt.show()

"""
Histogram for simulation using annealing.
"""

plt.clf()
final_magnetization = []

for _ in range(60):
	magnet = Magnet(T = 2000, size = 20)
	magnet.initialize()
	T = 2000

	while T > 2:
		magnet.change_temperature(T)
		magnet.run(50)
		T -= 1
		
	final_magnetization.append(magnet.magnetized_frac[-1])

plt.title("Simulation with Annealing")
plt.xlim(-1, 1)
plt.hist(final_magnetization)
plt.show()

