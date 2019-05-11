import recorder as rd
#import re
folder = './train/'
def readInput (name='input.txt'):
	f=open (name,'r',encoding='utf-8')
	data = str(f.read ())
	f.close ()
	return data.split ()

def exists (name):# check wav file's existential
	import os
	result = os.path.isfile(folder+'%s.wav' % name)
	return result

def recordWord (word, chExist=True):#record a word
	if (chExist and exists (word)):
		return
	data = rd.record ('Đọc: "%s" ...' % word,time=2)
	rd.save (data, folder+'%s.wav'%word)
	print ('--------------------------------------')
def recordByTimes (word,times=9):
	for i in range(times):
		recordWord (word+"%d"%(i));

def main ():

	recordByTimes ('silent',times=50)
	return
	# rd.plot ('chị.wav')
	print ('Bắt đầu thu thập dữ liệu ...')
	words = readInput ()
	for word in words:
		recordWord (word)
	print ('Xong, cảm ơn')

if __name__=='__main__':
	main ()