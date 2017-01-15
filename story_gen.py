import sys
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils

def story_gen(message_in=""):
	# load ascii text and covert to lowercase
	filename = "wonderland.txt"
	raw_text = open(filename).read()
	raw_text = raw_text.lower()
	
	# create mapping of unique chars to integers, and a reverse mapping
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
	
	# normalize
	X = X / float(n_vocab)
	# one hot encode the output variable
	y = np_utils.to_categorical(dataY)

	# define the LSTM model model = Sequential()
	model = Sequential()
	model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
	model.add(LSTM(256))
	model.add(Dense(y.shape[1], activation='softmax'))

	# load the network weights
	filename = "weights-improvement-20-1.2619.hdf5"
	model.load_weights(filename)
	model.compile(loss='categorical_crossentropy', optimizer='adam')

	# pick a random seed
	start = numpy.random.randint(0, len(dataX)-1)
	pattern = dataX[start]
	# pattern.append(message_in)

        return pattern, model, int_to_char, n_vocab, n_chars 

        
	


        
def get_sequence(pattern, model,int_to_char, n_vocab, n_chars):
    results = []
    # generate 
    for i in range(100):
	x = numpy.reshape(pattern, (1, len(pattern), 1))
	x = numpy.divide(x, n_vocab * 1.0)
	prediction = model.predict(x, verbose=0)
	index = numpy.argmax(prediction)
	result = int_to_char[index]
	seq_in = [int_to_char[value] for value in pattern]
	results.append(result)
	pattern.append(index)
	pattern = pattern[1:len(pattern)]

    return pattern, results

if __name__ == '__main__':
    pattern, model, int_to_char, n_vocab, n_chars= story_gen()
    print "Starting...\n\n"
    for i in range(7):
        pattern , result = get_sequence(pattern, model, int_to_char, n_vocab, n_chars)
        print "".join(result)
	# print "".join(story_gen("hello"))
