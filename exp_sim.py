#!/usr/bin/env python
# Simulate the differential equations in Hagerstrom (2015)

import numpy as np
import random
import time


'''
Outline

Generate photon times
Loop
	Get a photon
	Go through modulator
	Go through filter
'''

#The (basically unchangeable conditions)
dt = 0.000005 #Time interval (around the size of mu for lambda0 * Td = 3200)
samptime = 0.0001 #How often to take a sample
sampspersec = 1 / samptime #Inverse
Td = 0.001734 #Time delay
T1 = 0.0012 #Time constant for variable 1
T2 = 0.00006 #Time constant for variable 2
phi = np.pi / 4 #Filter phase displacement

#Simulation parameters
betatimesTd = 8.87 #this is the actual measurement that Aaron used, different than what he claims
beta = betatimesTd / Td #this is the real beta value, in the thousands.
deterministic = False
T = 5 #seconds to simulate

if not deterministic:
	filelist = [5000,10000]
else:
	filelist = ["det"]

for filename in filelist:
	t = 0
	transtime = 0.1
	x1 = 10 * random.random()
	x2 = 10 * random.random()
	N = int(Td / dt)
	x1hist = [.7834] * N
	x2hist = [.7834] * N
	xdiff = 0
	pval = np.pi
	ctr = 0

	foutv = open(str(filename) + "v.out","w")
	foutx = open(str(filename) + "xs.out","w")

	foutv.write(str(T) + "\n")

	timestart = time.clock()

	if not deterministic:
		lambda0timesTd = int(filename) #Metric given in Aaron's paper
		lambda0 = lambda0timesTd / Td
		mu = 1 / lambda0 #Poisson interarrival time average
		n = T / mu
		taus = np.random.exponential(mu, n)
		T = np.sum(taus)
		index = 0 #photon index
		lastt = 0

	while t < T:
		I = (np.sin(x1hist[ctr % N] - x2hist[ctr % N] + phi)) ** 2

		#Evolution of x1, x2
		if deterministic:
			x1 += (-1 / T1 * x1 + beta * I) * dt
			x2 += (-1 / T2 * x2 + beta * I) * dt
		else:
			while t > lastt + taus[index]:
				if random.random() <= I:
					x1 += beta / lambda0
					x2 += beta / lambda0
				index += 1
				lastt = lastt + taus[index]

			x1 *= np.exp(-dt/T1)
			x2 *= np.exp(-dt/T2)

		#Record data
		if t > transtime and int(t / dt) % int(samptime / dt) == 0:
			foutv.write("{:6f}\n".format(x1 - x2))
			if (x1 - x2 - pval) * xdiff < 0:
				foutx.write("{:6f}\n".format(t - transtime))
			xdiff = x1 - x2 - pval

		#Progress
		if int(t / dt) % int(T / 50. / dt) == 0:
			percent = int(t / dt) / int(T / 100. / dt)
			print ('=' * (percent / 2)) + percent

		x1hist[ctr % N] = x1
		x2hist[ctr % N] = x2
		t += dt
		ctr += 1

	foutv.close()
	foutx.close()

	print str(filename) + ": " + str(time.clock() - timestart)

print 'Program done...'