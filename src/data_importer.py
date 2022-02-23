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
