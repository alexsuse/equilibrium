#!/usr/bin/python
import numpy as np
import coding_matern as coding
import cPickle
import multiprocessing as mp
from multiprocessing import Pool
import sys
import os

order = 2

nsample = 10


def runm(params):
	[a,p] = params 
	print a,p
	sigmas = np.zeros((order,order))
	sigmasmf = np.zeros((order,order))
	[sigmas,sigmasmf] = coding.getMaternSampleWithSampler(phi = p, alpha = a)
	return [(a,p),sigmas,sigmasmf]


if __name__=='__main__':
	inp = []
	if len(sys.argv)>1:
		prefix = sys.argv[1]
	else:
		prefix = "phis_alphas_pool.pickle"
	phis = np.arange(0.0,3.0,0.05)
	alphas = np.arange(0.001,3.0,0.05)

	ncpus = mp.cpu_count()

	print "Running on ",ncpus," cores."

	out = dict()
	for p in phis:
		for a in alphas:
			inp.append([a,p])
	
	pool = mp.Pool(processes=ncpus)
	outp = pool.map(runm,inp)
	
	print "are these the droids?"
	for i in outp:
		sigmas = np.zeros((order,order))
		sigmasmf = np.zeros((order,order))
		sigmaseq = np.zeros((order,order))
		[(a,p),sigmas[:,:],sigmasmf[:,:]] = i
		out[(a,p)]=[sigmas,sigmasmf]
	
	fileout = open(prefix,"w+")
	cPickle.dump(out,fileout)
	fileout.close()

	os.system("""echo "simulation is ready, dude!"|mail -s "Simulation" alexsusemihl@gmail.com""")

	print "All is good with the force!"
