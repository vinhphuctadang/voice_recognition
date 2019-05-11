from gtts import gTTS

def convert (src, dst):
	from pydub import AudioSegment
	# convert wav to mp3                                                            
	sound = AudioSegment.from_mp3(src)
	sound.export(dst, format="wav")

def main ():

	obj = gTTS (text='Xin', lang='vi', slow=False)
	obj.save ('sample.mp3')

	# convert ('sample.mp3', 'sample.wav')
main ()