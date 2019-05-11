import numpy as np
import pandas as pd
import sklearn as sk
import recorder as rd
import visualize as vz
import sounddevice as sd
import os
# from tkinter import *
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, LSTM, Flatten, TimeDistributed, Conv1D, MaxPooling1D, MaxPooling2D, Conv2D
from keras import backend as K
import python_speech_features as psf

# def warn(*args, **kwargs):
#     pass
# import warnings
# warnings.warn = warn #disable all warning

folder = './train/'
defaultLen = 44100
particle = 100

def voice_lobe ():
	classifier = Sequential()
	classifier.add(Dense(output_dim=256, init='uniform', activation='relu', input_dim=44100, bias_initializer=keras.initializers.Ones())) # that fixed rate would become new
	classifier.add(Dropout(0.1))
	classifier.add(Dense(output_dim=128, init='uniform', activation='relu', bias_initializer=keras.initializers.Ones()))
	classifier.add(Dropout(0.1))
	classifier.add(Dense(output_dim=32, init='uniform', activation='relu', bias_initializer=keras.initializers.Ones()))
	classifier.add(Dense(output_dim=1, init='uniform', activation='sigmoid',bias_initializer=keras.initializers.Ones()))
	classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
	return classifier
def voice_lobe_2nd ():

	classifier = Sequential()
	classifier.add(LSTM(units=50, return_sequences=False, input_shape=(99, 13))) 
	classifier.add(Dropout(0.2))
	classifier.add(Dense(units=1, activation='sigmoid'))
	classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
	return classifier

def voice_lobe_3nd ():

	classifier = Sequential()
	classifier.add(LSTM(units=50, return_sequences=True, input_shape=(99, 13))) 
	classifier.add(Dropout(0.2))
	classifier.add(LSTM(units=50, return_sequences=False)) 
	classifier.add(Dropout(0.2))
	# classifier.add(Flatten())
	classifier.add(Dense(units=1, activation='relu'))
	classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
	return classifier

def voice_lobe_3rd_2 ():

	classifier = Sequential()

	classifier.add(LSTM(units=50, return_sequences=True, input_shape=(99, 13))) 
	classifier.add(Dropout(0.2))
	classifier.add(LSTM(units=50, return_sequences=False)) 
	classifier.add(Dropout(0.2))
	# classifier.add(Flatten())
	classifier.add(Dense (1,activation='sigmoid'))
	classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
	return classifier
def voice_lobe_4th ():#needs half of a second for 44.1kHz sound wave
					# inefficent model due to acc of 0.64 (fluctuate in range of 0.6-0.7)
	classifier = Sequential()
	classifier.add (Conv1D (32, 100, input_shape = (22050, 1))) 
	classifier.add (MaxPooling1D (pool_size = 100))
	classifier.add(Dropout(0.2))
	classifier.add (Conv1D (32, 100))
	classifier.add (MaxPooling1D (pool_size = 100))
	# classifier.add (Conv1D (32, 100	))
	# classifier.add (MaxPooling1D (pool_size = 3))
	# classifier.add(Dropout(0.2))

	# classifier.add (Conv1D (64, activation = 'softmax'))	
	# classifier.add (Conv1D (32, activation = 'relu'))
	# classifier.add (Flatten ())
	classifier.add (Flatten ())
	classifier.add (Dense (2))
	classifier.add (Activation('sigmoid'))

	classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
	return classifier


def voice_lobe_4th_2nd ():
	classifier = Sequential()

	classifier.add (Conv1D (128, 3, input_shape = (99, 13))) 
	classifier.add (MaxPooling1D (pool_size = 3))
	classifier.add(Dropout(0.2))
	classifier.add (Conv1D (100, 3))
	classifier.add (MaxPooling1D (pool_size = 3))
	classifier.add(Dropout(0.2))
	classifier.add (Conv1D (100, 3))
	classifier.add (MaxPooling1D (pool_size = 5))
	classifier.add (Dropout(0.2))
	classifier.add (Flatten ())
	# classifier.add (LSTM (10, return_sequences = False))
	classifier.add (Dense (10, activation='relu'))
	classifier.add (Dense (2, activation = 'sigmoid'))
	# classifier.add (Activation('sigmoid'))
	classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
	return classifier
def save_lobe (lobe,name='model.keras'):
	lobe.save(name)

def load_lobe (name='model.keras'):
	from keras.models import load_model
	model = load_model(name)
	return model

def scale(X):
	sm = np.ndarray([])
	if type(X) == type(sm):
		sc = max (X.max(axis=0), abs (X.min(axis=0)))
	else:
		sc = max (max(X), abs (min (X)))
	return X/sc 

def balanceLen (trim, slen = defaultLen):
	if len(trim)<slen:
		trim = np.concatenate ((trim, [0] * (slen-len(trim)) ) )
		return trim
	return trim[0:slen]

def trimWord (wav, slen=defaultLen, threshold = 0.1):
	mx, idx = vz.getMax (wav)
	# print (mx, idx)
	trim = vz.getWave_pivot_jump (wav, pivot=idx, step=1500, threshold=threshold)
	return balanceLen (trim)

def processWave (wav):
	return scale (wav)

def collect ():
	root, dirs, files = next (os.walk (folder))
	yes = []
	no = []
	import fnmatch as fm
	for file in files:
		if fm.fnmatch (file, 'nhu*'):
			yes.append (file)
		else:
			no.append (file)
	return yes, no

def transRaw (wav,trim=False):

	# return wav;
	wav =processWave (wav)
	if trim:
		wav = trimWord (wav, slen=defaultLen)
	# return wav.reshape (defaultLen, 1)
	else:
		wav = balanceLen (wav)
	mfcc = psf.mfcc (wav, defaultLen, nfft=1103)
	return mfcc

def importData (yes, no):
	X_train = []
	Y_train = []
	

	def fimport (i, label):
		mfcc = transRaw (rd.importSignal (folder+i), trim = True)
		# mfcc = mfcc.reshape (defaultLen // particle, particle)
		# wav = processWave (rd.importSignal (folder+i))	
		# sd.play (wav)
		# sd.wait ()
		# vz.plot (wav)
		# vz.show ()
		X_train.append (mfcc)
		Y_train.append (label)

	for i in yes:
		fimport (i, [1,0])
	for i in no:
		fimport (i, [0,1])
	
	return np.array(X_train), np.array(Y_train)

def ask (caption='Call me?', title='Question'):
	from tkinter import Tk
	from tkinter import messagebox
	wnd = Tk ()
	wnd.wm_withdraw()
	result = messagebox.askyesnocancel (title, caption, icon='warning')
	wnd.destroy ()
	return result

def beep ():
	import winsound
	frequency = 1000  # Set Frequency To 2500 Hertz
	duration = 250  # Set Duration To 1000 ms == 1 second
	winsound.Beep(frequency, duration)
def registerCtrlC ():
	import signal
	import sys
	def signal_handler(sig, frame):
			print('You pressed Ctrl+C!')
			sys.exit(0)

	signal.signal(signal.SIGINT, signal_handler)
def main ():
	# ask ()
	# return;
	# os.environ["CUDA_VISIBLE_DEVICES"]="-1"
	# from play import listFile
	# print (listFile (pattern=['nhu*']))	
	# return
	from play import listFile	
	# print (listFile (pattern=['khong*']))
	lobe = None
	if not os.path.isfile ('model.keras'):
		lobe = voice_lobe_4th_2nd ()
		print (lobe.summary ())
		# return;
		yes, no = collect ()
		print ('Importing Data set ...')
		X_train, Y_train = importData (yes, no)
		# Y_train = Y_train.reshape(Y_train.shape[0], 1, 1)
		# print (Y_train.shape)
		# Y_train = Y_train.reshape (1, Y_train.shape[0], 1)
		# X_train = X_train.reshape (len(X_train), defaultLen // particle, particle)
		# Y_train = Y_train.reshape (len(Y_train), 1)
		# print (X_train)
		# return;
		# print (X_train)
		lobe.fit (X_train, Y_train, batch_size=len(X_train), nb_epoch=300)
		save_lobe (lobe)	
	else:
		lobe = load_lobe ()
	# return;
	# from ann_visualizer.visualize import ann_viz;
	# ann_viz(lobe, title="My second neural network")

	

	def check (i):
		from time import time
		wav = rd.importSignal (i)
		mfcc = transRaw (wav, trim=True) # have to trim a word
		#from time import sleep
		mfcc=mfcc.reshape (1, mfcc.shape[0], mfcc.shape[1])	
		# mfcc = mfcc.reshape (1, defaultLen // particle, particle)

		mark = time ()
		pred = lobe.predict (mfcc)
		print ('%-40s' % str(pred),'for %10s estimate time in second: %5.4f'%(i,time()-mark),end=' ')
		chosen = 0
		mx = 0
		for i in range (len(pred[0])):
			if mx<pred[0][i]:
				chosen = i
				mx = pred[0][i]
		print ('label:',chosen)

		return (pred[0][0] >= 0.5)


	# for i in listFile (pattern=['nhu*']):
		# check (i)
	# return;
	cnt = 0
	_len = 0
	for i in listFile (pattern=['nhu*','khong*','toi*']):
		if check (i):
			cnt += 1
		_len += 1

	# return ;
	# print ('Actually correct:%d/%d = %.2f'%(cnt,_len, 1.0*cnt/_len))

	# return;
	# print (lobe.summary ())
	# save_lobe (lobe)

	registerCtrlC ()
	import soundlit as sl
	stream = sl.getStream ()
	while 1:
		print ('hnhu is listening ... ')
		# wav = sl.record (stream, time=1)

		# if np.amax(wav) - np.amin(wav) <= 2500:
		# 	continue
		wav = sl.nextWord (stream)
		sd.play(wav)
		# from time import sleep 
		# sleep (1)
		# sd.wait ()
		wav = transRaw (wav)
		# wav = rd.record ('Start saying ... ',time=2)
		# wav = trimWord (processWave (wav.flatten ()))
		# print (wav)
		pred = lobe.predict (wav.reshape (1,wav.shape[0], wav.shape[1]))
		print (pred)
		# vz.plot (wav)
		# vz.show ()
		if pred[0][0]>pred[0][1]:
			print ("-------- YES sir you call me?")
			beep ()
		else:
			print ("You have said something")
if __name__=='__main__':
	main ()