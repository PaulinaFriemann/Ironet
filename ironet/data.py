from words import *
from simile import *


def pickle_data(path, obj):
    f = open('../res/pdata/database/' + path, 'w')
    pickle.dump(obj, f)

class Data:

    def __init__(self):
        self.frequencies = dict()
        self.similes = []
        self.grounds = dict()
        self.vehicles = dict()
        self.ironic = dict()
        self.other_similes = []

    def add_simile_frequency(self, ground, vehicle, frequency):
        self.frequencies[(ground, vehicle)] = frequency

    def add_simile(self, ground, vehicle):
        self.similes.append((ground, vehicle))

    def save(self):
        pickle_data('frequencies.p', self.frequencies)
        pickle_data('grounds.p', self.grounds)
        pickle_data('ironic.p', self.ironic)
        pickle_data('similes_f.p', self.similes)
        pickle_data('similes_n.p', self.other_similes)
        pickle_data('vehicles.p', self.vehicles)

    def load(self):
        wd = WordDatabase()
        db = SimileData()

        self.grounds = wd.grounds
        self.vehicles = wd.vehicles

        db.load_data()

        self.similes = db.similes
        self.frequencies = db.simile_frequencies

        temp, self.ironic = parse_all()

        self.other_similes = temp[3000:]

        self.save()
