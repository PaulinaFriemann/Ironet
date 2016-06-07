"""Bayesian network for irony detection"""

from bayesian.bbn import *
from simile_parser import *
#from IPython import embed
#from nltk.corpus import wordnet as wn
#from nltk.corpus import lin_thesaurus as lin
from itertools import chain


def f_irony(ironic):
    if ironic:
        return 0.18
    else:
        return 0.82


def f_morphological_similarity(similar, ironic):
    """
    Is there a lexical similarity between vehicle and ground or related words?
    :param similar: morphological similarity?
    :param ironic: truth value of irony
    """
    if ironic:
        if similar:
            return 0
        else:
            return 1
    else:
        if similar:
            return 1
        else:
            return 0


def f_about_frequency(about_dominant, ironic):
    """ Predominance of "about":
    Is the web frequency of "about as GROUND as a VEHICLE" more than half that of "as GROUND as VEHICLE" -> ironic
    """
    if ironic:
        if about_dominant:
            return 1
        else:
            return 0
    else:
        if about_dominant:
            return 0
        else:
            return 1


def f_affect(ironic, affect):
    if ironic:
        if affect >= 2.28:
            return 0.14
        elif affect <= 1.36:
            return 123
        else:
            pass
    else:
        pass


def main():

    data = SimileData()

    data.parse_similes()
    #
    # g = build_bbn(
    #     f_irony,
    #     f_about_frequency,
    #     domains=dict(
    #         ironic=[True, False],
    #         similar=[True, False]
    #     )
    # )
    #
    # similes = [Simile('pretty', 'warthog', 'i'), Simile('manly', 'man', 'h')]
    #
    # honest = []
    # ironic = []
    #
    # correctly_categorized_honest = 0
    # correctly_categorized_ironic = 0
    # falsely_categorized_ironic = 0
    # falsely_categorized_honest = 0
    #
    # for simile in data.similes:
    #     result = g.query(similar=simile.about_predominant())
    #     if result[('ironic', True)] == 1:
    #         ironic.append(simile.name())
    #         if simile.ironic:
    #             correctly_categorized_ironic += 1
    #         else:
    #             falsely_categorized_ironic += 1
    #     else:
    #         honest.append(simile.name())
    #         if not simile.ironic:
    #             correctly_categorized_honest += 1
    #         else:
    #             falsely_categorized_honest += 1
    #
    # print honest
    # print ironic
    #
    # print correctly_categorized_honest
    # print falsely_categorized_honest
    # print correctly_categorized_ironic
    # print falsely_categorized_ironic


    #embed()

if __name__ == '__main__':
    main()
