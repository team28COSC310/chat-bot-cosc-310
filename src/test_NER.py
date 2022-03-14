"""
This module is used for getting the Named Entity vector array from a raw text
"""
import spacy
#NOTE: run 'python -m spacy download en_core_web_sm' in your terminal after downloading spacy to ensure the program runs
nlp = spacy.load("en_core_web_sm")
#Whether something is recognized as a named entity or not depends on a context.
# This is the list of words which are always recognized as named entities
FIXED_NE=['ubc', 'ubco', 'bc', 'gym', 'library', 'commons', 'eme']
def find_NER(raw_text):
    '''
    Accepts raw (unprocessed, with initial capitalization) text.
    Returns an array of lowercased Named entities found in text as strings
    '''
    processed=nlp(raw_text) #Apply Spacy pretrained model to the text
    # get every named entity (as a lowercased string) from the text
    text_ents = [ne.text.lower() for ne in processed.ents]
    #tokenize and lowercase every word from the text
    token_text=[w.text.lower() for w in processed]
    #make sure the fixed entitites are recognized too
    for word in token_text:
        if word not in text_ents and word in FIXED_NE:
            text_ents.append(word)
    return text_ents