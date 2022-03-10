"""
COSC 310 Chat Bot

Created by:
Nicholas Brown, Jonathan Chou, Omar Ishtaiwi, Niklas Tecklenburg and Elizaveta Zhukova
"""

import random
import json
import pickle
import nltk
from nltk.stem import WordNetLemmatizer

from response_model import ChatModel
from prepare_training_data import build_training_data
from data_importer import load_intents


class Chat:
    """
    Chatbot
    """
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

        self.intents = load_intents("../intents.json")
        self.train_x, self.train_y = build_training_data(self.intents)

        self.chat_model = ChatModel(len(self.train_x[0]), len(self.train_y[0]))

        with(open("pickle/words.pkl", "rb")) as word_file:
            self.words = pickle.load(word_file)

        with(open("pickle/classes.pkl", "rb")) as class_file:
            self.classes = pickle.load(class_file)

        # Load the Chatbot model, if there are no weights available, train the model
        try:
            self.chat_model.load_model_weights('./model_weights/weights.h5')
        except FileNotFoundError:
            self.chat_model.train(self.train_x, self.train_y, './model_weights/weights.h5')

    def preprocess_sentence(self, sentence):
        '''
        Tokenize the sentence entered by user into words, delete punctuation signs and lemmatize
        '''
        ignore_letters = ['?', '!', '.', ',']
        sent_words = nltk.word_tokenize(sentence)
        sent_words = [self.lemmatizer.lemmatize(word) for word in sent_words if word not in ignore_letters]
        return sent_words

    def bag_words(self, sentence):
        '''
        Create the bag of words representation of a sentence.
        That is, identify which words from our intents file are present in the users' sentence
        '''
        sent_words = self.preprocess_sentence(sentence)
        bag = [0] * len(self.words)
        for sw in sent_words:
            for i, word in enumerate(self.words):
                if word == sw:
                    bag[i] = 1
        return bag

    def predict_class(self, sentence):
        '''
        Predict the class (intent) of a users' sentence
        '''
        bow = self.bag_words(sentence)
        res = self.chat_model.predict(bow)[0]
        err_border = 0.3
        results = [[i, r] for i, r in enumerate(res) if r > err_border]
        # Sort by probability in reverse order
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({'intent': self.classes[r[0]], 'probability': str(r[1])})
        return return_list

    def get_response(self, intents_list, intents_json):
        '''
        Generate a response of the bot, given the probable intents of a users and the list of all intents
        '''
        if not intents_list:
            return "Sorry, I do not understand you. Please, try rephrasing the question"
        tag = intents_list[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break
        return result



if __name__ == '__main__':
    chat = Chat()
    with(open("../intents.json")) as intents_file:
        intents = json.loads(intents_file.read())
    print("You can start talking to the bot now. If you want to stop the bot, type `stop`")
    while True:
        message = input("")
        if message.lower() == 'stop':
            break
        ints = chat.predict_class(message)
        res = chat.get_response(ints, intents)
        print(res)
