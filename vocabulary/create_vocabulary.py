from collections import Counter
import pickle

plus = 'pos.txt'
minus = 'neg.txt'

# def dothis(infile):
# 	l=[]
# 	for line in infile.readlines():
# 		flux = line.split(' ')
# 		flux[-1] = flux[-1][:-1]
# 		l = l + flux

#word frequency print
def dothat(l,outfile):
	counts = Counter(l)
	#counts is dictionary of word frequencies
	counts = {i:counts[i] for i in counts if counts[i]>2}
	for i in sorted(counts):
		outfile.write(str(i) + ' : '+ str(counts[i])+'\n')

	return counts

def pickleOut(temp,fname):
	pickle_out = open(fname+'_word_freq.p', 'wb')
	pickle.dump(temp, pickle_out)
	pickle_out.close()



def freq():
	infile1 = open('rem_stopwords_'+plus,'r')
	infile2 = open('rem_stopwords_'+minus,'r')
	outfile1 = open('vocabulary-freq.txt','w')
	outfile2 = open('vocabulary.txt','w')
	pf = open('word_freq_pos.txt','w')
	nf = open('word_freq_neg.txt','w')
	#create list of words
	l = []

	#pos word frequency
	pfl=[]
	for line in infile1.readlines():
		flux = line.split(' ')
		flux[-1] = flux[-1][:-1]
		l = l + flux
		pfl = pfl + flux
	
	
	temp = dothat(pfl,pf)
	pickleOut(temp,'pos')
	#neg word freq
	nfl = []
	for line in infile2.readlines():
		flux = line.split(' ')
		flux[-1] = flux[-1][:-1]
		l = l + flux
		nfl = nfl + flux
	
	temp2 = dothat(nfl,nf)
	pickleOut(temp2,'neg')

	#print l
	counts = Counter(l)
	#counts is dictionary of word frequencies
	counts = {i:counts[i] for i in counts if counts[i]>2}
	for i in sorted(counts):
		outfile1.write(str(i) + ' : '+ str(counts[i])+'\n')
		outfile2.write(str(i)+'\n')

	pickleOut(counts,'all')

freq()
