import pickle
import math

plus = 'pos.txt'
minus = 'neg.txt'


def get_freq(fname):
	pickle_in = open(fname+'_word_freq.p','rb')
	db = pickle.load(pickle_in)
	#pickle_in.close()
	return db

def pickleOut(temp,fname):
	pickle_out = open(fname+'.p', 'wb')
	pickle.dump(temp, pickle_out)
	pickle_out.close()

pos = get_freq('pos')
neg = get_freq('neg')
voc = get_freq('all')
ls =  get_freq('net')
voc_size = ls[0]
tot_freq_neg = ls[1]
tot_freq_pos = ls[2]
#print voc_size,tot_freq_pos,tot_freq_neg
# def pre_patch():
# 	voc_size = N()
# 	tot_freq_pos = total(pos)
# 	tot_freq_neg = total(neg)
# 	ls = [voc_size,tot_freq_neg,tot_freq_pos]
# 	pickleOut(ls,'net_word_freq')

def total(db):
	count=0
	for word in db:
		count += db[word]
	return count
def N():
	global voc
	count=0
	for word in voc:
		count += 1
	return count

def p(word,flag):
	global pos,neg,voc_size
	db = neg
	tot = tot_freq_neg
	if flag==1:
		db = pos
		tot = tot_freq_pos
	tot = total(db)
	if word in db:
		return math.log10(db[word]+1)-math.log10(tot+voc_size)
	else:
		return math.log10(1)-math.log10(tot+voc_size)



def  create_model():
	global pos,neg
	db = {}
	for word in voc:
		db[word]=[p(word,1),p(word,0)]
		#print word,db[word]
	pickleOut(db,'MNBmodel')

#create_model()
#pre_patch()