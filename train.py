import numpy as np
import pandas as pd
# import sklearn as sk
import recorder as rd
import visualize as vz
import sounddevice as sd
import matplotlib.pyplot as plt
import os
# from tkinter import *
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, LSTM, Flatten, TimeDistributed, Conv1D, MaxPooling1D, MaxPooling2D, Conv2D
from keras import backend as K
import python_speech_features as psf
import vneural as vr
from play import listFile

defaultLen = 44100
particle = 100

def getWave_fixedLen (signal, pivot = 0, step=500, threshold=200, outPick = False, fixedLen = defaultLen):
	L = pivot

	while L > 0: 
		lmost = vz.clamp (L-step, 0, pivot)		
		# print (lmost,L)
		if max (signal[lmost:L]) - min (signal[lmost:L]) < threshold:
			# print (max (signal[lmost:L]) - min (signal[lmost:L]))
			break;
		L=lmost

	if outPick:
		return signal [L:vz.clamp (L+fixedLen, 0, len(signal))], L
	return signal [L:vz.clamp (L+fixedLen, 0, len(signal))]

def network_1 ():
	classifier = Sequential()
	classifier.add (Conv1D (32, 2, input_shape = (99 * 13, 1), activation = 'relu')) # with mfcc feature
	classifier.add (MaxPooling1D (pool_size = 3))
	classifier.add (Dropout(0.2))
	classifier.add (Conv1D (128, kernel_size = 3, activation = 'relu'))
	classifier.add (MaxPooling1D (pool_size = 5))
	classifier.add (Conv1D (128*2, kernel_size = 5, activation = 'relu'))
	classifier.add (MaxPooling1D (pool_size = 3))
	classifier.add (Dropout(0.2))
	classifier.add (Conv1D (128, kernel_size = 3, activation = 'relu'))
	classifier.add (MaxPooling1D (pool_size = 5))
	classifier.add (Conv1D (32, kernel_size = 2, activation = 'relu'))
	classifier.add (Flatten ())
	classifier.add (Dense (1, activation = 'sigmoid'))
	# classifier.add (Activation('sigmoid'))
	classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
	return classifier
def scale(X):
	sm = np.ndarray([])
	if type(X) == type(sm):
		sc = abs(max (X.max(axis=0), abs (X.min(axis=0))))
	else:
		sc = abs(max (max(X), abs (min (X))))
	return X/sc 

def getMfcc (wav):
	wav = scale (wav)
	mfcc = psf.mfcc (wav, defaultLen, nfft=1103)
	mfcc = scale (mfcc.reshape (mfcc.shape[0]*mfcc.shape[1]))
	return mfcc

def loadMfccFromFile (name):
	wav = rd.importSignal (name)
	return getMfcc (wav)
	
def loadFolder (nhu,label):
	import json
	if os.path.isfile (nhu+'cache'):
		a = np.loadtxt (nhu+'cache')
		return np.array(a), np.array([label] * len (a))
	else:
		X_train = []
		Y_train = []

		flist = listFile (os.walk(nhu), ['*.wav'])
		i = 0
		for file in flist:
			i += 1
			print ('%4d/%4d. Loading %-40s for label %5d' %(i, len (flist), nhu+file, label))
			mfcc = loadMfccFromFile (nhu+file)
			X_train.append (mfcc)
			Y_train.append (label)
		# print (X_train)
		np.savetxt (nhu+'cache', X_train)
		return np.array(X_train), np.array(Y_train)
def loadData ():

	print ("Loading data...")
	X_train = []
	Y_train = []

	folderList = {'./train/như/':1, './train/other/':0}
	for key in folderList:
		tmpX, tmpY = loadFolder (key, folderList[key])
		X_train.extend (tmpX)
		Y_train.extend (tmpY)
	return np.array (X_train), np.array(Y_train)
def loadTest ():
	res, tmp = loadFolder ('./test/',0)
	return [res]

def save_lobe (lobe,name='model.keras'):
	lobe.save(name)

def load_lobe (name='model.keras'):
	from keras.models import load_model
	model = load_model(name)
	return model

def main ():

	# print (X_train)
	if os.path.isfile ('model.keras'):
		model = load_lobe ()
	else:
		model = network_1 ()


	# for train purpose only
	# follow this standard
	X_train, Y_train = loadData ()
	X_train = X_train.reshape (X_train.shape[0], X_train.shape[1], 1)
	# 

	model.fit (X_train, Y_train, batch_size=32, nb_epoch = 50)
	save_lobe (model)

	for file in listFile (os.walk ('./test/'), ['*nhu*.wav']):
		mfcc = loadMfccFromFile ('./test/'+file)
		mfcc = mfcc.reshape (1, mfcc.shape[0], 1)

		pred = model.predict (mfcc)
		print ('Predict for %-40s:'%file, pred, pred[0][0]>0.5)

	pass
if __name__=='__main__':
	main ()