import pickle
from collections import Counter
import math
import os
import re

plus = 'pos.txt'
minus = 'neg.txt'

pbf,nbf,bf,pwf,nwf,wf,db = {},{},{},{},{},{},{}
tot_freq_pos,tot_freq_neg,voc_size,b_voc_size=0,0,0,0
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
	counts = {i:counts[i] for i in counts if counts[i]>=2}
	return counts

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

def  truncate(fl):
	temp = lis2dic(fl)
	temp = {i:temp[i] for i in temp if temp[i]>=2}
	return temp

def gen_frequencies():
	pbfl =get_bigrams('train_'+plus)
	pbf = lis2dic(pbfl)

	nbfl = get_bigrams('train_'+minus)
	nbf = lis2dic(nbfl)

	bf = lis2dic(pbfl+nbfl)
	
	pwfl =  tokenize('train_'+plus)
	pwf  =  lis2dic(pwfl)

	nwfl =  tokenize('train_'+minus)
	nwf  =  lis2dic(nwfl)

	wf = lis2dic(pwfl+nwfl)

	print len(pwf),len(nwf),len(wf)
	
	return pbf,nbf,bf,pwf,nwf,wf

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

def get_total_freq(dictionary):
	return sum(dictionary.itervalues())
def error():
	global pbf,nbf,bf,pwf,nwf,wf
	global tot_freq_pos,tot_freq_neg,voc_size,b_voc_size
	mylist = bf.values()
	print Counter(mylist)


def p(bigram,flag):
	global pbf,nbf,bf,pwf,nwf,wf
	global tot_freq_pos,tot_freq_neg,voc_size,b_voc_size
	
	#print 'in model creation'
	#error()

	db1 = nbf
	db2 = nwf
	tot_freq = tot_freq_neg
	if flag==1:
		db1 = pbf
		db2 = pwf
		tot_freq = tot_freq_pos

	count_w = 0
	if bigram[0] in db2:
		count_w = db2[bigram[0]]

	if bigram in db1:
		return math.log(db1[bigram]+1)-math.log(count_w+voc_size+b_voc_size)
	else:
		temp = math.log(1)-math.log(tot_freq+voc_size)
		t1,t2=temp,temp
		if bigram[0] in db2:
			t1 = math.log10(db2[bigram[0]]+1)- math.log10(tot_freq + voc_size)
		if bigram[1] in db2:
			t1 =  math.log10(db2[bigram[1]]+1)- math.log10(tot_freq + voc_size)
		return t1+t2

def  create_model():
	global pbf,nbf,bf,pwf,nwf,wf
	global tot_freq_pos,tot_freq_neg,voc_size,b_voc_size
	db = {}
	for bigram in bf:
		db[bigram]=[p(bigram,0),p(bigram,1)]
	return db

#optimize here
def q(doc,clas):
	global pbf,nbf,bf,pwf,nwf,wf,db
	global tot_freq_pos,tot_freq_neg,voc_size,b_voc_size
	res = 0
	doc = str_to_bigrams(doc)
	db2 = nwf
	tot_freq = tot_freq_neg
	if clas == 1:
		db2 = pwf
		tot_freq = tot_freq_pos
	for bigram in doc:
		if bigram in bf:
			res += db[bigram][clas]
		else:
			temp = math.log(1)-math.log(tot_freq+voc_size)
			t1,t2=temp,temp
			if bigram[0] in db2:
				t1 = (db2[bigram[0]]+1)/(tot_freq + voc_size)
			if bigram[1] in db2:
				t1 = (db2[bigram[1]]+1)/(tot_freq + voc_size)
			res += t1+t2
	return res


def predict(doc):
	if q(doc,1)>=q(doc,0):
		return 1 #pos
	else:
		return 0 #neg
def clean_mess():
	for f in ['all','pos','neg']:
		destroy(f+'_bigram_freq.p')
	for f in ['all','pos','neg']:
		destroy(f+'_word_freq.p')
	rem_files = ['train_pos.txt','train_neg.txt','MNBmodel.p']
	for f in rem_files:
		destroy(f)
def crossvalidate():
	global pbf,nbf,bf,pwf,nwf,wf,db
	global tot_freq_pos,tot_freq_neg,voc_size,b_voc_size
	# global fame
	sum_acc =0
	#for each test case i
	for i in range(1,11):
		#initialization for each test case
		pos,neg,voc,db,all_bigrams={},{},{},{},{}
		tot_freq_pos=0
		tot_freq_neg=0
		voc_size=0
		traindat1,traindat2 = '',''
		#----------------------------------

		#remaining train set
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
		print 'length of taining dat :',len(ls)


		#model creation-------------------------

		#freq print of train set
		pbf,nbf,bf,pwf,nwf,wf = gen_frequencies()
		print 'len of all_bigrams',len(bf),'len of voc',len(wf)
		

			#assertion code-------------------------
		# temp = [bi[0] for bi in nbf]
		# temp += [bi[1] for bi in nbf]
		# temp  = set(temp)
		# count=0
		# word = 'abandon'
		# # print wf[word],nwf[word],pwf[word]
		# l = nwf.keys()
		# l.sort()
		# print l[:30]

		# l = nbf.keys()
		# m = []
		# for b in l:
		# 	m += [b[0],b[1]]
		# m = set(m)
		# m = list(m)
		# m.sort()
		# print m[:50]

		# for bigram in bf:
		# 	if bigram[0] == word or bigram[1] == word:
		# 		print bf[bigram],nbf[bigram],pbf[bigram]

		# word = 'abandon'
		# if bigram in nwf:
		# 	print 'word is present'
		# else:
		# 	print 'wor not present'

		# print 'fail count',count


		b_voc_size = len(bf)
		voc_size = len(wf)
		tot_freq_pos = get_total_freq(pwf)
		tot_freq_neg = get_total_freq(nwf)
		
		db = create_model()

		# prediction phase----------------------

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

		print 'fp,fn,tp,tn ',fp,fn,tp,tn 
		accuracy = (tp+tn)/float(tp+tn+fn+fp)
		print 'accuracy',accuracy
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
