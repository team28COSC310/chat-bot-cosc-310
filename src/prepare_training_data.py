"""
This module is used for preparing intents data
"""
import os
import random
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

ignore_letters = ['?', '!', '.', ',']


def build_training_data(intents):
    """
    Build the training data set from the intents file
    """

    words = lemmatize_words(words=intents.words)
    classes = sorted(set(intents.classes))
    documents = intents.documents

    write_to_binary(words, 'pickle/words.pkl')
    write_to_binary(classes, 'pickle/classes.pkl')

    training = encode_word_patterns(words, classes, documents)

    return randomize_training_data(training)


def lemmatize_words(words):
    """
    Lemmzatizes, sorts and removes duplicates from a given word list
    :param words: the list of words
    :return: a sorted set of lemmatized words
    """

    words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
    words = sorted(set(words))

    return words


def encode_word_patterns(words, classes, documents):
    """

    :param words:
    :param classes:
    :param documents:
    :return:
    """
    training = []
    output_empty = [0] * len(classes)

    # encode word patterns
    for document in documents:
        bag = []
        word_patterns = document[0]
        word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
        for word in words:
            bag.append(1) if word in word_patterns else bag.append(0)

        output_row = list(output_empty)
        output_row[classes.index(document[1])] = 1
        training.append([bag, output_row])

    return training


def randomize_training_data(training):
    """

    :param training:
    :return:
    """

    random.shuffle(training)
    training = np.array(training)

    train_x = list(training[:, 0])
    train_y = list(training[:, 1])

    return train_x, train_y


def write_to_binary(info, file_name):
    """
    Writes information to a binary .pkl file
    :param info: data to write
    :param file_name: name of the file to write to
    """
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, 'wb') as file:
        pickle.dump(info, file)
