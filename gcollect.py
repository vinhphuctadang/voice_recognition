from collect import readInput
from play import listFile 

import recorder as rd
from gtts import gTTS
import os

defaultInput = 'input.txt'
defaultDir = 'data/'
def collect (word):
	if os.path.isfile (defaultDir + '%s.mp3' % word):
		return False
	obj = gTTS (text=word,lang='vi',slow=False)
	obj.save (defaultDir + '%s.mp3' % word)
	return True

def main ():
	cnt = 0
	for word in readInput (defaultInput):
		print ('Đang tải: "%s"'%word)
		if collect (word):
			cnt += 1
	print ('Số lượng tải về: %d' % cnt)
	# f = listFile (os.walk ('./data/'), pattern=['*.mp3'])
	# # print (f)
	# for file in f:
	# 	# print (defaultDir + file)
	# 	rd.play (defaultDir + file)
if __name__=='__main__':
	main ()