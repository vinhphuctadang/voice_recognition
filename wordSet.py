from collect import readInput 

__delimiter=',;.\n?*!#"-():“”/\\‘’–%… •\t><=+-*/'
	
def nextWord (buffer):
	word = ''
	for c in buffer:
		if c in __delimiter:
			if word != '':
				yield word.lower ()
			word = ''
		else:
			word += c
	if word != '':
		yield word.lower ()

def main ():

	words = set(readInput ())
	plug = set()

	for word in nextWord (open ('sample.txt', 'r', encoding='utf-8').read ()):
		if (word not in words) and (word not in plug):
			plug.add (word)

	train = open ('input.txt', 'a', encoding='utf-8')
	for word in plug:
		train.write (word+' ')
	train.close ()
	print ('Chèn thêm %d chữ' % len (plug))

if __name__=='__main__':
	main ()
