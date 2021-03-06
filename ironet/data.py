"""
Stores all the needed data about the similes
"""
from words import *
import utils.query_utils as qu
import pickle


def pickle_data(path, obj):
    f = open('../res/pdata/database/' + path, 'w')
    pickle.dump(obj, f)


def load_data(path):
    f = open('../res/pdata/database/' + path, 'r')
    return pickle.load(f)


def get_inverses(ground, vehicle):
    """
    Finds the inverses for a given ground and vehicle, where inverse = as GROUND-antonym as VEHICLE
    """
    inverses = []
    for antonym in ground.antonyms:
        inverse = (antonym, vehicle.name)
        inverses.append(inverse)
    return inverses


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Data:
    __metaclass__ = Singleton

    def __init__(self):
        self.frequencies = dict()  # (ground, vehicle)
        self.similes = []  # (ground, vehicle)
        self.grounds = dict()  # stores objects to names
        self.vehicles = dict()  # objects to names
        self.ironic = dict()  # (ground, vehicle)
        self.other_similes = []  # the similes which do not have a frequency yet
        self.inverses = dict()
        self.attribute_results = dict()

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
        if type(name) == 'instance':
            name = name.name
        try:
            return self.grounds[name]
        except KeyError:
            self.add_ground(name)
            return self.grounds[name]

    def get_vehicle(self, name):
        if type(name) == 'instance':
            name = name.name
        try:
            return self.vehicles[name]
        except KeyError:
            print name
            self.add_vehicle(name)
            return self.vehicles[name]

    def add_frequency(self, ground, vehicle, frequency, about_frequency):
        self.frequencies[(ground.name, vehicle.name)] = [frequency, about_frequency]

    def get_frequencies(self, ground, vehicle):
        if type(ground) == 'instance':
            ground = ground.name
        if type(vehicle) == 'instance':
            vehicle = vehicle.name
        try:
            return self.frequencies.get((ground, vehicle))
        except KeyError:
            return None

    def get_inverse(self, ground, vehicle):
        try:
            return self.inverses.get((ground, vehicle))
        except KeyError:
            return None

    def get_simile_name(self, ground, vehicle):
        return "as " + ground + " as " + "a|an " + vehicle

    def find_frequency(self, simile):
        """
        finds the web frequency of a simile with and without the about marker
        :param simile: (ground, vehicle)
        """
        frequency = 0
        about_frequency = 0
        if not self.get_frequencies(simile.ground, simile.vehicle):
            frequency = int(qu.get_num_results(simile.name, simile.vehicle.name))

        if frequency != 0:
            about_frequency = int(qu.get_num_results("about " + simile.name, simile.vehicle.name))

        if about_frequency > frequency:
            about_frequency = 0

        self.frequencies[(simile.ground.name, simile.vehicle.name)] = [frequency, about_frequency]

    def save(self):
        pickle_data('frequencies.p', self.frequencies)
        pickle_data('grounds.p', self.grounds)
        pickle_data('ironic.p', self.ironic)
        pickle_data('similes_t.p', self.similes)
        pickle_data('similes_n.p', self.other_similes)
        pickle_data('vehicles.p', self.vehicles)
        pickle_data('inverses.p', self.inverses)
        pickle_data('attribute_results.p', self.attribute_results)

    def load(self):
        self.frequencies = load_data('frequencies.p')
        self.grounds = load_data('grounds.p')
        self.ironic = load_data('ironic.p')
        self.similes = load_data('similes_t.p')
        self.other_similes = load_data('similes_n.p')
        self.vehicles = load_data('vehicles.p')
        self.inverses = load_data('inverses.p')
        self.attribute_results = load_data('attribute_results.p')
