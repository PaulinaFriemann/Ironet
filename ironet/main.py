"""
This NEEDS the Bayesian network library from https://github.com/eBay/bayesian-belief-networks
"""
from bayesian.bbn import *

import bbn
import simile_properties as sp
from tqdm import tqdm

from data import Data

data = Data()


def simulate_inverse(simile, g):
    global data

    ironic_results = 0
    for inverse in data.get_inverse(simile[0], simile[1]):
        if not query(inverse, g, web_frequ=True, about=True, similarity=True, attribute=True, inverse=False, syn_attributes=True):
            ironic_results += 1

    return not float(ironic_results) >= len(data.inverses[simile])/2


def query(simile, g, web_frequ=False, about=False, similarity=False, attribute=False, inverse=False, syn_attributes=False):
    """
    Convenience Function. Does a query for the bayesian network
    :param simile:
    :param g: network
    :param web_frequ: use the web frequency
    :param about: use "about"-dominance attribute
    :param similarity: use morphological similarity
    :param attribute: use vehicle attributes
    :param inverse: simulate inverse
    :param syn_attributes: use attributes of the synonyms of the vehicle
    :return: True if marked as ironic
    """
    params = {}
    if web_frequ:
        params["high_web_frequ"] = sp.high_web_frequency(simile)
    if about:
        params["about_dominant"] = sp.about_dominant(simile)
    if similarity:
        params["similar"] = sp.morphological_similar(simile) or sp.synonym_similar(simile) or sp.codescriptor_morph(simile)
    if attribute:
        params["attributes"] = sp.attributes(simile)
    if inverse and data.get_inverse(simile[0], simile[1]) is not None:
        params["inverse_var"] = simulate_inverse(simile, g)
    if syn_attributes:
        params["syn_attributes"] = sp.syn_has_attributes(simile)

    result = g.query(**params)
    return result[('ironic', True)] >= 0.5


def build_network():

    g = build_bbn(
        bbn.f_irony,
        bbn.f_web_frequency,
        bbn.f_about_frequency,
        bbn.f_morphological_similarity,
        bbn.f_inverse_variation,
        bbn.f_attributes,
        bbn.f_synonym_attribute,
        domains=dict(
            ironic=[True, False],
            high_web_frequ=[True, False],
            about_dominant=[True, False],
            similar=[True, False],
            inverse_var=[True, False],
            attributes=['00', '10', '01', '11', '02', '12', '20', '21', '22'],
            syn_attributes=[1, 0, -1]
        )
    )

    return g


def main():

    print "build network"
    global data

    g = build_network()

    print "done"

    honest = []
    ironic = []

    honest_as_honest = 0
    ironic_as_ironic = 0
    honest_as_ironic = 0
    ironic_as_honest = 0

    for simile in tqdm(data.similes):
        include_inverse = False
        if data.get_inverse(simile[0], simile[1]) is not None:
            include_inverse = True

        result = query(simile, g, web_frequ=True, about=True, similarity=True, attribute=True, inverse=include_inverse, syn_attributes=True)

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
