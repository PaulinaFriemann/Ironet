from bayesian.bbn import *

import bbn
from simile import *


def simulate_inverse(simile, g):

    return query(simile.inverse, g, False, False, True, True, False)


def query(simile, g, web_frequ=False, about=False, similarity=False, such_as=False, inverse=False):
    params = {}
    if web_frequ and simile.frequency != 0 and simile.frequency != "0":
        params["high_web_frequ"] = simile.high_web_frequency()
    if about:
        params["about_dominant"] = simile.about_dominant()
    if similarity:
        params["similar"] = simile.morphological_similar()
    if such_as:
        params["such_as"] = simile.such_as
    if inverse and simile.inverse is not None:
        params["inverse_var"] = simulate_inverse(simile, g)
    result = g.query(**params)
    return result[('ironic', True)] >= result[('ironic', False)]


def main():
    #data = SimileData()
    #data.load_data()
    #text_utils.get_not_done(data)
    #get_all_inverses(data)
    #text_utils.pickle_inverses(data)
    #text_utils.parse()
   #text_utils.get_frequencies()
    #get_inverse_frequency(data)
    #print data.similes[0].inverses[0].frequency
    text_utils.get_all_such()


def mainb():

    data = SimileData()
    data.load_data()

    g = build_bbn(
        bbn.f_irony,
        bbn.f_web_frequency,
        bbn.f_about_frequency,
        bbn.f_morphological_similarity,
        bbn.f_such_as,
        bbn.f_inverse_variation,
        domains=dict(
            ironic=[True, False],
            high_web_frequ=[True, False],
            about_dominant=[True, False],
            similar=[True, False],
            such_as=[True, False],
            inverse_var=[True, False]
        )
    )

    honest = []
    ironic = []

    honest_as_honest = 0
    ironic_as_ironic = 0
    honest_as_ironic = 0
    ironic_as_honest = 0

    for simile in data.similes:
        include_inverse = False
        if simile.inverse is not None:
            #if simile.inverse.frequency
            include_inverse = True
        result = query(simile, g, True, True, True, True, inverse=include_inverse)
        if result:
            ironic.append(simile.name + " i")
            if simile.ironic:
                print "ironic as ironic " + simile.name + " " + simile.get_frequencies()
                ironic_as_ironic += 1
            else:
                print "honest as ironic " + simile.name + " " + simile.get_frequencies()
                honest_as_ironic += 1
        else:
            honest.append(simile.name + " h")
            if not simile.ironic:
                honest_as_honest += 1
            else:
                print "ironic as honest " + simile.name + " " + simile.get_frequencies()
                ironic_as_honest += 1

    print honest_as_honest
    print ironic_as_honest
    print ironic_as_ironic
    print honest_as_ironic

    print "insgesamt: " + str(data.number)
    print "davon ironisch " + str(data.num_ironics)

if __name__ == '__main__':
    main()
