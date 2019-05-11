import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, LSTM
from keras import backend as K

def createModel (shape):
	classifier = Sequential()

	# classifier.add(Dense(output_dim=64, init='uniform', activation='relu', input_dim=10))
	# classifier.add(Dense(output_dim=32, init='uniform', activation='relu'))
	# classifier.add(Dense(output_dim=1, init='uniform', activation='sigmoid'))

	# classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

	classifier.add(LSTM(44, input_shape=shape, return_sequences = True))
	classifier.add(Dropout (0.2))
	classifier.add(LSTM(22, input_shape=shape, return_sequences = False))
	classifier.add(Dropout (0.1))
	classifier.add(Dense(1, activation = 'sigmoid'))
	classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
	return classifier

def loadWav():
	x = [i+offset for i in range (len(signal))]
	pass

def __1st_exp (shape):
	file = pd.read_csv ('sample.csv', delimiter=',')
	# print (file)
	
	from sklearn.model_selection import train_test_split as tts
	X_train, X_test, Y_train, Y_test = tts (file.iloc[:,0:10], file.iloc[:,10], test_size = 1/3.0)
	X_train = X_train.values.reshape (len(X_train), 10, 1)
	X_test = X_test.values.reshape (len(X_test), 10, 1)
	# print (X_train)
	# print (Y_train.shape)
	
	# return;
	# print (K.tensorflow_backend._get_available_gpus())
	classifier = createModel (shape)
	history = classifier.fit (X_train, Y_train, batch_size=10, nb_epoch=200,verbose=0)
	print(classifier.summary())
	# print (X_test)
	Y_pred = classifier.predict(X_test, batch_size = 1)

	print (Y_pred)
	print (Y_pred>0.5)
	print ('Y_test:',list(Y_test))

def main ():

	'''
		Pattern recognization:
		-- First problem: Hard to judge that is really the same with perceptron
		-- Really, dude?
	'''
	
	__1st_exp ((10, 1))
	# from keras.utils import plot_model

	# from ann_visualizer.visualize import ann_viz
	# ann_viz(classifier, title="My first neural network", filename='e:\\python\\network.gr')

	# import matplotlib.pyplot as plt
		# plot_model(classifier, to_file='model.png')

	# Plot training & validation accuracy values
	# plt.plot(history.history['acc'])
	# # plt.plot(history.history['val_acc'])
	# plt.title('Model accuracy')
	# plt.ylabel('Accuracy')
	# plt.xlabel('Epoch')
	# plt.legend(['Train', 'Test'], loc='upper left')
	# plt.show()

	# # Plot training & validation loss values
	# plt.plot(history.history['loss'])
	# plt.plot(history.history['val_loss'])
	# plt.title('Model loss')
	# plt.ylabel('Loss')
	# plt.xlabel('Epoch')
	# plt.legend(['Train', 'Test'], loc='upper left')
	# plt.show()
	# import matplotlib.image as mimg
	# img = mimg.imread ('model.png')
	# import matplotlib.pyplot as plt
	# plt.imshow (img)
	# plt.show ()
	# Y_pred = (Y_pred > 0.5)
	# Making the Confusion Matrix
	# from sklearn.metrics import confusion_matrix
	# cm = confusion_matrix(Y_test, Y_pred)
	# print(cm)

if __name__=='__main__':
	main ()