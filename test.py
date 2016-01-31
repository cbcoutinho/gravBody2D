import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import numpy as np
from funMod import func, getParticles

numPar = 12
NSteps = 1000

particles = getParticles(numPar, NSteps)

fig = plt.figure(figsize=(7,7))
ax = plt.axes(xlim=(-2,2),ylim=(-2,2))

# choose a different color for each trajectory
colors = plt.cm.jet(np.linspace(0, 1, numPar))

# set up lines and points
lines = sum([ax.plot([], [], '-', c=c, alpha=0.5)
             for c in colors], [])
pts = sum([ax.plot([], [], 'o', c=c)
           for c in colors], [])

def init():
    for line, pt in zip(lines, pts):
        line.set_data([], [])
        pt.set_data([], [])
        
    return lines + pts

def animate(i):
    for line, pt, j in zip(lines, pts, np.arange(numPar)):
        x, y = particles[j*2][:i], particles[j*2+1][:i]
        line.set_data(x, y)
        pt.set_data(x[-1:],y[-1:])
        
    return lines + pts

anim = FuncAnimation(fig, animate, init_func=init,
              frames=NSteps, interval=1)
plt.show()
