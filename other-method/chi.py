#!/usr/bin/python

size = 5
def binning( row ):
	mini = min(row)
	maxi = max(row)
	scale = maxi-mini
	return [ min(size-1,int((v-mini)/scale*size)) for v in row ]

from math import log

def getCHI(A, B, O):
	N = len(A) * 1.0
	tb = [[0 for j in xrange(size**2)] for i in xrange(2)]	
	rowsum = [0 for i in xrange(2)]	
	colsum = [0 for i in xrange(size**2)]
	for o, a, b in zip(O,A,B):
		tb[o][a*size+b] += 1
		rowsum[o] += 1
		colsum[a*size+b] += 1

	ret = 0.0

	for i in xrange(2):
		for j in xrange(size**2):
			expected = rowsum[i] * colsum[j] / N
			if expected == 0: continue
			ret += (tb[i][j] - expected)**2/expected

	return ret


import sys

with open(sys.argv[1],'r') as inp:
	if len(sys.argv) > 4 and sys.argv[4] == "discrete":
		data = [[int(r)+2 for r in row.strip().split()] for row in inp]
	else:
		data = [binning(map(float,row.strip().split())) for row in inp]

with open(sys.argv[2],'r') as inp:
	outcome = [int(x.strip()) for x in inp]

chi = [ getCHI(data[i], data[j], outcome) for i in xrange(len(data)) for j in xrange(i+1,len(data)) ]


import numpy

with open(sys.argv[3],'w') as oup:
	F, P = numpy.histogram(chi, 100)
	for f, p in zip(F,P):
		print >> oup, str(p) + '\t' + str(f)
