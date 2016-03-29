from collections import Counter

plus = 'pos.txt'
minus = 'neg.txt'

def freq():
	infile1 = open('rem_stopwords_'+plus,'r')
	infile2 = open('rem_stopwords_'+minus,'r')
	outfile1 = open('vocabulary-freq.txt','w')
	outfile2 = open('vocabulary.txt','w')
	#create list of words
	l = []
	for line in infile1.readlines():
		flux = line.split(' ')
		flux[-1] = flux[-1][:-1]
		l = l + flux
	for line in infile2.readlines():
		flux = line.split(' ')
		flux[-1] = flux[-1][:-1]
		l = l + flux
	#print l
	counts = Counter(l)
	#counts is dictionary of word frequencies
	counts = {i:counts[i] for i in counts if counts[i]>1}
	for i in sorted(counts):
		outfile1.write(str(i) + ' : '+ str(counts[i])+'\n')
		outfile2.write(str(i)+'\n')


freq()