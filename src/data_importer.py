import json

import nltk
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer


def load_intents(path: str):
    try:
        file = open(path)
        intents = json.loads(file.read())
        file.close()

        words = []
        classes = []
        documents = []

        for intent in intents['intents']:
            for pattern in intent['patterns']:
                word_list = nltk.word_tokenize(pattern)
                words.append(word_list)
                documents.append((word_list, intent['tag']))
                if intent['tag'] not in classes:
                    classes.append(intent['tag'])

        return Intents(words, classes, documents)

    except FileNotFoundError:
        print("Intents file not found.")
        return Intents([], [], [])


class Intents:

    words: []
    classes: []
    documents: []

    def __init__(self, words: [], classes: [], documents: []):
        self.words = words
        self.classes = classes
        self.documents = documents
