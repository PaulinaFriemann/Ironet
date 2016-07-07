import utils.query_utils as query_utils

database = None


def init():
    global database
    from data import Data
    database = Data()


def get_inverses(simile):
        inverses = []
        for antonym in simile.ground.antonyms:
            inverse = Simile(antonym, simile.vehicle.name)
            inverses.append(inverse)
        return inverses


class Simile:

    def __init__(self, ground, vehicle):
        global database

        self.key = ground + ";" + vehicle

        self.ground = database.add_ground(ground)
        self.vehicle = database.add_vehicle(vehicle)

        self.inverses = []

        self.name = "as " + self.ground.name + " as " + "a|an " + self.vehicle.name

        self.inverses = get_inverses(self)

    def determine_frequencies(self):

        if not database.get_frequency_objects(self.ground, self.vehicle):
            self.frequency = int(query_utils.get_num_results(self.name, self.vehicle.name))
            if self.frequency != 0:
                self.about_frequency = int(query_utils.get_num_results("about " + self.name, self.vehicle.name))

        if self.about_frequency > self.frequency:
            self.about_frequency = 0

    def equals(self, other):
        if self.ground.name == other.ground.name and self.vehicle.name == other.vehicle.name:
            return True
        return False
