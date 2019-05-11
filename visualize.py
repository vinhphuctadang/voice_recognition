
import recorder as rd
import numpy as np
import matplotlib.pyplot as plt
import math
import sounddevice as sd
from play import listFile

def test ():
	file = 'tmp.wav'
	signal = rd.importSignal (file);
	print (signal)
	print (type(signal))
	rd.plot (signal, file)
def emulateData ():
	buffer = open ('input.txt').read ()
	data = list(map(int, buffer.split ()))
	return list (data)


def plotGaussian (signal, x_start=-10, x_end=10, mul=1.0):
	import math
	mean = np.mean (signal)
	mset = [(x-mean)**2 for x in signal]
	variant = np.mean (mset)    
	__sqrt = math.sqrt (2*math.pi*variant)
	x = np.linspace (x_start, x_end,100)
	y = mul*np.exp (-(x-mean)**2/(2*variant)) / __sqrt;
	plt.plot (x,y)
	
def getMax (a):
	res = -2000000000
	idx = 0
	for i in range(len(a)):
		if res < a[i]:
			res = a[i]
			idx = i
	return res, idx

def checkRgn (signal, threshold):
	for i in signal:
		if abs(i) >= threshold:
			return True

	return False

def clamp (val, mn, mx):
	if val < mn:
		return mn
	if val > mx:
		return mx
	return val

def getWave_pivot_jump (signal, pivot = 0, step=500, threshold=120, outPick = False):# 3rd improvement: using step range

	L = pivot

	while L > 0: 
		lmost = clamp (L-step, 0, pivot)		
		# print (lmost,L)
		if max (signal[lmost:L]) - min (signal[lmost:L]) < threshold:
			break;
		L=lmost

	R = pivot
	_len = len (signal)
	while R < _len:
		rmost = clamp (R+step, pivot, _len)
		if max (signal[R:rmost]) - min (signal[R:rmost]) < threshold:
			break;
		R = rmost
	if not outPick:
		return signal[L:R]

	return signal[L:R], L	

def getWave_pivot (signal, pivot = 0, threshold=100000, outPick = False):# second developement, using next greedy
	L = pivot
	while L > 0: 
		
		if abs (signal[L]) < threshold:
			if not checkRgn(signal[clamp (L-500, 0, L):L], threshold):
				break;
		L-=1

	R = pivot
	_len = len (signal)
	while R < _len:
		if abs (signal[R]) < threshold:
			if not checkRgn(signal[R:clamp (R+500, R, _len)], threshold):
				# print(signal[R])
				break;
		R+=1
	if not outPick:
		return signal[L:R]
		
	return signal[L:R], L

def plotEach (signal):

	# plot (signal) 
	mx, idx = getMax (signal)
	cut, L = getWave_pivot_jump (signal, pivot=idx, threshold=130, step=600, outPick=True) # silent thresholds
	plot (signal)


def samplePlot (fList):
	import numpy as np
	import matplotlib.pyplot as plt

	from matplotlib.ticker import NullFormatter  # useful for `logit` scale

	# Fixing random state for reproducibility
	# plot with various axes scales
	plt.figure(1)
	i = 0
	for file in fList:
		i+=1
		print (file)
		plt.subplot(330+i)
		signal = rd.importSignal (file)
		plotEach (signal)

			
	# Format the minor tick labels of the y-axis into empty strings with
	# `NullFormatter`, to avoid cumbering the axis with too many labels.
	plt.gca().yaxis.set_minor_formatter(NullFormatter())
	# Adjust the subplot layout, because the logit one may take more space
	# than usual, due to y-tick labels like "1 - 10^{-3}"
	plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,
	                    wspace=0.35)

	plt.show()

def show ():
	plt.show ()
def getWave (signal, threshold=100000, outPick=False): #1st thinking
	L = 0
	R = len (signal)
	for i in range(0,len(signal)):
		if signal[i] < 0 and -signal[i]>=threshold:
			break;
		if signal[i] > 0 and signal[i]>=threshold:
			break;
		L+=1
	for i in range(len(signal)-1,-1,-1):
		if signal[i] < 0 and -signal[i]>=threshold:
			break;
		if signal[i] > 0 and signal[i]>=threshold:
			break;
		R-=1
	if not outPick:
		return signal[L:R]
	return signal[L:R], L

def plot (signal, offset = 0):
	x = [i+offset for i in range (len(signal))]
	plt.plot (x, signal)

# def hangingDraw ():

	
# 	start = time.time()fig = plt.figure()	

# 	canvas = np.zeros((480,640))
# 	screen = pf.screen(canvas, 'Sinusoid')

# 	while True:
# 	    now = time.time() - start

# 	    x = np.linspace(now-2, now, 100)
# 	    y = np.sin(2*np.pi*x) + np.sin(3*np.pi*x)
# 	    plt.xlim(now-2,now+1)
# 	    plt.ylim(-3,3)
# 	    plt.plot(x, y, c='black')

# 	    # If we haven't already shown or saved the plot, then we need to draw the figure first...
# 	    fig.canvas.draw()

# 	    image = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
# 	    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

# 	    screen.update(image)

def myplot ():# plot a signal

	plotEach (importSignal ('anh.wav'))
	plt.show ()	

	pass
def main ():
	#test ()
	#myplot ()
	import sys
	samplePlot ([sys.argv[1]+'%d.wav'%x for x in range (9)])
	pass

if __name__=='__main__':
	main ()