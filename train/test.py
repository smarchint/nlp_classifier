import pickle

def pickleIn(fname):
	pickle_in = open(fname+'.p','rb')
	db = pickle.load(pickle_in)
	#pickle_in.close()
	return db

db = pickleIn('MNBmodle')
def p(doc,clas):
	global db
	res = 0
	for word in doc:
		res += math.log10(db[word][clas])
	return res


def predict(doc):
	if p(doc,0)>p(doc,1):
		return 0
	else:
		return 1

def main():
	#open test file
	# for doc in testfile:
	# 	print predict(doc)

if __name__ == '__main__':
	main()