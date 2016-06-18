import os
import pickle

from nltk.corpus import wordnet as wn
from requests.exceptions import ProxyError, ConnectionError

import utils.query_utils as query_utils
import utils.text_utils as text_utils


def get_all_inverses(data):
    inverses = []
    with open('../res/inverses.txt', 'w') as f:

        for simile in data.similes:
            inverse = get_inverse(simile)
            if inverse is not None:
                inverse.frequency, inverse.about_frequency = get_inverse_frequ(inverse, data.similes)
                inverses.append(inverse)

    text_utils.dump(inverses, '../res/pdata/inverses.txt')
    data.save_data()


def get_inverse(simile):
    if simile.antonyms != []:
        antonym = simile.antonyms[0]

        new_simile = Simile(antonym, simile.vehicle)
        return new_simile
    else:
        return None


def get_inverse_frequ(inverse, similes):
    for simile in similes:

        if simile.name == inverse.name:
            inverse.frequency = simile.frequency
            inverse.about_frequency = simile.about_frequency

    if inverse.frequency == 0 or inverse.frequency == "0":
        f = open('../res/pdata/invwfrequ.txt', 'r')
        done = pickle.load(f)
        f.close()
        for simile in done:
            if inverse.name == simile.name:
                inverse.frequency = simile.frequency
                inverse.about_frequency = simile.about_frequency

    return inverse.frequency, inverse.about_frequency


def get_inverse_frequency(data):

    with open('../res/inversefrequsINWORK.txt', 'a+') as f:
        lines = 0
        for line in f:
            lines += 1

        print lines

        trytoinit = True
        num = 0
        for simile in data.similes:
            for inverse in simile.inverses:
                if num < lines:
                    num += 1
                    continue

                try:
                    inverse.initialise()
                except ProxyError:
                    data.save_data()
                    raise SystemExit
                except ConnectionError:
                    data.save_data()
                    raise SystemExit
                except:
                    data.save_data()
                    raise SystemExit
                print "write " + inverse.name + ";" + str(inverse.frequency) + " " + str(inverse.about_frequency) + "\n"
                f.write(inverse.name + ";" + str(inverse.frequency) + " " + str(inverse.about_frequency) + "\n")
            f.write("\n")


def get_synonyms(word, array, wn_type):
    def append_to_array(lemmas):
        for lemma in lemmas:
            for name in lemma.lemma_names():
                name = name.encode("utf-8")
                if name not in array:
                    array.append(name)

    # get direct synonyms
    for syns in wn.synsets(word, wn_type):

        for lemma in syns.lemmas():
            name = lemma.name().encode("utf-8")
            if name not in array:
                array.append(name)

        append_to_array(syns.hyponyms())
        append_to_array(syns.similar_tos())


class Simile:

    def __init__(self, ground, vehicle, irony=False, frequency=0, about_frequency=0):

        self.ground = ground
        self.vehicle = vehicle
        self.ironic = (irony == 'i')
        self.frequency = frequency
        self.about_frequency = about_frequency

        self.an = "an " if (self.vehicle[0] in ['a', 'e', 'i', 'o', 'u']) else "a "

        self.ground_synonyms = [self.ground]
        self.vehicle_synonyms = [self.vehicle]
        self.antonyms = []
        self.inverse = None

        self.such_as = False

        self.name = "as " + self.ground + " as " + self.an + self.vehicle

    @classmethod
    def from_phrase(cls, phrase):
        words = phrase.split(" ")
        adjective, vehicle, irony = words[1], words[4], words[5].rstrip('\n')
        return cls(adjective, vehicle, irony)

    @classmethod
    def from_line(cls, line):
        line = line.split(";")
        words = line[0].split(" ")
        adjective, vehicle, irony = words[1], words[4], words[5].rstrip('\n')
        frequencies = line[1].split(" ")
        return cls(adjective, vehicle, irony, frequencies[0], frequencies[1].rstrip("\n"))

    @classmethod
    def from_line_no_irony(cls, line):
        line = line.split(";")
        words = line[0].split(" ")
        adjective, vehicle = words[1], words[4]
        frequencies = line[1].split(" ")
        return cls(adjective, vehicle, irony=False, frequency=frequencies[0], about_frequency=frequencies[1].rstrip("\n"))

    def initialise(self):

        if self.frequency == 0:
            self.determine_frequencies()
        self.find_synonyms()

        self.find_antonyms()

        self.such_as = text_utils.such_as(self)

        self.inverse = get_inverse(self)

        if self.inverse is not None:

            fa = open('../res/pdata/invwfrequ.txt', 'rb')
            frequ_inverses = pickle.load(fa)
            fa.close()
            for inv in frequ_inverses:
                    if inv.name == self.inverse.name:
                        self.inverse.frequency = inv.frequency
                        self.inverse.about_frequency = inv.about_frequency

    def find_synonyms(self):
        get_synonyms(self.ground, self.ground_synonyms, wn.ADJ)
        get_synonyms(self.vehicle, self.vehicle_synonyms, wn.NOUN)

    def find_antonyms(self):
        if True:
            for syn in wn.synsets(self.ground, wn.ADJ):
                #print syn
                for lemma in syn.lemmas():
                    #print lemma
                    #print lemma.antonyms()
                    for antonym in lemma.antonyms():
                        if antonym.name().encode("utf-8") not in self.antonyms:
                            self.antonyms.append(antonym.name().encode("utf-8"))
            #print "word : " + self.ground
            #print "antonyms : " + str(self.antonyms)

    def morphological_similar(self):
        # TODO: iii) between the vehicle and an adjective that is a frequent conjoined
        # with the ground as a co-descriptor (e.g. as [cold and snowy] as snow)

        for word in self.ground_synonyms:
            if self.vehicle in word:
                return True

        return False

    def determine_frequencies(self):
        self.frequency = int(query_utils.get_num_results(self.name))
        self.about_frequency = int(query_utils.get_num_results("about " + self.name))

        if self.about_frequency > self.frequency:
            self.about_frequency = 0

    def get_frequencies(self):
        return str(self.frequency) + " " + str(self.about_frequency) + "\n"

    def about_dominant(self):
        return float(self.about_frequency) > 0.5 * float(self.frequency)

    def high_web_frequency(self):
        return int(self.frequency) >= 10


def parse_old():
    similes = []
    with open('../res/similes.txt', 'r') as f:
        for line in f:
            simile = Simile.from_line(line)
            simile.initialise()
            similes.append(simile)

    return similes


class SimileData:
    def __init__(self):
        self.similes = []
        self.number = 0
        self.num_ironics = 0

    def load_data(self):
        if os.stat('../res/pdata/similedata.txt').st_size == 0:
            self.similes = parse_old()
            self.number = len(self.similes)
            for simile in self.similes:
                if simile.ironic:
                    self.num_ironics += 1
            self.save_data()
        else:
            f = open('../res/pdata/similedata.txt', 'r')
            tmp_data = pickle.load(f)
            self.similes = tmp_data.similes
            self.number = tmp_data.number
            self.num_ironics = tmp_data.num_ironics
            f.close()

    def save_data(self):
        print "save data thou"
        f = open('../res/pdata/similedata.txt', 'wb')
        pickle.dump(self, f)
        f.close()
