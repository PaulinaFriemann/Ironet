"""
Properties of similes used for the Bayesian network
"""
from data import Data
import utils.rexgrabber as rex
from collections import Counter

database = Data()


def morphological_similar(simile):
    """
    Is the vehicle contained in the ground? (e.g. As manly as a man)
    :param simile: (GROUND, VEHICLE)
    :return: True if contained, else false
    """

    if simile[0] in simile[1]:
        return True
    else:
        return False


def synonym_similar(simile):
    """
    Is the vehicle contained in one of the synonyms of the ground?
    :param simile: (GROUND, VEHICLE)
    :return:
    """

    for word in database.get_ground(simile[0]).synonyms[1:]:
        if simile[1] in word:
            print word + " " + simile[1]
            return True

    return False


def codescriptor_morph(simile):
    """
    Is the vehicle contained in a codescriptor of the ground?
    :param simile: (GROUND, VEHICLE)
    :return:
    """
    for word in database.get_ground(simile[0]).codescriptors:
        if simile[1] in word:
            print simile[1] + " " + word
            return True
    return False


def about_dominant(simile):
    """
    Is the frequency of "about as GROUND as VEHICLE" at least half of the base frequency?
    :param simile: (GROUND, VEHICLE)
    :return:
    """

    return database.get_frequency(simile[0], simile[1])[1] \
           >= 0.5 * database.get_frequency(simile[0], simile[1])[0]


def high_web_frequency(simile):
    """
    Is the web frequency more than 10?
    :param simile:
    :return: True if more than 10, else false
    """

    return database.get_frequency(simile[0], simile[1])[0] >= 10


def ironic(simile):

    return database.ironic[simile]


def attributes(simile):
    """
    Does the VEHICLE have the attribute GROUND? (Taken from Thesaurus Rex)
    :param simile: (GROUND, VEHICLE)
    :return:
    """
    syn_one_mult = 0
    ant_one_mult = 0
    ground = database.get_ground(simile[0])
    vehicle = database.get_vehicle(simile[1])

    if vehicle.has_attribute(ground.name):
        syn_one_mult = 1
    for synonym in ground.synonyms:
        if synonym != ground.name:
            if vehicle.has_attribute(synonym):
                syn_one_mult = 2
                print synonym + ", ground: " + ground.name + ", vehicle: " + vehicle.name
    if not ground.antonyms:
        ant_one_mult = 0
    else:
        for antonym in ground.antonyms:
            if vehicle.has_attribute(antonym):
                if ant_one_mult == 0:
                    ant_one_mult = 1
                else:

                    ant_one_mult = 2
    return str(syn_one_mult)+ str(ant_one_mult)


def synonym_has_attribute(simile):
    """
    Does a synonym of VEHICLE have the attribute GROUND? (Taken from Thesaurus Rex)
    :param simile: (GROUND, VEHICLE)
    :return: 1 if one has the attribute, -1 if has antonym, 0 else
    """
    ground = database.get_ground(simile[0])
    vehicles = database.get_vehicle(simile[1]).synonyms

    print len(ground.antonyms)

    has = 0
    has_not = 0
    results = []

    for vehicle, i in enumerate(vehicles):

        vehicle_object = database.get_vehicle(vehicle)

        for synonym in ground.synonyms:
            if vehicle_object.has_attribute(synonym):
                has += 1
        for antonym in ground.antonyms:
            if vehicle_object.has_attribute(antonym):
                has_not += 1

        if len(ground.synonyms) != 0:
            has_percent = has / len(ground.synonyms)
        else:
            has_percent = 0
        if len(ground.antonyms) != 0:
            has_not_percent = has_not / len(ground.antonyms)
        else:
            has_not_percent = 0

        if has_percent > has_not_percent:
            results[i] = 1
        elif has < has_not:
            results[i] = -1
        else:
            results[i] = 0

    result = 0
    for res in results:
        result += res
    database.attribute_results[simile] = result

    return result

