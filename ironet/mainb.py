from bayesian.bbn import *

import bbn2
import simile_properties as sp
from data import Data

data = Data()


def simulate_inverse(simile, g):
    global data

    ironic_results = 0
    for inverse in data.get_inverse(simile[0], simile[1]):
        if not query(inverse, g, True, True, True, True):
            ironic_results += 1

    return not float(ironic_results) >= len(data.inverses[simile])/2


def query(simile, g, web_frequ=False, about=False, similarity=False, such_as=False, inverse=False):
    params = {}
    if web_frequ:
        params["high_web_frequ"] = sp.high_web_frequency(simile)
    if about:
        params["about_dominant"] = sp.about_dominant(simile)
    if similarity:
        params["similar"] = sp.morphological_similar(simile) or sp.synonym_similar(simile) or sp.codescriptor_morph(simile)
    if such_as:
        params["attributes"] = sp.attributes(simile)
    if inverse and data.get_inverse(simile[0], simile[1]) is not None:
        params["inverse_var"] = simulate_inverse(simile, g)
    #result = g.q(**params)
    result = g.query(**params)
    return result[('ironic', True)] >= 0.5


def main():

    print "build network"
    global data

    g = build_bbn(
        bbn2.f_irony,
        bbn2.f_web_frequency,
        bbn2.f_about_frequency,
        bbn2.f_morphological_similarity,
        bbn2.f_inverse_variation,
        bbn2.f_attributes,
        domains=dict(
            ironic=[True, False],
            high_web_frequ=[True, False],
            about_dominant=[True, False],
            similar=[True, False],
            inverse_var=[True, False],
            attributes=['00', '10', '01', '11', '02', '12', '20', '21', '22']
        )
    )
    print "done"

    honest = []
    ironic = []

    honest_as_honest = 0
    ironic_as_ironic = 0
    honest_as_ironic = 0
    ironic_as_honest = 0


    #query(('straight', 'rail'), g, such_as=True)

    for simile in data.similes:
        include_inverse = False
        if data.get_inverse(simile[0], simile[1]) is not None:
            #if simile.inverse.frequency
            include_inverse = True
       # result = query(simile, g, web_frequ=False, about=False, similarity=True, such_as=False, inverse=include_inverse)
        result = query(simile, g, web_frequ=True, about=True, similarity=True, such_as=True, inverse=include_inverse)
        if result:
            ironic.append(str(simile) + " i")
            if sp.ironic(simile):
                ironic_as_ironic += 1
            else:
                honest_as_ironic += 1
        else:
            honest.append(str(simile) + " h")
            if not sp.ironic(simile):
                honest_as_honest += 1
            else:
                ironic_as_honest += 1

    print "honest as honest " + str(honest_as_honest)
    print "ironic as honest " + str(ironic_as_honest)
    print "ironic as ironic " + str(ironic_as_ironic)
    print "honest as ironic " + str(honest_as_ironic)


if __name__ == '__main__':
    main()
