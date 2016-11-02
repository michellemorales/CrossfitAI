#Michelle Morales
#Text Generation With LSTM Recurrent Neural Networks in Python with Keras
#http://machinelearningmastery.com/text-generation-lstm-recurrent-neural-networks-python-keras/
#Train LSTM using CFGC wod data

import sys, os, os.path, nltk
import numpy
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
			cfgc_data.append(line.strip().lower())

# create mapping of unique chars to integers, and a reverse mapping
raw_text = ' '.join(cfgc_data)
chars = sorted(list(set(raw_text)))
char_to_int = dict((c, i) for i, c in enumerate(chars))
int_to_char = dict((i, c) for i, c in enumerate(chars))

# summarize the loaded data
n_chars = len(raw_text)
n_vocab = len(chars)

print "Total Characters: ", n_chars
print "Total Vocab: ", n_vocab

# prepare the dataset of input to output pairs encoded as integers
seq_length = 100
dataX = []
dataY = []
for i in range(0, n_chars - seq_length, 1):
	seq_in = raw_text[i:i + seq_length]
	seq_out = raw_text[i + seq_length]
	dataX.append([char_to_int[char] for char in seq_in])
	dataY.append(char_to_int[seq_out])
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
filepath="log/weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]
# fit the model
model.fit(X, y, nb_epoch=20, batch_size=128, callbacks=callbacks_list)
