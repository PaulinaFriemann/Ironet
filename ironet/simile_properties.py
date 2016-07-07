from data import Data

database = Data()


def morphological_similar(simile):

    if simile.vehicle.name in simile.ground.name:
        return True
    else:
        return False


def synonym_similar(simile):

    for word in simile.ground.synonyms[1:]:
        if simile.vehicle.name in word:
            print word + " " + simile.vehicle.name
            return True

    return False


def codescriptor_morph(simile):
    for word in simile.ground.codescriptors:
        if simile.vehicle.name in word:
            print simile.vehicle.name + " " + word
            return True
    return False


def about_dominant(simile, data):

    return data.get_frequency_objects(simile.ground, simile.vehicle)[1] \
           >= 0.5 * data.get_frequency_objects(simile.ground, simile.vehicle)[0]


def high_web_frequency(simile, data):

    return data.get_frequency_objects(simile.ground, simile.vehicle)[0] >= 10


def such_as(simile):

    if simile.vehicle.has_attribute(simile.ground):
        return True
    else:
        return False


def ironic(simile, data):
    return data.ironic[(simile.ground.name, simile.vehicle.name)]
