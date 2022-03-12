import os
from pathlib import Path
from symspellpy import SymSpell, Verbosity

MAX_EDIT_DISTANCE = 3
DICTIONARY_PATH = os.path.join(Path(os.path.dirname(os.path.abspath(__file__))).parent, "assets", "big.txt")


class SpellChecker:
    _spell = SymSpell(max_dictionary_edit_distance=MAX_EDIT_DISTANCE, prefix_length=7)

    def __init__(self):
        self._spell.create_dictionary(DICTIONARY_PATH, encoding="utf8")

    def segment_string(self, input_sentence: str):
        return "".join([
            self._spell.word_segmentation(term, max_edit_distance=1).corrected_string + " "
            for term in
            input_sentence.split()
        ])

    def suggestions(self, input_term: str):
        suggestions = self._spell.lookup(input_term, Verbosity.TOP, max_edit_distance=2)
        if len(suggestions) > 0:
            return suggestions[0].term
        else:
            return input_term

    def autocorrect(self, input_sentence):
        terms = self.segment_string(input_sentence).split()
        return "".join([
            self.suggestions(term) + " "
            for term in terms
        ])

# Check list of recognized words for recognized words contained in the input sentence
# extract recognized words
