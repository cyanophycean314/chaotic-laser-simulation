import numpy as np
import matplotlib.pyplot as plt

#Compare divs across int_noise (internal noise) and det_noise (deterministic external noise)

finint = open('divs_intnoise.out','r')
findet = open('divs_NT.out','r')

dataint = [[],[],[]]
for line in finint:
	a,b,c = line.split()
	dataint[0].append(int(1/(float(a) ** 2)))
	dataint[1].append(float(b))
	dataint[2].append(float(c))

datadet = [[],[],[]]
for line in findet:
	a,b,c = line.split()
	datadet[0].append(int(1/(float(a) ** 2)))
	datadet[1].append(float(b))
	datadet[2].append(float(c))

plt.figure(1, figsize = (15,10))
plt.subplot(211)
plt.title("Kullback-Leibler distance")
plt.semilogx(dataint[0], dataint[1], 'r',marker='.', label = 'internal noise')
plt.semilogx(datadet[0], datadet[1], 'g',marker='.', label = 'external noise')
plt.subplot(212)
plt.title("Kolmogorov-Smirnov distance")
plt.semilogx(dataint[0], dataint[2], 'r',marker='.', label = 'internal noise')
plt.semilogx(datadet[0], datadet[2], 'g',marker='.', label = 'external noise')
#plt.show()
plt.savefig("divs_compintdet.png")