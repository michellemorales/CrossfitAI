#Michelle Morales
#Text Generation With LSTM Recurrent Neural Networks in Python with Keras
#http://machinelearningmastery.com/text-generation-lstm-recurrent-neural-networks-python-keras/
#Train LSTM using CFGC wod data

import sys, os, os.path
import numpy
from nltk import word_tokenize
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils

# load ascii text and covert to lowercase
directory = "CFGC_data"
cfgc_data = []
for filename in os.listdir(directory):
	with open(os.path.join(directory,filename),'r') as f:
		for line in f.readlines()[1:]:
			tokens = word_tokenize(line.strip().lower())
			for t in tokens:
				cfgc_data.append(t)	

# create mapping of unique chars to integers, and a reverse mapping
words = sorted(list(set(cfgc_data)))
word_to_int = dict((w, i) for i, w in enumerate(words))
int_to_word = dict((i, w) for i, w in enumerate(words))

# summarize the loaded data
n_words = len(cfgc_data)
n_vocab = len(words)

print "Total Words: ", n_words
print "Total Vocab: ", n_vocab

# prepare the dataset of input to output pairs encoded as integers
seq_length = 10
dataX = []
dataY = []
for i in range(0, n_words - seq_length, 1):
	seq_in = cfgc_data[i:i + seq_length]
	seq_out = cfgc_data[i + seq_length]
	dataX.append([word_to_int[w] for w in seq_in])
	dataY.append(word_to_int[seq_out])
n_patterns = len(dataX)
print "Total Patterns: ", n_patterns
# reshape X to be [samples, time steps, features]
X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
print 'Reshape Done'
# normalize
X = X / float(n_vocab)
print 'Normalize Done'
# one hot encode the output variable
y = np_utils.to_categorical(dataY)
print 'One Hot Done'
# define the LSTM model
# define the LSTM model
model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2])))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')
# define the checkpoint
filepath="logW/weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]
# fit the model
model.fit(X, y, nb_epoch=20, batch_size=128, callbacks=callbacks_list)
