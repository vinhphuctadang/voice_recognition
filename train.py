import soundlit as sl
import vneural as nr
import visualize as vz
import sounddevice as sd
from os import system

def listenToBoss ():
	import speech_recognition as sr
	r = sr.Recognizer ()
	with sr.Microphone () as source:
		audio = r.listen (source)
	try:
		txt = r.recognize_google (audio)
	except:
		return 'Error';

	if txt.lower () == 'exit':
		return 'exit'

	res = txt
	txt = ''
	for i in res:
		if i != ' ':
			txt += i
		else:
			txt += '+'

	system ('"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" google.com/search?q=%s' % txt)
	return txt
def main ():

	# system ('"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" google.com/search?q=haha')
	# return;	
	try:
		lobe = nr.load_lobe ()
	except:
		print ('No lobe found')
		return

	end = False
	stream = sl.getStream ()
	while 1:
		print ('hnhu is listening ... ')
		wav = sl.nextWord (stream)
		# sd.play(wav)
		wav = nr.transRaw (wav)
		pred = lobe.predict (wav.reshape (1,wav.shape[0], wav.shape[1]))
		print (pred)
		if pred[0][0]>pred[0][1]:
			print ("-------- YES sir you call me?")
			nr.beep ()
			print(listenToBoss ())
		else:
			print ("You have said something")

if __name__=='__main__':
	main ()