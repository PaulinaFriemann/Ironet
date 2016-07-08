"""
Properties of similes used for the Bayesian network
"""
from data import Data

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


def such_as(simile):
    """
    Does the VEHICLE have the attribute GROUND? (Taken from Wikipedia -
    "GROUND x such as VEHICLE")
    :param simile:
    :return:
    """

    if database.get_vehicle(simile[1]).has_attribute(database.get_ground(simile[0])):
        return True
    else:
        return False


def ironic(simile):
    return database.ironic[(simile[0], simile[1])]
