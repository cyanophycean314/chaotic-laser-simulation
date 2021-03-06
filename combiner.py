#Combine some files and cleans them up!

import sys

filelist = [str(_) + '' for _ in ['det']]
subscripts = ['','super']

for filename in filelist:
	fout = open(str(filename) + 'comvt.out','w')
	totalT = 0
	for lett in subscripts:
		fin = open(str(filename) + lett + 'vt.out','r')
		totalT += float(fin.readline())
	fout.write("{:6f}\n".format(totalT))
	for lett in subscripts:
		fin = open(str(filename) + lett + 'vt.out','r')
		firstline = True
		for line in fin:
			if not firstline and len(line.split()) == 2 and len(line) == 18:
				fout.write(line)
			firstline = False