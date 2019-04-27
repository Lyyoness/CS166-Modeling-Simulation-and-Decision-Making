import math
import numpy as np
import matplotlib.pyplot as plt


# Data (hard coded)
Dx = [1.0, 2.0] # We actually don’t need the x values
Dy = [30.0, 40.0]

# Model , horizontal line , y(x) = m
def y(x, theta):
	return theta[0]

# Chi Squared
def chi2(Dx, Dy, theta):
	s  =  0.0
	for i in range(len(Dx)):
		s += (y(Dx[i], theta) - Dy[i])**2

	return s/len(Dx)

# Likelihood function
def P(Dx, Dy, theta):
	return (-chi2(Dx, Dy, theta))


# Initial guess for model parameters
theta_cur  =  [-3.0]
P_cur  =  P(Dx, Dy, theta_cur)
chain  =  [] # Array to save the MCMC chain


# Do 5000 generations
for _ in range(5000):

	# Randomly draw new_prop theta
	theta_prop  =  [theta + 0.1 * np.random.randn() for theta in theta_cur]
	P_prop  =  P(Dx, Dy, theta_prop)

	# Calculate likelihood ratio
	ratio  =  math.exp(P_prop - P_cur)

	# Decide if to accept the new theta values
	if ratio > np.random.rand():
		theta_cur  =  theta_prop
		P_cur  =  P_prop

	# Save_cur theta value in chain
	chain.append(theta_cur[0])


# Plot the result
plt.plot(chain)
plt.show()


"""
Using a more complicated model, this process
looks almost exactly the same:
"""

# # Read in data
# Dx=[]
# Dy=[]

# for line in open("temp.txt"):
# 	rows = line.split(" ")
# 	Dx.append(float(rows[0]))
# 	Dy.append(float(rows[1]))

# # Model
# def y(x,theta):
# 	return theta[0]+theta[1]* math.sin(2.* math.pi/24.*x+theta[2])

# # Chi Squared
# def chi2(Dx, Dy, theta):
# 	s = 0.
# 	for i in range(len(Dx)):
# 		s += (y(Dx[i],theta)Dy[i])**2
# 	return s/len(Dx)

# # Likelihood function
# def P(Dx, Dy, theta):
# 	return -chi2(Dx,Dy,theta)

# # Initial guess for model parameters
# theta_cur = [0.,0.,0.]
# P_current = P(Dx,Dy,theta_cur)
# chain = []

# for i in range(10000):
# 	theta_prop = [theta+0.1* numpy.random.randn() for theta in theta_cur]
# 	P_prop = P(Dx,Dy,theta_prop)
# 	ratio = math.exp(P_prop - P_cur)

# 	if ratio > numpy.random.rand():
# 		theta_cur = theta_prop
# 		P_cur = P_prop

# 	if i>=5000: # save chain only after burnin
# 		chain.append(theta_cur)


# # Calculate average:
# theta_avg = [0.,0.,0.]
# for theta in chain:
# 	for i in range(3):
# 		theta avg[i] += theta[i]

# for i in range(3):
# 	theta_avg[i] /= len(chain)

# # Calculate model y
# My = []
# for x in Dx:
# 	My.append(y(x,theta avg))

# plt.plot(Dx, Dy, "ro")
# plt.plot(Dx, My, ".")
# plt.show()