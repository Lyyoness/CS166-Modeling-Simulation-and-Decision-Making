import numpy as np
import random as rd
import matplotlib.pyplot as plt


#-------------------------------
# GAMBLER'S RUIN
#-------------------------------
# Simulate the gambler's ruin problem with different upper bounds on
# the iteration count.
# a) how does this bias average game duration?
# b) How does this bias sample variance?
#---------------------------------------------------------------------

def gamble():
	if rd.uniform(0,1) < 0.5:
		return 1
	else:
		return -1

def simulate(runs, time_lim, plot=False):
	len_game = []

	for r in range(runs):
		gamblers_money = 100
		house_money = 2000

		for t in range(time_lim):
			if (gamblers_money > 0) & (house_money > 0):
				game_return = gamble()
				gamblers_money += game_return
				house_money -= game_return
				total_time = t
			else:
				total_time = t
				break

		len_game.append(total_time)

	var = np.var(len_game)
	mean = np.mean(len_game)

	if plot:
		plt.hist(len_game)
		plt.title("Gambles until bankrupcy with %d samples" %runs)
		plt.xlabel("Game durations at a time limit of %d rounds. \n Mean: %.3g;  Var: %.3g"
					%(time_lim, mean, var))
		plt.show()


simulate(100, 1000, plot=True)


