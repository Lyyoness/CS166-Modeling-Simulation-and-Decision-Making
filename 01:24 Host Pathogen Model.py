# Simple CA simulator in Python
#
# *** Hosts & Pathogens ***
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

RD.seed()

width = 50
height = 50
sim_size = width * height

def param_init(P_init = 0.01):
    global initProb
    initProb = float(P_init)
    return initProb

def param_infection(R_inf = 0.85):
    global infectionRate
    infectionRate = float(R_inf)
    return infectionRate

def param_growth(R_growth = 0.15):
    global regrowthRate
    regrowthRate = float(R_growth)
    return regrowthRate

def init():
    global time, config, nextConfig, healthy_density, sick_density
    healthy_density, sick_density = [], []
    time = 0
    
    config = SP.zeros([height, width])
    for x in range(width):
        for y in range(height):
            if RD.random() < initProb:
                state = 2
            else:
                state = 1
            config[y, x] = state

    nextConfig = SP.zeros([height, width])

def draw():
    PL.cla()
    PL.subplot(1,2,1)
    PL.pcolor(config, vmin = 0, vmax = 2, cmap = PL.cm.jet)
    PL.axis('image')
    PL.title('t = ' + str(time))
    PL.subplot(1,2,2)
    PL.plot(healthy_density, 'g-', sick_density, 'r-')


def step():
    '''
    0 represents dead (blue)
    1 represents alive (green)
    2 represents infected (red)
    '''
    global time, config, nextConfig

    time += 1

    for x in range(width):
        for y in range(height):
            state = config[y, x]
            if state == 0:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if config[(y+dy)%height, (x+dx)%width] == 1:
                            if RD.random() < regrowthRate:
                                state = 1
            elif state == 1:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if config[(y+dy)%height, (x+dx)%width] == 2:
                            if RD.random() < infectionRate:
                                state = 2
            else:
                state = 0

            nextConfig[y, x] = state
    healthy_individuals = NP.count_nonzero(config.ravel() == 1)
    sick_individuals = NP.count_nonzero(config.ravel() == 2)
    healthy_density.append(healthy_individuals/sim_size)
    sick_density.append(sick_individuals/sim_size)

    config, nextConfig = nextConfig, config

import pycxsimulator
pycxsimulator.GUI(parameterSetters=[param_init, param_infection, param_growth]).start(func=[init,draw,step])

def f(x):
    return 28*x**9 - 224*x**8 + 700*x**7 - 1120*x**6 + 980*x**5 - 448*x**4 + 84*x**3

x = NP.linspace(0,1, 100)
y = [f(x) for x in x]
PL.plot(x, y, 'b-', x, x, 'r-')
PL.show()
