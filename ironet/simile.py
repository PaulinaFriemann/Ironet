import os
import pickle
from words import Ground, Vehicle
from words import WordDatabase as WD

import utils.query_utils as query_utils

database = WD()


def get_inverses(simile):
        inverses = []
        for antonym in simile.ground.antonyms:
            inverse = Simile(antonym, simile.vehicle)
            inverses.append(inverse)
        return inverses


class Simile:

    def __init__(self, ground, vehicle, frequency=0, about_frequency=0):
        global database

        if ground not in database.grounds:
            database.add_ground(ground)
        if vehicle not in database.vehicles:
            database.add_vehicle(vehicle)

        self.ground = database.get_ground(ground)
        self.vehicle = database.get_vehicle(vehicle)

        self.frequency = int(frequency)
        self.about_frequency = int(about_frequency)
        self.inverses = []

        self.name = "as " + self.ground + " as " + "a|an " + self.vehicle

        #if self.frequency == 0:
         #   self.determine_frequencies()

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

        self.inverses = get_inverses(self)

    def determine_frequencies(self):
        self.frequency = int(query_utils.get_num_results(self.name))
        self.about_frequency = int(query_utils.get_num_results("about " + self.name))

        if self.about_frequency > self.frequency:
            self.about_frequency = 0

    def get_frequencies(self):
        return str(self.frequency) + " " + str(self.about_frequency) + "\n"


def parse_all():

    global database

    similes = []
    with open('../res/similesNoDups.txt', 'r') as f:
        for line in f:
            #line = line.split(";")
            words = line.split(" ")
            ground, vehicle = words[1], words[4]
            #frequencies = line[1].split(" ")

            simile = Simile(ground, vehicle)
            simile.initialise()
            similes.append(simile)
    database.save()


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
