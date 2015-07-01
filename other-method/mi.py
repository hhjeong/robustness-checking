#!/usr/bin/python

size = 5
def binning( row ):
	mini = min(row)
	maxi = max(row)
	scale = maxi-mini
	return [ min(size-1,int((v-mini)/scale*size)) for v in row ]

from math import log

def entropy( X, N ):
	return -sum([(x/N) * log(x/N,2) for x in X if x > 0])

def getMI( A, B ):
	N = len(A) * 1.0
	tb = [0 for i in xrange(size**2)]
	sa = [0 for i in xrange(size)]
	sb = [0 for i in xrange(size)]

	for a, b in zip(A,B):
		tb[a*size+b] += 1
		sa[a] += 1
		sb[b] += 1

	return entropy(sa,N) + entropy(sb,N) - entropy(tb,N)

import sys, numpy

with open(sys.argv[1],'r') as inp:
	if len(sys.argv) > 3 and sys.argv[3] == "discrete":
		data = [[int(r)+2 for r in row.strip().split()] for row in inp]
	else:
		data = [binning(map(float,row.strip().split())) for row in inp]

mi = [getMI(data[i],data[j]) for i in xrange(len(data)) for j in xrange(i+1,len(data))]

with open(sys.argv[2],'w') as oup:
	F, P = numpy.histogram(mi, 100)
	for f, p in zip(F,P):
		print >> oup, str(p) + '\t' + str(f)
