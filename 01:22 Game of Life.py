import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import pylab as pl

n = 100 # size of space: n x n

def p_param(val = 0.1):
    global p

    p = float(val)
    return p

def initialize():
    global config, nextconfig, density
    density = []
    config = pl.zeros([n, n])
    for x in range(n):
        for y in range(n):
            config[x, y] = 1 if pl.random() < p else 0
            nextconfig = pl.zeros([n, n])
            
def observe():
    global config, nextconfig
    pl.cla()
    pl.subplot(1,2,1)
    pl.imshow(config, vmin = 0, vmax = 1, cmap = pl.cm.binary)
    pl.subplot(1,2,2)
    pl.plot(density)

#Game of Life
def update():
    global config, nextconfig, density
    for x in range(n):
        for y in range(n):
            count = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    count += config[(x + dx) % n, (y + dy) % n]
            if config[x, y] == 0:
                nextconfig[x, y] = 1 if count == 3 else 0
            if config[x, y] == 1:
                nextconfig[x, y] = 1 if (count == 3) or (count == 2) else 0
    density.append(np.mean(config.ravel()))
    config, nextconfig = nextconfig, config

# #Panic simulation
# def update():
#     global config, nextconfig, density
#     for x in range(n):
#         for y in range(n):
#             count = 0
#             for dx in [-1, 0, 1]:
#                 for dy in [-1, 0, 1]:
#                     count += config[(x + dx) % n, (y + dy) % n]
#                     nextconfig[x, y] = 1 if count >= 4 else 0
#     density.append(np.mean(config.ravel()))
#     config, nextconfig = nextconfig, config

    
import pycxsimulator
pycxsimulator.GUI(parameterSetters=[p_param]).start(func=[initialize, observe, update])