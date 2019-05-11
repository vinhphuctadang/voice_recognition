import sounddevice as sd 
import soundfile as sf 
import matplotlib.pyplot as plt
import numpy as np
import wave
from pyglet.resource import media
from time import sleep 
# from pygame import mixer

def importSignal (name, dtype='Int16'):
	spf = wave.open(name,'r')
	signal = spf.readframes(-1)
	# print (len (signal))
	signal = np.fromstring(signal, dtype)
	# print (signal)
	if spf.getnchannels() == 2:
		raise ValueError ('Mone wave supported')
	return signal

def plot (signal,name='sound'):
	
	# print (signal)
	plt.figure(1)
	plt.title(name)
	plt.plot(signal)
	plt.show()

def play (name):

	med = media (name)
	med.play ()
	sleep (med.duration-0.3)
	return med

def record (prompt, time=1):
	print (prompt)
	sd.default.channels = 1
	data = sd.rec (int (time*44100))
	sd.wait ()
	return data

def save (data,name):
	sf.write (name, data, 44100)	

def init ():
	mixer.init ()
def main ():
	pass

# init ()
if __name__ == '__main__':
	main ()

