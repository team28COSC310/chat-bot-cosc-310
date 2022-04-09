import os.path
import unittest
import sys

sys.path.append(os.path.join(sys.path[0], '../src'))

from src.translation import get_language, translate_from_en, translate_to_en, translate


class TestTranslation(unittest.TestCase):

    def test_get_language(self):
        word = "bonjour"
        expected_language = "fr"
        actual_language = get_language(word)
        self.assertEqual(expected_language, actual_language)

    def test_translate_from_en(self):
        word = "hello"
        expected_result = "안녕하세요"
        actual_result = translate_from_en(word, dest='ko')
        self.assertEqual(expected_result, actual_result)

    def test_translate_to_english(self):
        word = "cómo estás"
        expected_result = "how are you"
        actual_result = translate_to_en(word)
        self.assertEqual(expected_result, actual_result)

    def test_translate(self):
        word = "do widzenia"
        expected_result = "auf Wiedersehen"
        actual_result = translate(word, src="pl", dest="de")
        self.assertEqual(expected_result, actual_result)


# Run tests by running the python file
if __name__ == '__main__':
    unittest.main()
