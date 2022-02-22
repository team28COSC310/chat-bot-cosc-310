"""
This module is used for loading and preparing intents data
"""
import json

import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()


def load_intents(path):
    """
    Loads a specified intents JSON file
    :param path: Path to the intents file
    :return: An Intents object
    """
    try:
        with open(path) as file:
            intents = json.loads(file.read())

            words = []
            classes = []
            documents = []

            for intent in intents['intents']:
                for pattern in intent['patterns']:
                    word_list = nltk.word_tokenize(pattern)
                    words.extend(word_list)
                    documents.append((word_list, intent['tag']))
                    if intent['tag'] not in classes:
                        classes.append(intent['tag'])

            return Intents(words, classes, documents)

    except FileNotFoundError:
        print("Intents file not found.")
        return Intents([], [], [])


class Intents:
    """
    A class containing the words, classes and documents information
    loaded from an Intents JSON file.
    """
    def __init__(self, words, classes, documents):
        self.words = words
        self.classes = classes
        self.documents = documents
        
  
#------------
      
import random 
import pickle
import numpy as np

ignore_letters = ['?', '!', '.', ',']

intents = load_intents("./intents_test.json")
words = intents.words
classes = intents.classes
documents = intents.documents

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

classes = sorted(set(classes))

training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])
    
random.shuffle(training)
training = np.array(training)

train_x = list(training[:, 0])
train_y = list(training[:, 1])


#------
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD



model = Sequential()
