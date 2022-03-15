"""
COSC 310 Chat Bot

Created by:
Nicholas Brown, Jonathan Chou, Omar Ishtaiwi, Niklas Tecklenburg and Elizaveta Zhukova
"""

from email import message_from_binary_file
import random
import json
import pickle
import nltk
from nltk.stem import WordNetLemmatizer

from response_model import ChatModel
from prepare_training_data import build_training_data
from data_importer import load_intents, load_entities

from NER_func import find_NER
from data_importer import load_intents
from spellchecker import SpellChecker


#5 versions of apologies in case the bot cannot identify user's request and therefore cannot reply
APOLOGIES=["Sorry, I do not understand you. Please, try rephrasing the question using synonyms or simpler words",
           "Sorry, I cannot seem to comprehend what you are saying. Try asking me about the dining places, or the weather",
           "My apologies, I do not understand your question. Try asking me about the sport events at campus or UBCO history",
           "I apologize for the incovenience, but I do not understand you. \nPlease, try rephrasing your request. \nFor example instead of asking 'Where can I get some food on campus?' ask 'I am hungry, where do I go?'",
           "I am very sorry but I do not understand you. \nCheck out UBCO FAQ, you might find an answer to your question there: https://students.ok.ubc.ca/academic-success/academic-advising/frequently-asked-questions/"]

class Chat:
    """
    Chatbot
    """

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

        self.intents = load_intents("../intents.json")
        self.spellchecker = SpellChecker()
        self.train_x, self.train_y = build_training_data(self.intents)
        
        self.entity_infos = load_entities('../entity_infos.json')

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

        # print("Entered:", sentence)
        sentence = self.spellchecker.autocorrect(sentence)
        # print("Interpreted:", sentence)

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

    def get_response(self, intents_list, intents_json, ents):
        '''
        Generate a response of the bot, given the probable intents of a users and the list of all intents
        '''
        if not intents_list:
            return random.choice(APOLOGIES)
        tag = intents_list[0]['intent']
        
        
        if tag in ["opening hours", "more information", "location info", "contact info"]:
            ent_matches = []
            for ent in ents:
                if ent in self.entity_infos.keys():
                    ent_matches.append(ent)
            if len(ent_matches)>0:
                entity = random.choice(ent_matches)
            else:
                entity = []
                
            if tag == "opening hours":
                if entity ==[]:
                    result = f"I am really sorry but I do not have infos on the opening hours for the {random.choice(ents)}"
                else:
                    info = self.entity_infos[entity]["opening hours"]
                    result = f"The opening hours for the {entity} are {info}."
            elif tag =="more information":
                if entity ==[]:
                    result = f"I am really sorry but I do not have further infos on the {random.choice(ents)}"
                else:
                    info = self.entity_infos[entity]["link"]
                    result = f"You can find more infos on the {entity} here: {info}"
            elif tag == "location info":
                if entity ==[]:
                    result = f"I am really sorry but I do not have location infos for the {random.choice(ents)}"
                else:
                    info = self.entity_infos[entity]["location"]
                    result = f"The {entity} is located here: {info}"
            elif tag =="contact info":
                if entity ==[]:
                    result = f"I am really sorry but I do not have contact infos {random.choice(ents)}"
                else:
                    info = self.entity_infos[entity]["contact"]
                    result = f"You can reach out to the {entity} here: {info}"
        else:
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
        ents = find_NER(message)
        # add nouns found in the sentence
        # nouns = findNN(message)
        # ents.extend(nouns)
        res = chat.get_response(ints, intents, ents)
        print(res)
