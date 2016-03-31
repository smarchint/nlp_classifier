import pickle
from collections import Counter
import math
# import trian
# import test

import os

plus = 'pos.txt'
minus = 'neg.txt'
# test = 'aaa.txt'
def lower(fname):
	infile = open('temp_'+fname, 'r')
	data = infile.read()
	data= data.lower()
	data = data.replace("lrb", "")
	data = data.replace("rrb", "")
	outfile = open('temp_'+fname,'w')
	outfile.write(data)

def replace(fname):
	infile = open(fname, 'r')
	data = infile.read()
	data = data.replace("\"", "")
	data = data.replace(",", "")
	#
	data = data.replace("\n ", "\n")
	data = data.replace(".", "")
	data = data.replace("!", "")
	data = data.replace("/", "")
	data = data.replace("-", " ")
	data = data.replace("?", "")
	data = data.replace("`", "")
	data = data.replace("\'", "")
	data = data.replace(";", "")
	data = data.replace("&", "")
	data = data.replace("\\", "")
	data = data.replace("*", "")
	data = data.replace("$", "")
	data = data.replace(":", "")
	data = data.replace(" s ", " ")
	#
	data = data.replace("\ns ", "")


	s='0123456789'
	for i in s:
		data = data.replace(i,"")
	data = data.replace('ca nt','cant')
	data = data.replace('wo nt','wont')
	data = data.replace('ai nt','aint')
	#data = data.replace('ca nt','cant')
	outfile = open('temp_'+fname, 'w')
	outfile.write(data)

def remove(fname):
	stop = open('stopwords.txt','r')
	l=[]
	for word in stop:
		l.append(word[:-1])
	
	infile = open('temp_'+fname, 'r')
	data = infile.read()
	for stopword in l:
		#print stopword
		data = data.replace(" "+stopword+"\n","\n")
		data = data.replace(" "+stopword+" "," ")
		data = data.replace("\n"+stopword+" ","\n")
	outfile = open('temp_'+fname, 'w')
	outfile.write(data)

def dothat(l):
	counts = Counter(l)
	#counts is dictionary of word frequencies
	counts = {i:counts[i] for i in counts if counts[i]>=2}
	# for i in sorted(counts):
	# 	outfile.write(str(i) + ' : '+ str(counts[i])+'\n')

	return counts
#stores as dictionary
def pickleOut(temp,fname):
	pickle_out = open(fname+'.p', 'wb')
	pickle.dump(temp, pickle_out)
	pickle_out.close()
it =0
def err():
	global pos,neg,voc,db,tot_freq_pos,tot_freq_neg,voc_size
	# print 'pos',pos
	# print 'neg',neg
	# print 'voc',voc
	len(voc)
def freq():
	global it
	infile1 = open('train_'+plus,'r')
	infile2 = open('train_'+minus,'r')
	#outfile = open('vocabulary-freq.txt','w')
	#pf = open('freq_'+plus,'w')
	#nf = open('freq_'+minus,'w')
	#create list of words
	l = []

	#pos word frequency
	pfl=[]
	for line in infile1.readlines():
		flux = line.split(' ')
		flux[-1] = flux[-1][:-1]
		l = l + flux
		pfl = pfl + flux
	
	
	temp = dothat(pfl)
	pickleOut(temp,'pos_word_freq')
	#neg word freq
	nfl = []
	for line in infile2.readlines():
		flux = line.split(' ')
		flux[-1] = flux[-1][:-1]
		l = l + flux
		nfl = nfl + flux
	
	temp2 = dothat(nfl)
	pickleOut(temp2,'neg_word_freq')

	#temp = dothat(l)
	counts = Counter(l)
	#counts is dictionary of word frequencies
	counts = {i:counts[i] for i in counts if counts[i]>=2}
	print it,'*************************************'
	#print it,counts
	it+=1
	# for i in sorted(counts):
	# 	outfile1.write(str(i) + ' : '+ str(counts[i])+'\n')
	# 	outfile2.write(str(i)+'\n')

	pickleOut(counts,'all_word_freq')
	infile1.close()
	infile2.close()

def cleanData():
	for doc in [plus,minus]:
		replace(doc)
		lower(doc)
		remove(doc)

def fold10(doc):
	infile = open('temp_'+doc)
	# ls = infile.read().split('\n')
	# infile.close()
	# l = [ls[i:i+50] for i in xrange(0, len(ls), 50)]
	# for i in range(10):
	# 	outfile = open(str(i+1)+doc,'w')
	# 	for j in l[i]:
	# 		outfile.write(j+'\n')
	# outfile.close()


	for i in range(1,11):
		outfile = open(str(i)+doc,'a')
		for j in range(50):
			outfile.write(infile.readline())
		outfile.close()
#--------------------------------------------------------
#global pos,neg,voc,db,tot_freq_pos,tot_freq_neg,voc_size
pos,neg,voc,db={},{},{},{}
tot_freq_pos=0
tot_freq_neg=0
voc_size=0
def pickleIn(fname):
	pickle_in = open(fname+'.p','rb')
	db1 = pickle.load(pickle_in)
	#pickle_in.close()
	return db1


def pre_patch():
	global pos,neg,voc,db,tot_freq_pos,tot_freq_neg,voc_size
	voc_size = N()
	tot_freq_pos = total(pos)
	tot_freq_neg = total(neg)
	ls = [voc_size,tot_freq_neg,tot_freq_pos]
	pickleOut(ls,'net_word_freq')
def total(db1):
	#global pos,neg,voc,db,tot_freq_pos,tot_freq_neg,voc_size
	c=0
	for word in db1:
		c += db1[word]
	return c
def N():
	global voc
	#global voc
	count=0
	for word in voc:
		count += 1
	return count
def p(word,flag):
	global pos,neg,voc,db,tot_freq_pos,tot_freq_neg,voc_size
	db1 = neg
	tot = tot_freq_neg
	if flag==1:
		db1 = pos
		tot = tot_freq_pos
	tot = total(db1)
	if word in db1:
		return math.log10(db1[word]+1)-math.log10(tot+voc_size+1)
	else: 
		return math.log10(1)-math.log10(tot+voc_size)
def  create_model():
	global pos,neg,voc,db,tot_freq_pos,tot_freq_neg,voc_size
	db = {}
	for word in voc:
		#word : [pos_pob,neg_prob]
		db[word]=[p(word,1),p(word,0)]
		#print word,db[word]
	#print db
	pickleOut(db,'MNBmodel')

def q(doc,clas):
	global pos,neg,voc,db,tot_freq_pos,tot_freq_neg,voc_size
	#global db
	res = 0
	doc = doc.split()
	#print doc
	for word in doc:
		if word in voc:
			res += db[word][clas]
		else:
			res += math.log10(1)-math.log10(N()+voc_size+1)

	return res

def predict(doc):
	if q(doc,0)>q(doc,1):
		return 1
	else:
		return 0
def clean_mess():
	for f in ['all','net','pos','neg']:
		os.remove(f+'_word_freq.p')

	for f in ['train_pos.txt','train_neg.txt','MNBmodel.p']:
		os.remove(f)
def crossvalidate():
	global pos,neg,voc,db,tot_freq_pos,tot_freq_neg,voc_size
	sum_acc =0
	for i in range(1,11):
		pos,neg,voc,db={},{},{},{}
		tot_freq_pos=0
		tot_freq_neg=0
		voc_size=0
		# testdat1 = open(str(i+1)+plus).read()
		# testdat2 = open(str(i+1)+minus).read()
		# test = open('test.txt','w')
		# test.write(testdat1+testdat2)
		# test.close()
		traindat1,traindat2 = '',''
		for j in range(1,11):
			
			if j != i:
				inplus = open(str(j)+plus)
				traindat1 += inplus.read()
				inplus.close()
				inminus = open(str(j)+minus)
				traindat2 += inminus.read()
				inminus.close()
		intrain = open('train_'+plus,'w')
		intrain.write(traindat1)
		intrain.close()
		intrain = open('train_'+minus,'w')
		intrain.write(traindat2)
		intrain.close()

		ls =  (traindat1 + traindat2).split('\n')
		#print ls,len(ls)
		print 'length of taining dat :',len(ls)
		# if len(ls) == 1:print ls
		
		#freq print of train set
		freq()


		pos = pickleIn('pos_word_freq')
		neg = pickleIn('neg_word_freq')
		voc = pickleIn('all_word_freq')

		err()

		#counts in freq print of tain set
		pre_patch()

		ls =  pickleIn('net_word_freq')
		voc_size = ls[0]
		tot_freq_neg = ls[1]
		tot_freq_pos = ls[2]
		
		create_model()
		
		db = pickleIn('MNBmodel')
		#print db
		fp,fn,tp,tn = 0,0,0,0
		#acuracy,recall,precision
		tes = open(str(i)+plus,'r').read().split('\n')
		for doc in tes:
			if predict(doc)==1:
				tp += 1
			else:
				tn += 1
		#print tes
		testl = open(str(i)+minus,'r').readlines()

		for doc in testl:
			if predict(doc)==0:
				fn += 1
			else:
				fp += 1

		print fp,fn,tp,tn 
		accuracy = (tp+fn)/float(tp+tn+fn+fp)
		print 'accuracy',accuracy
		precision = tp/float(tp+tn)
		recall = tp/float(tp+fn)
		fmeasure = 2*precision*recall/float(precision+recall+1)*0.1
		sum_acc  +=  accuracy
		clean_mess()
	print sum_acc
	avg_acc = sum_acc/10
	print avg_acc




def main():
	# cleanData()
	# print "cleaned data : removed unwanted charecters, stopwords and lower cased"
	# fold10(plus)
	# fold10(minus)
	# print "split dataset into 10 folds"
	crossvalidate()



if __name__ == '__main__':
	main()
