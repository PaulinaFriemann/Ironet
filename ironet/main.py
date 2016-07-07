from bayesian.bbn import *

import bbn
from simile import *
import simile_properties as sp
from query_utils import get_num_results

from words import WordDatabase
import utils.text_utils as tu


def simulate_inverse(simile, g, data):
    print "inverse"
    ironic_results = 0
    for inverse in simile.inverses:
        if query(inverse, g, data, False, False, True, True, False):
            ironic_results += 1

    return ironic_results >= len(simile.inverses)/2


def query(simile, g, data, web_frequ=False, about=False, similarity=False, synonym_similar=False, codescr_similarity=False, such_as=False, inverse=False):
    params = {}
    print simile.key
    if web_frequ:
        params["high_web_frequ"] = sp.high_web_frequency(simile, data)
    if about:
        params["about_dominant"] = sp.about_dominant(simile, data)
    if similarity:
        params["similar"] = sp.morphological_similar(simile)
    if synonym_similar:
        params["synonym_similar"] = sp.synonym_similar(simile)
    if codescr_similarity:
        params["codescr_similar"] = sp.codescriptor_morph(simile)
    if such_as:
        params["such_as"] = sp.such_as(simile)
    if inverse and simile.inverses is not None:
        params["inverse_var"] = simulate_inverse(simile, g, data)
    result = g.query(**params)
    return result[('ironic', True)] >= result[('ironic', False)]


def main():

    tu.get_attributes()


def mainb():

    data = SimileData()
    data.load_data()
    #data.similes, data.ironic = parse_all()

    print "build network"

    g = build_bbn(
        bbn.f_irony,
        bbn.f_web_frequency,
        bbn.f_about_frequency,
        bbn.f_morphological_similarity,
        bbn.f_synonym_similar,
        bbn.f_codescr_morph,
        bbn.f_such_as,
        bbn.f_inverse_variation,
        domains=dict(
            ironic=[True, False],
            high_web_frequ=[True, False],
            about_dominant=[True, False],
            similar=[True, False],
            synonym_similar=[True, False],
            codescr_similar=[True, False],
            such_as=[True, False],
            inverse_var=[True, False]
        )
    )
    print "done"

    honest = []
    ironic = []

    honest_as_honest = 0
    ironic_as_ironic = 0
    honest_as_ironic = 0
    ironic_as_honest = 0

    for simile in data.similes:
        include_inverse = False
        if simile.inverses is not None:
            #if simile.inverse.frequency
            include_inverse = True
        result = query(simile, g, data, web_frequ=True, about=True, similarity=True, synonym_similar=True, codescr_similarity=True, such_as=True, inverse=include_inverse)
        if result:
            ironic.append(simile.name + " i")
            if sp.ironic(simile, data):
                #print "ironic as ironic " + simile.name + " " + simile.get_frequencies()
                ironic_as_ironic += 1
            else:
                #print "honest as ironic " + simile.name + " " + simile.get_frequencies()
                honest_as_ironic += 1
        else:
            honest.append(simile.name + " h")
            if not sp.ironic(simile, data):
                #print "honest as honest " + simile.name + " " + simile.get_frequencies()
                honest_as_honest += 1
            else:
                #print "ironic as honest " + simile.name + " " + simile.get_frequencies()
                ironic_as_honest += 1

    print honest_as_honest
    print ironic_as_honest
    print ironic_as_ironic
    print honest_as_ironic

    print "insgesamt: " + str(data.number)
    print "davon ironisch " + str(data.num_ironics)

if __name__ == '__main__':
    main()
