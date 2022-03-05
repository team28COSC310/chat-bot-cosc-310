import os.path
import unittest
import sys
sys.path.append(os.path.join(sys.path[0], '../src'))

import nltk
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('omw-1.4')

from data_importer import load_intents, Intents


class TestDataImporter(unittest.TestCase):

    def test_load_intents_success(self):
        mock_path = "mocks/mock_intents.json"

        result = load_intents(mock_path)

        expected_words = ['pattern1', 'pattern2']
        expected_documents = [(['pattern1'], 'mock'), (['pattern2'], 'mock')]
        expected_classes = ['mock']

        self.assertIsInstance(result, Intents)
        self.assertEqual(result.words, expected_words)
        self.assertEqual(result.documents, expected_documents)
        self.assertEqual(result.classes, expected_classes)

    def test_load_intents_failure(self):
        mock_path = "invalid.json"

        result = load_intents(mock_path)

        self.assertIsInstance(result, Intents)
        self.assertEqual(result.words, [])
        self.assertEqual(result.documents, [])
        self.assertEqual(result.classes, [])


# Run tests by running the python file
if __name__ == '__main__':
    unittest.main()