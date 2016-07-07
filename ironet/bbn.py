"""Bayesian network for irony detection"""


def f_irony(ironic):
    if ironic:
        return 0.18
        #return 0.5
    else:
        #return 0.5
        return 0.82


def f_morphological_similarity(similar, ironic):
    """
    Step 1
    Is there a lexical similarity between vehicle and ground or related words?
    :param similar: morphological similarity?
    :param ironic: truth value of irony
    """
    if ironic:
        if similar:
            return 0.0067
        else:
            return 0.993
    else:
        if similar:
            return 0.02348
        else:
            return 0.97651


def f_synonym_similar(synonym_similar, ironic):
    if ironic:
        if synonym_similar:
            return 0.0055
        else:
            return 0.9945
    else:
        if synonym_similar:
            return 0.02
        else:
            return 0.98


# TODO test and get frequencies
def f_codescr_morph(codescr_similar, ironic):
    """
    Step 1, c)
    Is there a lexical similarity between vehicle and a codescriptor of the ground?
    :param similar: morphological similarity?
    :param ironic: truth value of irony
    """
    if ironic:
        if codescr_similar:
            return 0.00169
        else:
            return 0.99831
    else:
        if codescr_similar:
            return 0.0011
        else:
            return 0.9989


def f_about_frequency(about_dominant, ironic):
    """ Predominance of "about":
    Is the web frequency of "about as GROUND as a VEHICLE" more than half that of "as GROUND as VEHICLE" -> ironic
    """
    if ironic:
        if about_dominant:
            return 0.32
        else:
            return 0.68
    else:
        if about_dominant:
            return 0.052
        else:
            return 0.948


def f_such_as(such_as, ironic):
    """
    Step 5 and 6:
    Is there a "GROUND * such as VEHICLE" found on the web? (or here: Wikipedia)
    """
    if ironic:
        if such_as:
            return 0.09
        else:
            return 0.91
    else:
        if such_as:
            return 0.17
        else:
            return 0.83


def f_inverse_variation(inverse_var, ironic):
    """
    Step 7:
    Is the simile an inverse variation of a non-ironic simile?
    """
    if ironic:
        if inverse_var:
            return 0.19
        else:
            return 0.81
    else:
        if inverse_var:
            return 0.26
        else:
            return 0.74


def f_web_frequency(high_web_frequ, ironic):
    """
    Step 8 and 9: Is the web-frequency >= 10? -> non-ironic
    """
    if ironic:
        if high_web_frequ:
            return 0.453
        else:
            return 0.547
    else:
        if high_web_frequ:
            return 0.6
        else:
            return 0.4


