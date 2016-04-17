import pickle
from collections import Counter
import math
# import trian
# import test

import os
import re

plus = 'pos.txt'
minus = 'neg.txt'

pos,neg,pos_w,neg_w,voc,db,all_bigrams={},{},{},{},{},{},{}
tot_freq_pos=0
tot_freq_neg=0
voc_size=0
# test = 'aaa.txt'
def destroy(fname):
	if os.path.exists(fname):
		os.remove(fname)

def lower(fname):
	infile = open('temp_'+fname, 'r')
	data = infile.read()
	infile.close()
	data= data.lower()
	outfile = open('temp_'+fname,'w')
	outfile.write(data)
	outfile.close()

def replace2(fname):
	infile = open(fname, 'r')
	data = infile.read()
	data = data.lower()
	re.sub(r'\W+	', '', data)
	s='0123456789'
	for i in s:
		data = data.replace(i,"")
	data = data.replace('ca nt','cant')
	data = data.replace('wo nt','wont')
	data = data.replace('ai nt','aint')
	#data = data.replace('ca nt','cant')
	destroy('temp_'+fname)
	outfile = open('temp_'+fname, 'w')
	outfile.write(data)

def replace(fname):
	infile = open(fname, 'r')
	data = infile.read()
	infile.close()
	data = data.replace("\"", "")
	data = data.replace(",", "")
	#
	data = data.replace("\n ", "\n")
	data = data.replace(".", " ")
	data = data.replace("!", " ")
	data = data.replace("/", " ")
	data = data.replace("-", " ")
	data = data.replace("?", " ")
	data = data.replace("`", " ")
	data = data.replace("\'", " ")
	data = data.replace(";", " ")
	data = data.replace("&", " ")
	data = data.replace("\\", " ")
	data = data.replace("*", " ")
	data = data.replace("$", "")
	data = data.replace(":", " ")
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
	infile.close()
	for stopword in l:
		#print stopword
		data = data.replace(" "+stopword+"\n","\n")
		data = data.replace(" "+stopword+" "," ")
		data = data.replace("\n"+stopword+" ","\n")
	outfile = open('temp_'+fname, 'w')
	outfile.write(data)
	outfile.close()

def lis2dic(l):
	counts = Counter(l)
	#counts = {i:counts[i] for i in counts if counts[i]>=2}
	return counts

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
def tokenize(fname):
	infile = open(fname,'r')
	l=[]
	for line in infile.readlines():
		ls = line.split()
		ls = [i.strip('\n') for i in ls if i!='']
		ls += ['*','**']
		l += ls
	return l

def get_bigrams(fname):
	infile = open(fname,'r')
	bi_grams=[]
	for line in infile.readlines():
		ls = line.split()
		ls = [i.strip('\n') for i in ls if i != '']
		bi=[]
		if ls[0]:
			bi=[('*',ls[0])]
		n = len(ls)
		for i in range(n-1):
			bi.append((ls[i],ls[i+1]))
		if ls:
			bi.append((ls[n-1],'**'))
		bi_grams += bi		
	return bi_grams
def str_to_bigrams(doc):
	ls = doc.split()
	ls = [i.strip('\n') for i in ls if i != '']
	bi_grams=[]
	if ls:
		bi_grams=[('*',ls[0])]
	n = len(ls)
	for i in range(n-1):
		bi_grams.append((ls[i],ls[i+1]))
	if ls:
		bi_grams.append((ls[n-1],'**'))
	return bi_grams
def gen_frequencies():
	
	pbfl =get_bigrams('train_'+plus)
	temp = lis2dic(pbfl)
	pickleOut(temp,'pos_bigram_freq')
	
	pf = tokenize('train_'+plus)
	temp = lis2dic(pf)
	temp = {i:temp[i] for i in temp if temp[i]>=2}
	pickleOut(temp,'pos_word_freq')


	nbfl = get_bigrams('train_'+minus)
	temp = lis2dic(nbfl)
	pickleOut(temp,'neg_bigram_freq')
	
	nf = tokenize('train_'+minus)
	temp = lis2dic(nf)
	temp = {i:temp[i] for i in temp if temp[i]>=2}
	pickleOut(temp,'neg_word_freq')


	temp = lis2dic(pbfl+nbfl)
	#print temp
	pickleOut(temp,'all_bigram_freq')

	temp = lis2dic(pf+nf)
	temp = {i:temp[i] for i in temp if temp[i]>=2}
	#print temp
	pickleOut(temp,'all_word_freq')
def cleanData():
	for doc in [plus,minus]:
		replace(doc)
		lower(doc)
		remove(doc)

def fold10(doc):
	infile = open('temp_'+doc)
	for i in range(1,11):
		destroy(str(i)+doc)
		outfile = open(str(i)+doc,'w')
		for j in range(50):
			outfile.write(infile.readline())
		outfile.close()
	infile.close()
#--------------------------------------------------------
#global pos,neg,voc,db,tot_freq_pos,tot_freq_neg,voc_size

def pickleIn(fname):
	pickle_in = open(fname+'.p','rb')
	db1 = pickle.load(pickle_in)
	pickle_in.close()
	return db1
def pre_patch():
	global pos,neg,voc,db,tot_freq_pos,tot_freq_neg,voc_size,pos_w,neg_w
	voc_size = len(voc)+2
	tot_freq_pos = total(pos_w)
	tot_freq_neg = total(neg_w)
	ls = [voc_size,tot_freq_neg,tot_freq_pos]
	pickleOut(ls,'net_word_freq')
def total(db1):
	#global pos,neg,voc,db,tot_freq_pos,tot_freq_neg,voc_size
	c=0
	for word in db1:
		c += db1[word]
	return c
def p(bigram,flag):
	global pos,pos_w,neg_w,neg,voc,db,tot_freq_pos,tot_freq_neg,voc_size,all_bigrams
	db1 = neg
	db2 = neg_w
	if flag==1:
		db1 = pos
		db2 = pos_w
	tot = len(db1)
	if bigram in db1:
		if bigram[0] in db2:
			return math.log(db1[bigram]+1)-math.log(db2[bigram[0]]+voc_size)
		else:
			return math.log(db1[bigram]+1)-math.log(1+voc_size)
	else: 
		return math.log(1)-math.log(tot+voc_size)

def  create_model():
	global pos,pos_w,neg_w,neg,voc,db,tot_freq_pos,tot_freq_neg,voc_size,all_bigrams
	db = {}
	for bigram in all_bigrams:
		db[bigram]=[p(bigram,0),p(bigram,1)]
	destroy('MNBmodel.p')
	pickleOut(db,'MNBmodel')

#optimize here
def q(doc,clas):
	global pos,pos_w,neg_w,neg,voc,db,tot_freq_pos,tot_freq_neg,voc_size
	#global db
	res = 0
	doc = str_to_bigrams(doc)
	theta = len(neg)
	if clas == 1:
		theta = len(pos)
	for bigram in doc:
		if bigram in all_bigrams:
			res += db[bigram][clas]
		else:
			res += math.log(1)-math.log(theta+voc_size)
	return res

def predict(doc):
	if q(doc,1)>=q(doc,0):
		return 1 #pos
	else:
		return 0 #neg
def clean_mess():
	for f in ['all','pos','neg']:
		os.remove(f+'_bigram_freq.p')
	for f in ['all','pos','neg']:
		os.remove(f+'_word_freq.p')
	rem_files = ['train_pos.txt','train_neg.txt','MNBmodel.p']
	for f in rem_files:
		os.remove(f)
def crossvalidate():
	global pos,pos_w,neg_w,neg,voc,db,tot_freq_pos,tot_freq_neg,voc_size,all_bigrams
	sum_acc =0
	for i in range(1,11):
		pos,neg,voc,db,all_bigrams={},{},{},{},{}
		tot_freq_pos=0
		tot_freq_neg=0
		voc_size=0
		traindat1,traindat2 = '',''
		for j in range(1,11):
			
			if j != i:
				inplus = open(str(j)+plus)	
				traindat1 += inplus.read()
				inplus.close()
				inminus = open(str(j)+minus)
				traindat2 += inminus.read()
				inminus.close()
		destroy('train_'+plus)
		intrain = open('train_'+plus,'w')
		intrain.write(traindat1)
		intrain.close()
		destroy('train_'+minus)
		intrain = open('train_'+minus,'w')
		intrain.write(traindat2)
		intrain.close()

		ls =  (traindat1 + traindat2).split('\n')
		#print ls,len(ls)
		print 'length of taining dat :',len(ls)
		# if len(ls) == 1:print ls
		
		#freq print of train set
		gen_frequencies()


		pos = pickleIn('pos_bigram_freq')
		neg = pickleIn('neg_bigram_freq')
		all_bigrams = pickleIn('all_bigram_freq')

		pos_w = pickleIn('pos_word_freq')
		neg_w = pickleIn('neg_word_freq')
		voc = pickleIn('all_word_freq')
		

		# err()

		# counts in freq print of tain set
		pre_patch()



		ls =  pickleIn('net_word_freq')
		voc_size,tot_freq_neg,tot_freq_pos = ls[0],ls[1],ls[2]
		print ls


		create_model()
		


		db = pickleIn('MNBmodel')

		fp,fn,tp,tn = 0,0,0,0
		#acuracy,recall,precision
		tes = open(str(i)+plus,'r').read().split('\n')
		for doc in tes:
			if predict(doc)==1:
				tp += 1
			else:
				fn += 1
		#print tes
		testl = open(str(i)+minus,'r').readlines()

		for doc in testl:
			if predict(doc)==0:
				tn += 1
			else:
				fp += 1

		print fp,fn,tp,tn 
		accuracy = (tp+tn)/float(tp+tn+fn+fp)
		print 'accuracy',accuracy
		precision = tp/float(tp+tn)
		recall = tp/float(tp+fn)
		fmeasure = 2*precision*recall/float(precision+recall+1)
		sum_acc  +=  accuracy
		clean_mess()
	print sum_acc
	avg_acc = sum_acc/10.0
	print avg_acc


def main():
	cleanData()
	print "cleaned data : removed unwanted charecters, stopwords and lower cased"
	fold10(plus)
	fold10(minus)
	print "split dataset into 10 folds"
	crossvalidate()



if __name__ == '__main__':
	main()
