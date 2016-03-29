def remove(fname):
	stop = open('stopwords.txt','r')
	l=[]
	for word in stop:
		l.append(word[:-1])
	
	with open('final_'+fname, 'r') as infile,open('rem_stopwords_'+fname, 'w') as outfile:
		data = infile.read()
		for i in l:
			print i
			data = data.replace(" "+i+"\n","\n")
			data = data.replace(" "+i+" "," ")
			data = data.replace("\n"+i+" ","\n")
		outfile.write(data)

# def rem(fname):
# 	stop = open('stopwords.txt','r')
# 	l=[]
# 	for word in stop:
# 		l.append(word[:-1])
	
# 	with open('final_'+fname, 'r') as infile,open('rem_stopwords_'+fname, 'w') as outfile:
# 		data = infile.read()
# 		for i in l:
# 			print i
# 			data = data.replace(" "+i+" ","")
# 		outfile.write(data)
remove('pos.txt')
remove('neg.txt')