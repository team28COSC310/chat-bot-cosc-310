import sys
import os

sys.path.append(os.path.abspath('../src'))

import unittest
import json

from chatbot import Chat
from data_importer import load_entities
from NER_func import find_NER


class TestChatModel(unittest.TestCase):
    def setUp(self):
        self.chat = Chat()
        with(open("../intents.json")) as intents_file:
            self.intents = json.loads(intents_file.read())
        self.entity_infos = load_entities('../entity_infos.json')

    def test_predict_class_returns_correct_intent(self):
        sentence = "hello"
        pred = self.chat.predict_class(sentence)[0]['intent']
        expected_pred = 'greetings'

        self.assertEqual(pred, expected_pred)

    def test_get_response_return_proper_message(self):
        sentence = "hello"
        pred = self.chat.predict_class(sentence)
        resp = self.chat.get_response(pred, self.intents, [], sentence)

        expected_resp = ["Hello, I am the UBCO Chatbot",
                         "Hi, how can I help you today?",
                         "Hello from UBCO, how can I help you?"]

        self.assertTrue(resp in expected_resp)

    def test_get_response_can_deal_with_entity_file(self):
        sentence = "Where is the gym open?"
        pred = self.chat.predict_class(sentence)
        ents = find_NER(sentence)
        resp = self.chat.get_response(pred, self.intents, ents, sentence)

        expected_resp = "The gym is located here: 3211 Athletics Court"

        self.assertEquals(resp, expected_resp)

    def test_get_response_can_deal_with_unknown_entity(self):
        sentence = "Where is the Wembley Stadium?"
        pred = self.chat.predict_class(sentence)
        ents = find_NER(sentence)
        resp = self.chat.get_response(pred, self.intents, ents, sentence)

        expected_resp = "I am really sorry but I do not have location infos for it."

        self.assertEquals(resp, expected_resp)


if __name__ == '__main__':
    unittest.main()
