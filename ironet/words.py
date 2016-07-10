"""
Word Types (Grounds and Vehicles)
"""
from nltk.corpus import wordnet as wn


def find_synonyms(word, wn_type):
    """
    finds all synonyms and similar words to a given word
    """
    synonyms = []

    def append_to_array(lemmas):
        for lemma in lemmas:
            for name in lemma.lemma_names():
                name = name.encode("utf-8")
                if name not in synonyms:
                    synonyms.append(name)

    # get direct synonyms
    for syns in wn.synsets(word, wn_type):

        for lemma in syns.lemmas():
            name = lemma.name().encode("utf-8")
            if name not in synonyms:
                synonyms.append(name)

        append_to_array(syns.hyponyms())
        append_to_array(syns.similar_tos())
    return synonyms


def find_antonyms(word):
    """
    finds the antonyms to a given adjective
    :param word: adjective
    :return: list of antonyms
    """
    antonyms = []
    for syn in wn.synsets(word, wn.ADJ):
        for lemma in syn.lemmas():
            for antonym in lemma.antonyms():
                if antonym.name().encode("utf-8") not in antonyms:
                    antonyms.append(antonym.name().encode("utf-8"))
    return antonyms


class Word:
    """
    Base class for words
    """
    def __init__(self, name, word_type):
        self.name = name
        self.synonyms = [self.name]

        self.wordType = word_type

        self.get_synonyms()

    def get_synonyms(self):
        self.synonyms += find_synonyms(self.name, self.wordType)


class Ground(Word):
    def __init__(self, name):
        Word.__init__(self, name, wn.ADJ)
        self.codescriptors = []
        self.antonyms = []

        self.get_antonyms()

    def add_codescriptor(self, codescriptor):
        self.codescriptors.append(codescriptor)

    def get_antonyms(self):
        self.antonyms = find_antonyms(self.name)


class Vehicle(Word):
    def __init__(self, name):
        Word.__init__(self, name, wn.NOUN)
        self.attributes = []
        self.loaded = False

    def add_attribute(self, attribute):
        self.attributes.append(attribute)

    def has_attribute(self, attribute):
        if type(attribute) == 'instance':
            attribute = attribute.name

        return attribute in self.attributes
