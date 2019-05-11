import pyaudio
import numpy as np
import sounddevice as sd
import visualize as vz 

CHUNK_SIZE = 1024

def getStream(CHUNK = CHUNK_SIZE, FORMAT = pyaudio.paInt16, 
	CHANNELS = 1, RATE = 44100):
	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
					channels=CHANNELS,
					rate=RATE,
					input=True,
					frames_per_buffer=CHUNK)
	return stream

def record (stream, time = 2, rate = 44100, chunk = 1024):
	frames = []
	for i in range(0, int(rate / chunk * time)):
		data = stream.read(chunk)
		data = np.frombuffer (data, 'Int16')
		frames.extend(data)
	return frames

def nextWord (stream, hearable=200, mxLen=44100, chunk=CHUNK_SIZE):
	mark = False
	word = []
	while 1:
		data = stream.read(chunk)
		data = np.frombuffer (data, 'Int16')
		# print (max (data), min (data))
		if max (data) - min (data) >= hearable:#if a noise can be heard
			mark = True
			word.extend (data)
			if len(word)>mxLen:
				return word
		elif mark:
			return word
	pass
def firstExperiment (st):
	for i in range(2):
		print ('recording...')
		fr = record (st)
		print (fr)

		from visualize import getWave_pivot_jump as gpj, getMax

		mx, idx = getMax (fr)
		trim, L = gpj (fr, pivot=idx, outPick = True)
		sd.play (trim)
		vz.plot (fr)	
		vz.plot (trim, L)
		vz.show ()

def secondOne (st):
	wrd = nextWord (st, hearable = 280, chunk=1024) 
	# print (wrd)
	sd.play (wrd)
	vz.plot (wrd)
	vz.show ()

def getApprSilence ():
	SL = 0
	return SL
def main ():
	print ('Listening for a word ...')
	st = getStream ()
	#firstExperiment (st)
	secondOne (st)


if __name__=='__main__':
	main ()