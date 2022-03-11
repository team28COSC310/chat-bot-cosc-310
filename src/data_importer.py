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
    
    
def load_entities(path):
    """
    Load the entities and return an dict carrying all relevant info
    """
    try:
        with open(path) as file:
            entities = json.loads(file.read())

            ents = {}

            for e in entities['entities']:
                ents[e['entity']] = {'opening hours':e['opening hours'],
                                     'location':e['location'],
                                     'contact':e['contact'],
                                     'link':e['link']
                                    }
        return ents      

    except FileNotFoundError:
        print("Entities file not found.")
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
