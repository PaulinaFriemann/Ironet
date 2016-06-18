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


class Ground:
    def __init__(self, name):
        self.name = name
        self.codescriptors = []
        self.synonyms = []
        self.antonyms = []

    def add_codescriptor(self, codescriptor):
        self.codescriptors.append(codescriptor)

    def get_synonyms(self):
        self.synonyms = find_synonyms(self.name, wn.ADJ)

    def get_antonyms(self):
        self.antonyms = find_antonyms(self.name)


class Vehicle:
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.synonyms = []

    def add_attribute(self, attribute):
        self.attributes.append(attribute)

    def get_synonyms(self):
        self.synonyms = find_synonyms(self.name, wn.NOUN)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class WordDatabase:
    __metaclass__ = Singleton

    def __init__(self):
        self.grounds = dict()
        self.vehicles = dict()

    def add_ground(self, ground):
        self.grounds[ground] = Ground(ground)

    def add_vehicle(self, vehicle):
        self.vehicles[vehicle] = Vehicle(vehicle)

    def get_ground(self, name):
        return self.grounds[name]

    def get_vehicle(self, name):
        return self.vehicles[name]

    def load(self):
        self.grounds = self.load_grounds()
        self.vehicles = self.load_vehicles()

    def load_grounds(self):
        # TODO
        pass

    def load_vehicles(self):
        # TODO
        pass
