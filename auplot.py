import pyaudio
import numpy as np

CHUNK = 2**10
RATE = 44100

p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK)

#f=open('auplot.txt','w')
for i in range(30*RATE//CHUNK): #go for a few seconds
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    peak=np.average(np.abs(data))*2
    bars='*'*int(50*peak//2**12)
    print("%05d %s"%(peak,bars))
    #f.write ("%05d %s\n"%(peak,bars))
#f.close ()
stream.stop_stream()
stream.close()
p.terminate()