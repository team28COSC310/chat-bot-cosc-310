import numpy  
import random 
import pickle

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

class ChatModel:
    '''
    Create a model, to train it and make prediction for input sentence vectors
    '''
    
    def __init__(self, input_size, output_size):
        '''
        build and setup the model structure and return compile model
        '''
        self.input_shape = input_size
        self.model = Sequential()
        self.model.add(Dense(128, input_shape=(input_size,), activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(64, activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(output_size, activation='softmax'))

        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        self.model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    
    def train(self, train_x, train_y, save_path):
        '''
        train the model on a given data set (given as list of lists)
        '''
        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        self.model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
        self.model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
        self.model.save_weights(save_path)
    
    def load_model_weights(self, path):
        '''
        load model weights, stored under given path
        '''
        self.model.load_weights(path)
    
    def predict(self, input):
        '''predict the class for the given input (given as a list)'''
        input = np.array(input)
        input = np.reshape(input, (1, self.input_shape))
        prediction = self.model.predict(input)
        return np.argmax(prediction)    
