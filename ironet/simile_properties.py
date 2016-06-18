def morphological_similar(simile):
    # TODO: iii) between the vehicle and an adjective that is a frequent conjoined
    # with the ground as a co-descriptor (e.g. as [cold and snowy] as snow)

    for word in simile.ground.synonyms:
        if simile.vehicle.name in word:
            return True

    for word in simile.ground.codescriptors:
        if simile.vehicle.name in word:
            return True

    return False


def about_dominant(simile):
    return float(simile.about_frequency) > 0.5 * float(simile.frequency)


def high_web_frequency(simile):
    return int(simile.frequency) >= 10


def such_as(simile):
    for ground in simile.ground.synonyms:
        for vehicle in simile.vehicle.synonyms:
            if vehicle.has_attribute(ground):
                return True
    return False
