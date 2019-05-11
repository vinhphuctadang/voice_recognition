
from recorder import play 
from wordSet import nextWord
from time import time

def main ():
	now = time ()
	txt = 'Xin chào, tôi là kết quả công tác hôm nay'
	# print (txt)
	for word in nextWord (txt):
		print (word)
		play ('data/%s.mp3'%word)
	print ('Done after %.2fs'%(time()-now))
if __name__=='__main__':
	main ()