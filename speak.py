import pyttsx3 
import sys

engine = pyttsx3.init()   
if len(sys.argv) > 1:
	engine.say(sys.argv[1]) 
engine.runAndWait() 