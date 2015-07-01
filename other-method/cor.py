#!/usr/bin/python

from math import log,sqrt

def mean(X):
	return sum(X)*1.0/len(X)

def getCor( A, B ):
	mA, mB = mean(A), mean(B)
	up = sum([(a-mA)*(b-mB) for a,b in zip(A,B)])
	dn = sum([(a-mA)**2 for a in A]) * sum([(b-mB)**2 for b in B])
	return 0 if dn == 0 else up / sqrt(dn)

import sys, numpy

with open(sys.argv[1],'r') as inp:
	data = [map(float,row.strip().split()) for row in inp]


cor = [getCor(data[i],data[j]) for i in xrange(len(data)) for j in xrange(i+1,len(data))]

with open(sys.argv[2],'w') as oup:
	F, P = numpy.histogram(cor, 100)
	for f, p in zip(F,P):
		print >> oup, str(p) + '\t' + str(f)
