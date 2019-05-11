import sys
import os
import fnmatch
from recorder import play

def matchPattern (file, pattern=[]):
	for fPat in pattern:
		if fnmatch.fnmatch (file, fPat):
			return True
	return False

def listFile (walk=os.walk ('.'), pattern=['*.wav']):
	root, dirs, files = next (walk)
	result = []
	for file in files:
		if (matchPattern (file, pattern)):
			result.append (file)
	return result

def main ():

	if len(sys.argv) < 2:
		print ('No file played')
		return
		
	pattern = sys.argv[1]
	files = listFile (pattern=[pattern])
	# print (files)
	for file in files:
		print ('Playing "%s" ... '%file)
		play (file)
		
if __name__=='__main__':
	main ()


