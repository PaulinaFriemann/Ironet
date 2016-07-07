from words import WordDatabase as WD

database = WD()

def morphological_similar(simile):
    # TODO: iii) between the vehicle and an adjective that is a frequent conjoined
    # with the ground as a co-descriptor (e.g. as [cold and snowy] as snow)

    if simile.vehicle.name in simile.ground.name:
        return True
    else:
        return False


def synonym_similar(simile):
    #print simile.ground.synonyms
    #print simile.ground.synonyms[1:]
    for word in simile.ground.synonyms[1:]:
        if simile.vehicle.name in word:
            print word + " " + simile.vehicle.name
            return True

    return False


# TODO add node
def codescriptor_morph(simile):
    for word in simile.ground.codescriptors:
        if simile.vehicle.name in word:
            print simile.vehicle.name + " " + word
            return True
    return False


def about_dominant(simile, data):
    #return float(simile.about_frequency) > 0.5 * float(simile.frequency)
    return data.get_frequency(simile.key)[1] >= 0.5 * data.get_frequency(simile.key)[0]


def high_web_frequency(simile, data):
    #return int(simile.frequency) >= 10
    return data.get_frequency(simile.key)[0] >= 10


def such_as(simile):
    print database.vehicles.__sizeof__()

    for ground in simile.ground.synonyms:
        for vehicle in simile.vehicle.synonyms:
            if vehicle not in database.vehicles:
                database.add_vehicle(vehicle)
            veh_object = database.get_vehicle(vehicle)
            if veh_object.has_attribute(ground):
                return True
    return False


def ironic(simile, data):
    return data.ironic[simile.key]
