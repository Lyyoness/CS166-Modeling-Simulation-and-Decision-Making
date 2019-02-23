# Simple CA simulator in Python
#
# *** Forest fire ***
#
# Copyright 2008-2012 Hiroki Sayama
# sayama@binghamton.edu

# Modified to run with Python 3

import matplotlib
matplotlib.use('TkAgg')

import pylab as PL
import random as RD
import scipy as SP
import numpy as NP
from matplotlib.pyplot import cm

RD.seed()

width = 100
height = 100
initProb_default = 0.4
empty, tree, fire, char = range(4)

def param_init(tree_prob = initProb_default):
    global initProb
    initProb = float(tree_prob)
    return initProb

def init():
    global time, config, nextConfig, burnt_area

    time = 0
    burnt_area = []

    config = SP.zeros([height, width])
    for x in range(width):
        for y in range(height):
            if RD.random() < initProb:
                state = tree
            else:
                state = empty
            config[y, x] = state
    config[height//2, width//2] = fire

    nextConfig = SP.zeros([height, width])

def draw():
    PL.cla()
    PL.subplot(1,2,1)
    PL.pcolor(config, vmin = 0, vmax = 3, cmap = PL.cm.binary)
    PL.axis('image')
    PL.title('t = ' + str(time))
    PL.subplot(1,2,2)
    PL.ylim(0,1)
    PL.plot(burnt_area, 'b-')

def step():
    global time, config, nextConfig

    time += 1

    for x in range(width):
        for y in range(height):
            state = config[y, x]
            if state == fire:
                state = char
            elif state == tree:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if config[(y+dy)%height, (x+dx)%width] == fire:
                            state = fire
            nextConfig[y, x] = state
    burnt = NP.count_nonzero(config.ravel() == 3)
    alive = NP.count_nonzero(config.ravel() == 1)
    burnt_area.append( burnt/(burnt + alive))

    config, nextConfig = nextConfig, config

# import pycxsimulator
# pycxsimulator.GUI(parameterSetters=[param_init]).start(func=[init,draw,step])

def f(x):
	return x**4 + 4*x**3*(1-x) + 4*x**2*(1-x)**2

# x = NP.linspace(0,1, 100)
# y = [f(x) for x in x]
# PL.plot(x, y, 'b-', x, x, 'r-')
# PL.show()

runs = 10
time_steps = 200
probabilites = [0.3, 0.38, 0.4, 0.42, 0.5]
total_burnt_area = NP.zeros((runs, len(probabilites), time_steps))

for r in range(runs):
	print("RUN:", r)
	j = 0
	for prob in probabilites:
		global initProb
		initProb = prob
		init()
		for i in range(time_steps):
			step()

		print (NP.shape(burnt_area))
		print (NP.shape(total_burnt_area))
		total_burnt_area[r, j, :] = burnt_area
		j+=1

mean_burnt_area = NP.mean(total_burnt_area, axis=0)
print (NP.shape(mean_burnt_area))

x = range(0,time_steps)
color = cm.rainbow(NP.linspace(0,1, len(probabilites)))

for y, col in zip(range(0, len(probabilites)), color):
	PL.plot(x, mean_burnt_area[y,:], c = col)

PL.xlabel("Time")
PL.ylabel("Fraction of forest burnt")
PL.legend(['Initial density = 0.3','Initial density = 0.38',
			'Initial density = 0.4','Initial density = 0.42',
			'Initial density = 0.5'])
PL.show()
