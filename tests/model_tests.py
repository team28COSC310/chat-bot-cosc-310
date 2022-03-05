import unittest
import json
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer
from prepare_training_data import build_training_data
from data_importer import Intents, load_intents
from response_model import ChatModel


class TestChatModel(unittest.TestCase):

    def setUp(self):
        # Setup the data so it can be easily used in the test cases
        intents = load_intents("./intents_test.json")
        self.train_x, self.train_y = build_training_data(intents)


    def test_model_makes_predictions(self):
        # run predictions on the data to see whether the model trains properly and doesnt break (input output shape, ...)
        chat_model = ChatModel(len(self.train_x[0]), len(self.train_y[0]))
        chat_model.train(self.train_x, self.train_y, './chat_model.h5')

        pred = chat_model.predict(self.train_x[0])
        expected_pred = self.train_y[0]

        self.assertEqual(pred, expected_pred)


    def test_model_can_be_saved_and_loaded(self):
        # train and save the model make prediction reload the model_weights and compare the predictions, they should be the same
        chat_model = ChatModel(len(self.train_x[0]), len(self.train_y[0]))
        chat_model.train(self.train_x, self.train_y, './chat_model.h5')
        chat_model_1 = ChatModel(len(self.train_x[0]), len(self.train_y[0]))
        chat_model_1.load_model_weights('./chat_model.h5')

        pred = chat_model_1.predict(self.train_x[0])
        expected_pred = chat_model.predict(self.train_x[0])

        self.assertEqual(pred, expected_pred)

if __name__ == '__main__':
    unittest.main()