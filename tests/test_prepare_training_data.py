import os.path
import unittest
import sys

sys.path.append(os.path.join(sys.path[0], '../src'))

import nltk
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('omw-1.4')

from prepare_training_data import lemmatize_words, encode_word_patterns


class TestPrepareTrainingData(unittest.TestCase):

    def test_lemmatize_words(self):
        words = lemmatize_words(['cars', 'pickles', 'abaci', 'car', 'abacus'])
        expected_words = ['abacus', 'car', 'pickle']

        self.assertEqual(words, expected_words)

    def test_encode_word_patterns(self):
        words = ['pattern1', 'pattern2', 'pattern3']
        classes = ['mock', 'mock2', 'mock3']
        documents = [(['pattern1'], 'mock'), (['pattern2'], 'mock'), (['pattern3'], 'mock2')]

        # pattern1, mock
        list1 = [[1, 0, 0], [1, 0, 0]]
        # pattern2, mock
        list2 = [[0, 1, 0], [1, 0, 0]]
        # pattern3, mock2
        list3 = [[0, 0, 1], [0, 1, 0]]

        result = encode_word_patterns(words, classes, documents)

        self.assertEqual(result[0], list1)
        self.assertEqual(result[1], list2)
        self.assertEqual(result[2], list3)


# Run tests by running the python file
if __name__ == '__main__':
    unittest.main()
