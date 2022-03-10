"""
This module is responsible for training
and utilizing the Neural Network model
"""
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD


class ChatModel:
    """
    Create a model, to train it and make prediction for input sentence vectors
    """

    def __init__(self, input_size, output_size):
        """
        build and setup the model structure and return compile model
        """
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
        """
        train the model on a given data set (given as list of lists)
        """
        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        self.model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
        self.model.fit(np.array(train_x), np.array(train_y), epochs=500, batch_size=5, verbose=1)

        # Note:
        # I could not run the chatbot while saving weights here,
        # so I changed save_weights to save.
        # Feel free to change it back if you know how to fix the chatbot issue.
        # self.model.save_weights(save_path)
        self.model.save(save_path)

    def load_model_weights(self, path):
        """
        load model weights, stored under given path
        """
        self.model.load_weights(path)

    def predict(self, input_array):
        """
        predict the class for the given input (given as a list)
        """
        input_array = np.array(input_array)
        input_array = np.reshape(input_array, (1, self.input_shape))
        prediction = self.model.predict(input_array)
        return prediction
