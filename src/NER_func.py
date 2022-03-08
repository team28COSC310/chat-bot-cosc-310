"""
This module is used for getting the Named Entity vector array from a raw text
"""
import spacy
#NOTE: run 'python -m spacy download en_core_web_sm' in your terminal after downloading spacy to ensure the program runs
nlp = spacy.load("en_core_web_sm")
#Whether something is recognized as a named entity or not depends on a context.
# This is the list of words which are always recognized as named entities
FIXED_NE=['ubc', 'ubco', 'bc']
def NER_vector_from_raw(raw_text):
    '''
    Accepts raw (unprocessed, with initial capitalization) text and returns 2 elements.
    The first element of the tuple is the array of tokenized and lowercased raw_text words.
    The second element of the tuple is the array of numbers 0 and 1, used as a vector for the given raw text.
    0 means the corresponding word in the first tuple is not a (part of) Named Entity.
    1 means the corresponding word in the first tuple is a (part of) Named Entity.
    '''
    processed=nlp(raw_text) #Apply Spacy pretrained model to the text
    # get every word (and lowercase it) from text which is a part of named entity
    # (some named entities are compound, for example 'British Columbia')
    text_ents = [[pe.text.lower() for pe in ne] for ne in processed.ents]
    #tokenize and lowercase every word from the text
    token_text=[w.text.lower() for w in processed]
    #make sure the fixed entitites are recognized too
    text_ents.append([word for word in token_text if word in FIXED_NE])
    #flatten the array
    text_ents=[fe for sub in text_ents for fe in sub]
    final_vector=[]
    for token in token_text:
        if token in text_ents:
            final_vector.append(1)
        else:
            final_vector.append(0)
    return token_text, final_vector
