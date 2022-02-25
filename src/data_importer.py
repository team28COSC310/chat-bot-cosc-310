"""
This module is used for loading and preparing intents data
"""
import json

import nltk
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()


def load_intents(path: str):
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
                        
            words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
            words = sorted(set(words))

            classes = sorted(set(classes))



            training = []
            output_empty = [0] * len(classes)

            for doc in documents:
                 bag = []
                 word_patterns = doc[0]
                 word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
                 for word in words:
                     bag.append(1) if word in word_patterns else bag.append(0)

                 output_row = list(output_empty)
                 output_row[classes.index(doc[1])] = 1
                 training.append([bag, output_row])

             random.shuffle(training)
             training = np.array(training)
                        
              

            return Intents(words, classes, documents)

    except FileNotFoundError:
        print("Intents file not found.")
        return Intents([], [], [])


class Intents:
    """
    A class containing the words, classes and documents information
    loaded from an Intents JSON file.
    """

    words: []
    classes: []
    documents: []

    def __init__(self, words: [], classes: [], documents: []):
        self.words = words
        self.classes = classes
        self.documents = documents
