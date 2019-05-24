import numpy as np
import pandas as pd
# import sklearn as sk
import recorder as rd
import visualize as vz
import sounddevice as sd
import matplotlib.pyplot as plt
import soundlit as sl
import os
import keras
from keras import backend as K
import python_speech_features as psf
import random as rand
from standardize import loadSilences
from train import load_lobe, getMfcc
import winsound
def beep(f=500, d=500):
	winsound.Beep(f,d) 
	
def listenToBoss ():
	import speech_recognition as sr
	
	r = sr.Recognizer ()
	try:
		with sr.Microphone () as source:
			audio = r.listen (source, timeout=3)
		txt = r.recognize_google (audio,language='vi-VN')
	except:
		return 'error'

	if txt.lower () == 'hủy':
		return txt.lower ()

	return txt

def action ():
	from os import system
	print ('Yes')
	beep ()
	print ('Tôi đang lắng nghe ...')
	val = listenToBoss ()

	if val == 'tắt máy':
		system ('shutdown /h')
	elif val != 'error' and val != 'hủy':
		if '.' in val:
			system ('"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" %s' % val)
		else:
			system ('"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" google.com/search?q=%s' % val.replace (' ', '+'))

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
	lobe = load_lobe () # model.keras
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
		if result[0][0] > 0.9:
			action ()
		else:
			print ('No')

if __name__=='__main__':
	main ()