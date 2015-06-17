from math import ceil

class FreqTable:
	def __init__(self, precision=4):
		self.order = 10**precision
		self.freq = [0 for i in xrange(2*self.order+1)]
		self.total = 0

	def put(self, num):
		self.freq[int(num*self.order)] += 1
		self.total += 1


	def freq2bin(self,binSize,minPos,maxPos):
		mini = int(minPos*self.order)
		maxi = int(maxPos*self.order)

		width = int(ceil((maxi-mini)*1.0/binSize))

		return [(i*1.0/self.order,sum(self.freq[i:i+width])) for i in xrange(mini,maxi+1,width)] 





