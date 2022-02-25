import unittest
import json
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer


class TestChatModel(unittest.TestCase):
    
    def setUp(self):
        # Setup the so the data can be easily used in the test cases
        pass
    
    def test_model_makes_predictions(self):
        # run predictions on the data to see whether the model trains properly and doesnt break (input output shape, ...)
        pass
    
    def test_model_can_be_saved_and_loaded(self):
        # train and save the model make prediction reload the model_weights and compare the predictions, they should be the same
        pass
    
    

if __name__ == '__main__':
    unittest.main()