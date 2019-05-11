from recorder import record 
from numpy import savetxt as save
from numpy import array
import os
import csv 

if not os.path.isfile ('test.txt'):	
	data = record ('Start speaking ...')
	data.reshape (44100)
	save ('test.txt', data, delimiter=' ')
else:
	tmp = 	csv.reader (open('test.txt','r'), delimiter=' ')
	data = []
	for i in tmp:
		data.append 	 (float (i[0]))
	data = array(data)
print (data)

import python_speech_features as psf

mfcc = psf.mfcc (data, 44100, nfft=1103)
save ('testMfcc.txt', mfcc, delimiter=' ')
print (mfcc.shape)
import visualize as vz 
vz.plot (mfcc)
vz.show ()



