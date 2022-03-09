import os
from pathlib import Path
from symspellpy import SymSpell, Verbosity


class SpellChecker:
    _spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)

    def __init__(self):
        dictionary_path = os.path.join(
            Path(os.path.dirname(os.path.abspath(__file__))).parent, "assets", "big.txt"
        )

        self._spell.create_dictionary(dictionary_path, encoding="utf8")

    def segment_string(self, input_term):
        return self._spell.word_segmentation(input_term).corrected_string

    def suggestions(self, input_term):
        return self._spell.lookup(input_term, Verbosity.ALL)


if __name__ == '__main__':
    s = SpellChecker()

    print(s.segment_string("thequickbrownfoxjumpsoverthelazydog"))
    for suggestion in s.suggestions("memebers"):
        print(suggestion.term)
