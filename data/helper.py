
import re

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def replace():
    string = open('pos.txt').read()
    new_str = re.sub('[^a-zA-Z0-9\n\.]', ' ', string)
    #new_str = re.sub('*[A-Z]*', '[a-z]', new_str)
    open('temp.txt', 'w').write(new_str)


def replace2():
    with open('pos.txt', 'r') as infile,open('temp.txt', 'w') as outfile:
        data = infile.read()
        data = data.replace("\"", "")
        data = data.replace(",", "")
        data = data.replace("\n ", "\n")
        outfile.write(data)
def lower(fname):
    with open(fname, 'r') as fileinput:
       for line in fileinput:
           line = line.lower()

def main():
    lower("temp.txt")
    replace2()
    replace()
    
main()