#!/usr/bin/python

import numpy as np
import sys
import gaussianenv as ge
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy.random.mtrand as mt

def getMaternSampleWithSampler( rng = None,gamma = 1.0, eta = 1.0, order = 2, alpha = 0.1, phi = 2.0, dtheta = 0.3, dt = 0.001, repetitions = 100, timewindow=100000):
	zeta = 2
	L = 0.8
	N = 1
	a = np.zeros(N*N)
	sigma = 0.001

	if rng==None:
		rng = mt.RandomState()
		rng.seed(12345)

	e = ge.GaussianEnv(zeta,gamma,eta,L,N,-2.0,-2.0,4.0,4.0,sigma,order)
	gam = e.getgamma()
	et = e.geteta()
	abar  = np.sqrt(2.0*np.pi)*alpha*phi/dtheta

	sigmaavg = np.zeros((order,order))
	sigma = np.zeros((order,order))
	sigmaeq = np.zeros((order,order))
	sigmamf = np.zeros((order,order))
	sigmamf[:,:] = 0.01*np.identity(order)
	
	for i in range(timewindow):
		sigmamf[:,:] = sigmamf[:,:] - dt*(np.dot(gam,sigmamf[:,:])+np.dot(sigmamf[:,:],gam.T)-et) - dt*abar*np.dot(np.array([sigmamf[:,0]]).T,np.array([sigmamf[:,0]]))/(alpha**2+sigmamf[0,0])
	sigmaeq[:,:] = sigmamf[:,:]
	
	samples = 0
	for i in range(timewindow):
		if rng.rand()<abar*dt:
			sigma[:,:] -= np.dot(np.array([sigma[:,0]]).T,np.array([sigma[:,0]]))/(alpha**2+sigma[0,0])
		else:
			sigma[:,:] -= dt*(np.dot(gam,sigma[:,:])+np.dot(sigma[:,:],gam.T)-et)
		sigmaavg += sigma[:,:]
		samples +=1
		 
	sigmaavg = sigmaavg/samples
	return [sigmaavg,sigmamf]

