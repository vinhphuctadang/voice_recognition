import numpy as np
import pandas as pd
import recorder as rd
import visualize as vz
import sounddevice as sd
import matplotlib.pyplot as plt
import os
import python_speech_features as psf
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

	R = pivot
	_len = len (signal)
	while R < _len:
		rmost = vz.clamp (R+step, pivot, _len)
		if max (signal[R:rmost]) - min (signal[R:rmost]) < threshold:
			break;
		R = rmost


	if outPick:
		return signal [L:vz.clamp (L+fixedLen, 0, len(signal))], L, R
	return signal [L:vz.clamp (L+fixedLen, 0, len(signal))], R

def mix (src, dst, dstX = 0):
	if dstX >= len(dst):
		raise ValueError ("mix point exceed orignal len (point,org_len)=(%d,%d)"%(dstX, len (dst)))

	__len = min (len (src), len(dst)-dstX)

	# print (__len)
	mix_seg = dst[dstX:dstX+__len] + src[0:__len]
	# if dstX == 0:
	# 	return mix_seg
	# print (dst[0:dststX])
	res = np.concatenate ((dst[0:dstX], mix_seg, dst[dstX+__len:len(dst)]))
	return res
def trim (wav, outOrgLen=False):
	mx, idx = vz.getMax (wav)
	res, L, R = getWave_fixedLen (wav, pivot = idx, outPick = True)
	if outOrgLen:
		return res, R-L
	return res


def execute (silences, inputFolder='./raw/',outputFolder = './train/', segment=500, verbose=True, defaultSilenceLen = defaultLen):

		
	import random as ran

	
	silences_list_len = len (silences) # number of silences sample

	for file in listFile (os.walk (inputFolder), ['*.wav']):
		org = rd.importSignal (inputFolder+file)
		wav, __len = trim (org, outOrgLen=True)
		

		for i in range(1):# range (max ((defaultSilenceLen - __len) // segment-2, 1)):
			idx = ran.randrange (0, silences_list_len)
			choice = silences [idx]
			seg = mix (wav, choice, i*segment)
			sname = outputFolder+'mix_%d_%d_%s'%(idx,i,file)
			rd.save (seg, sname)
			if verbose:
				print ("Saved file:%-40s with sample size:%5d"%(sname, len(seg)))

def pretest ():
	wav1 = rd.importSignal ('./raw/silent/silent0.wav')[0:defaultLen]
	wav2, __len = trim (rd.importSignal ('./raw/như/nhu1.wav'), outOrgLen = True)
	wav = mix (wav2, wav1, 0)
	
	fig = plt.gcf()
	i = 0
	
	seg = 1000
	count = (len(wav1) - __len) // seg
	print (count)
	while 1:
		i = (i+1) % count
		plt.clf ()
		wav = mix (wav2, wav1, i*seg)	
		plt.plot(wav)
		fig.canvas.draw()	
		plt.pause (0.6)
def loadSilences (dir='./raw/silent/'):
	silences = []
	for silent in listFile (os.walk (dir), ['*.wav']):

		silence = rd.importSignal ('%s%s'%(dir,silent))[0:defaultLen]	
		silences.append (silence)
		# print (len (silence))
	return silences

def generate ():

	silences = loadSilences ()
	execute (silences, inputFolder='./rawtest/', outputFolder='./test/', segment = 1000)


def main ():
	generate ()
	pass
if __name__=='__main__':
	main ()