from bayesian.bbn import *

import bbn
import simile_properties as sp
import rexgrabber as rex
from tqdm import tqdm

import utils.text_utils as tu
from data import Data

data = Data()


def simulate_inverse(simile, g):
    global data

    ironic_results = 0
    for inverse in data.get_inverse(simile[0], simile[1]):
        if not query(inverse, g, True, True, True, True, True, True):
            ironic_results += 1

    print "inverse " + str(data.inverses[simile]) + " " + str(ironic_results) + " freque " + str(data.get_frequency(simile[0], simile[1]))

    return not float(ironic_results) >= len(data.inverses[simile])/2
    #return not float(ironic_results) > 0


def query(simile, g, web_frequ=False, about=False, similarity=False, synonym_similar=False, codescr_similarity=False, such_as=False, inverse=False):
    params = {}
    if web_frequ:
        params["high_web_frequ"] = sp.high_web_frequency(simile)
    if about:
        params["about_dominant"] = sp.about_dominant(simile)
    if similarity:
        params["similar"] = sp.morphological_similar(simile)
    if synonym_similar:
        params["synonym_similar"] = sp.synonym_similar(simile)
    if codescr_similarity:
        params["codescr_similar"] = sp.codescriptor_morph(simile)
    if such_as:
        params["attributes"] = sp.attributes(simile)
    if inverse and data.get_inverse(simile[0], simile[1]) is not None:
        params["inverse_var"] = simulate_inverse(simile, g)
    print simile
    result = g.q(**params)
    result = g.query(**params)
    return result[('ironic', True)] >= 0.5
    #return result[('ironic', True)] >= result[('ironic', False)]


def main():

    da = Data()

    #print da.get_vehicle('feather').attributes

    # for vehicle in da.vehicles.values():
    #     vehicle.attributes = []
    #     vehicle.attributes = rex.find_attributes(rex.do_request(vehicle.name))
    # da.save()
    num = 0
    # for simile in da.similes:
    #     if da.ironic[simile]:
    #         vehicle = da.get_vehicle(simile[1])
    #         for syn in vehicle.synonyms:
    #             print da.get_vehicle(syn).attributes

    results = {}
    for simile in tqdm(da.similes):
        if not da.ironic[simile]:
            result = sp.synonym_has_attribute(simile)
            try:
                results[str(result)] += 1
            except KeyError:
                results[str(result)] = 1
    print results

    da.save()


def mainb():

    print "build network"
    global data

    g = build_bbn(
        bbn.f_irony,
        bbn.f_web_frequency,
        bbn.f_about_frequency,
        bbn.f_morphological_similarity,
        bbn.f_synonym_similar,
        bbn.f_codescr_morph,
        bbn.f_inverse_variation,
        bbn.f_attributes,
        domains=dict(
            ironic=[True, False],
            high_web_frequ=[True, False],
            about_dominant=[True, False],
            similar=[True, False],
            synonym_similar=[True, False],
            codescr_similar=[True, False],
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
       # result = query(simile, g, web_frequ=False, about=False, similarity=False, synonym_similar=False, codescr_similarity=False, such_as=True, inverse=include_inverse)
        result = query(simile, g, web_frequ=True, about=True, similarity=True, synonym_similar=True,
                       codescr_similarity=True, such_as=True, inverse=include_inverse)
        if result:
            ironic.append(str(simile) + " i")
            if sp.ironic(simile):
                #print "ironic as ironic " + simile.name + " " + simile.get_frequencies()
                ironic_as_ironic += 1
            else:
                #print "honest as ironic " + simile.name + " " + simile.get_frequencies()
                honest_as_ironic += 1
        else:
            honest.append(str(simile) + " h")
            if not sp.ironic(simile):
                #print "honest as honest " + simile.name + " " + simile.get_frequencies()
                honest_as_honest += 1
            else:
                #print "ironic as honest " + simile.name + " " + simile.get_frequencies()
                ironic_as_honest += 1

    print "honest as honest " + str(honest_as_honest)
    print "ironic as honest " + str(ironic_as_honest)
    print "ironic as ironic " + str(ironic_as_ironic)
    print "honest as ironic " + str(honest_as_ironic)


if __name__ == '__main__':
    main()
