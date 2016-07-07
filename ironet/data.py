from words import *
from simile import Simile


def pickle_data(path, obj):
    f = open('../res/pdata/database/' + path, 'w')
    pickle.dump(obj, f)


def load_data(path):
    f = open('../res/pdata/database/' + path, 'r')
    return pickle.load(f)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Data:
    __metaclass__ = Singleton

    def __init__(self):
        self.frequencies = dict()
        self.similes = []
        self.grounds = dict()
        self.vehicles = dict()
        self.ironic = dict()
        self.other_similes = []

        self.load()

    def add_simile_frequency(self, ground, vehicle, frequency):
        self.frequencies[(ground, vehicle)] = frequency

    def add_ground(self, ground):
        if ground not in self.grounds.keys():
            self.grounds[ground] = Ground(ground)
        return self.grounds[ground]

    def add_vehicle(self, vehicle):
        if vehicle not in self.vehicles.keys():
            self.vehicles[vehicle] = Vehicle(vehicle)
        return self.vehicles[vehicle]

    def get_ground(self, name):
        return self.grounds[name]

    def get_vehicle(self, name):
        return self.vehicles[name]

    def add_frequency(self, ground, vehicle, frequency, about_frequency):
        self.frequencies[(ground.name, vehicle.name)] = 0

    def get_frequency(self, ground, vehicle):
        try:
            return self.frequencies.get((ground, vehicle))
        except KeyError:
            return None

    def get_frequency_objects(self, ground, vehicle):
        try:
            return self.frequencies.get((ground.name, vehicle.name))
        except KeyError:
            return None

    def save(self):
        pickle_data('frequencies.p', self.frequencies)
        pickle_data('grounds.p', self.grounds)
        pickle_data('ironic.p', self.ironic)
        pickle_data('similes_f.p', self.similes)
        pickle_data('similes_n.p', self.other_similes)
        pickle_data('vehicles.p', self.vehicles)

    def load(self):
        self.frequencies = load_data('frequencies.p')
        self.grounds = load_data('grounds.p')
        self.ironic = load_data('ironic.p')
        self.similes = load_data('similes_f.p')
        self.other_similes = load_data('similes_n.p')
        self.vehicles = load_data('vehicles.p')
