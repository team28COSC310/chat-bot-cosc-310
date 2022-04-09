from googletrans import Translator

t = Translator()


def get_language(sentence):
    """
    Returns the language of the provided sentence
    """
    return t.translate(sentence).src


def translate_to_en(sentence):
    """
    Returns the given sentence translated to english
    """
    return translate(sentence, src=get_language(sentence), dest='en')


def translate_from_en(sentence, dest):
    """
    Translates a given sentence from English
    to the specified destination language
    """
    return translate(sentence, src='en', dest=dest)


def translate(sentence, src, dest):
    """
    Translates a given sentence from the specified source language
    to the specified destination language
    """
    return t.translate(sentence, src=src, dest=dest).text


if __name__ == '__main__':
    print(get_language("인사말"))
