def lower(fname1,fname2):
	outfile = open('final_'+fname2,'w')
	infile = open(fname1+fname2, 'r')
	for line in infile:
		line = line.lower()
		outfile.write(line)

def replace2(fname):
	with open(fname, 'r') as infile,open('rem_unwanted_char_'+fname, 'w') as outfile:
		data = infile.read()
		data = data.replace("\"", "")
		data = data.replace(",", "")
		#
		data = data.replace("\n ", "\n")
		data = data.replace(".", "")
		data = data.replace("!", "")
		data = data.replace("/", "")
		data = data.replace("-", "")
		data = data.replace("?", "")
		data = data.replace("`", "")
		data = data.replace("\'", "")
		data = data.replace(";", "")
		data = data.replace("&", "")
		data = data.replace("\\", "")
		data = data.replace("*", "")
		data = data.replace("$", "")
		data = data.replace(":", "")
		data = data.replace(" s ", "")
		#
		data = data.replace("\ns ", "")


		s='0123456789'
		for i in s:
			data = data.replace(i,"")

		outfile.write(data)

def unique(fname):
	outfile = open('uniques_'+fname,'w')
	infile = open(fname, 'r')
	s = set([])
	for line in infile:
		s = s | set(line)
	outfile.write(str(s))

plus = 'pos.txt'
minus = 'neg.txt'

unique(plus)
unique(minus)

replace2(plus)
replace2(minus)

lower('rem_unwanted_char_',plus)
lower('rem_unwanted_char_',minus)

#OUTPUT
#final_pos.txt
#final_neg.txt