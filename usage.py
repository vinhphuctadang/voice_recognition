import numpy as np
import pandas as pd
# import sklearn as sk
import recorder as rd
import visualize as vz
import sounddevice as sd
import matplotlib.pyplot as plt
import soundlit as sl
import os
# from tkinter import *
import keras
# from keras.models import Sequential
# from keras.layers import Dense, Dropout, Activation, LSTM, Flatten, TimeDistributed, Conv1D, MaxPooling1D, MaxPooling2D, Conv2D
from keras import backend as K
import python_speech_features as psf
import random as rand
from standardize import loadSilences
from train import load_lobe, getMfcc
import winsound
def beep(f=500, d=500):
	"""
	Uses the Sound-playing interface for Windows to play a beep
		
	Arguments
	f: Frequency of the beep in Hz
	d: Duration of the beep in ms
	"""
	winsound.Beep(f,d) 
	
def listenToBoss ():
	import speech_recognition as sr
	from os import system
	r = sr.Recognizer ()
	with sr.Microphone () as source:
		audio = r.listen (source)
	try:
		txt = r.recognize_google (audio,language='vi-VN')
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
	return res

# record the word then mix with loaded silences
def record (stream,silences,fixedLen=44100,chunk=2048,threshold=100):
	mark = False
	word = []
	while 1:
		data = stream.read(chunk)
		data = np.frombuffer (data, 'Int16')
		
		if max (data) >= threshold:#if a noise can be heard
			mark = True
			word.extend (data)
			if len(word)>fixedLen:
				break
		elif mark:
			break

	idx = rand.randrange (0, len(silences))
	return np.concatenate ((word, silences[idx][0:fixedLen-len(word)]))
# listen to a word then get mfccs
def listen (stream, silences, fixedLen=44100):
	wrd = record (stream, silences, fixedLen)[0:fixedLen]
	mfcc = getMfcc (wrd)
	return mfcc

def main (): 
	lobe = load_lobe ()
	stream = sl.getStream(CHUNK=1024*2)
	silences = loadSilences ()

	while 1:
		print ('Listening ...')
		mfcc = listen (stream, silences)
		# vz.plot (mfcc)
		# vz.show ()

		mfcc = mfcc.reshape (1, mfcc.shape[0], 1)
		result = lobe.predict (mfcc)
		
		print (result)
		if result[0][0] > 0.5:
			print ('Yes')
			beep ()
			print ('Nói để tìm kiếm ...')
			val = listenToBoss ()
			print (val)
		else:
			print ('No')

if __name__=='__main__':
	main ()