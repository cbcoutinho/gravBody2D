import numpy as np
from numpy.linalg import norm
from scipy.integrate import odeint

def func(y,t,m):
    G = 0.5
    
# Put y into array of [x,y,v_x,v_y] for every mass
    y = y.reshape(-1,4)

# Get number of masses
    n = y.shape[0]
    
# Create empty position and velocity vectors
    r, v = np.empty([n,2]), np.empty([n,2])
    for ii in np.arange(n):
# Get position and velocity from y
        r[ii], v[ii] = y[ii,0:2], y[ii,2:]

# Derivative of position is velocity, no need to calculate
    dr = v

# Initialize acceleration vector
    dv = np.zeros([n,2])
    
# Calculate acceleration vector
    for ii in np.arange(n):
        for jj in np.arange(n):
            if ii != jj:
                dv[ii] = dv[ii] + G*m[jj]*(r[jj]-r[ii])/(norm(r[jj]-r[ii])**3.0)

# Reshape velocity and acceleration arrays into a vector
    dydt = np.concatenate([dr,dv],axis=1).reshape([1,-1])[0]
    return dydt

def getParticles(numPar,NSteps):
    
    particles0 = np.zeros(numPar, dtype=[('position', float, 2),
                                        ('velocity', float, 2),
                                        ('mass', float, 1)])

#    particles0['position'] = np.random.uniform(-2,2,(numPar, 2))
    for ii in np.arange(numPar):
        x = 0.75
        if ii < int(numPar/2):
            x = 1.5
            
        particles0['position'][ii] = x*np.array([np.cos(ii/numPar*4*np.pi),
                                       np.sin(ii/numPar*4*np.pi)])

    particles0['velocity'] = np.random.uniform(-1,1,(numPar, 2))*1.2
    #particles0['velocity'] = np.zeros((numPar, 2))
    particles0['mass'] = np.ones(numPar)*np.random.uniform(5,10,numPar)
    #particles0['mass'] = np.ones(numPar)*0.01

    rStart = np.concatenate([particles0['position'],
                            particles0['velocity']],
                            axis=1).reshape([1,-1])[0]

    tStart = 0.0
    tEnd = 5.0

    t = np.linspace(tStart, tEnd, NSteps)
    sol = odeint(func, rStart, t,
                full_output=1,
                args=(particles0['mass'],))

    particles = np.empty([numPar*2,NSteps])
    for ii in np.arange(numPar):
        particles[ii*2:ii*2+2] = sol[0].T[ii*4:ii*4+2]
        
    return particles
