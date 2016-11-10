#Michelle Morales
#Generate WOD

# Load LSTM network and generate text
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
words_to_int = dict((w, i) for i, w in enumerate(words))
int_to_words = dict((i, w) for i, w in enumerate(words))

# summarize the loaded data
n_words = len(cfgc_data)
n_vocab = len(words)


# prepare the dataset of input to output pairs encoded as integers
seq_length = 10
dataX = []
dataY = []
for i in range(0, n_words - seq_length, 1):
	seq_in = cfgc_data[i:i + seq_length]
	seq_out = cfgc_data[i + seq_length]
	dataX.append([words_to_int[w] for w in seq_in])
	dataY.append(words_to_int[seq_out])
n_patterns = len(dataX)
print "Coach is being trained..."
# reshape X to be [samples, time steps, features]
X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
# normalize
X = X / float(n_vocab)
# one hot encode the output variable
y = np_utils.to_categorical(dataY)
# define the LSTM model
model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2])))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))
# load the network weights
filename = "logW/weights-improvement-19-3.7380.hdf5"
model.load_weights(filename)
model.compile(loss='categorical_crossentropy', optimizer='adam')
# pick a random seed
start = numpy.random.randint(0, len(dataX)-1)
pattern = dataX[start]
print "Seed:"
print "\"", ' '.join([int_to_words[value] for value in pattern]), "\""
# generate wod
for i in range(20):
	x = numpy.reshape(pattern, (1, len(pattern), 1))
	x = x / float(n_vocab)
	prediction = model.predict(x, verbose=0)
	index = numpy.argmax(prediction)
	result = int_to_words[index]
	seq_in = [int_to_words[value] for value in pattern]
	sys.stdout.write(result+' ')
	pattern.append(index)
	pattern = pattern[1:len(pattern)]
print "\nLet's go!"
