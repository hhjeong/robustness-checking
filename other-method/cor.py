#!/usr/bin/pypy

from math import log,sqrt

def mean(X):
	return sum(X)*1.0/len(X)

def getCor( A, B ):
	mA, mB = mean(A), mean(B)
	up = sum([(a-mA)*(b-mB) for a,b in zip(A,B)])
	dn = sum([(a-mA)**2 for a in A]) * sum([(b-mB)**2 for b in B])
	return 0 if dn == 0 else 1-up / sqrt(dn)

import sys

with open(sys.argv[1],'r') as inp:
	data = [map(float,row.strip().split()) for row in inp]

from FreqTable import FreqTable 
ft = FreqTable()

for i in xrange(len(data)):
	for j in xrange(i+1,len(data)):
		ft.put(getCor(data[i],data[j]))

with open(sys.argv[2],'w') as oup:
	for line in ft.freq2bin(100,0.0,2.0):
		print >> oup, "%f\t%d" % line
