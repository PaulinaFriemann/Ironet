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
            return 0.007
        else:
            return 0.993
    else:
        if similar:
            return 1
        else:
            return 0.975



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


def f_attributes(attributes, ironic):
    atts_probs = [{'00': 0.87, '10': 0.004, '01': 0.04, '11': 0.002, '02':1, '12':0.002, '20': 0.04, '21':0.013, '22':0.002}, {'00': 0.82, '10': 0.0364, '01': 0.0027, '11': 0.002, '02':0, '12':0, '20': 1, '21':0.0039, '22':0}]
    return atts_probs[int(not ironic)][attributes]


def f_synonym_attribute(syn_attributes, ironic):

    if ironic:
        if syn_attributes == 1:
            return 0.092
        elif syn_attributes == -1:
            return 0.0527
        elif syn_attributes == 0:
            return 0.83

    else:
        if syn_attributes == 1:
            return 0.241
        elif syn_attributes == -1:
            return 0.006
        elif syn_attributes == 0:
            return 0.75


def f_inverse_variation(inverse_var, ironic):
    """
    Step 7:
    Is the simile an inverse variation of a non-ironic simile?
    """
    if ironic:
        if inverse_var:
            #return 0.246
            #return 0.577 # ironic results > 0
            #return 0.62 # iro results > 1/2
            #return 0.54 # honest > 0
            return 0.33 # honest >= 1/2
            #return 0
        else:
            #return 1
            return 0.67 # honest >= 1/2
            #return 0.46  # honest > 0
            #return 0.423 # ironic results > 0
            #return 0.38 # iro results > 1/2
            #return 0.754
    else:
        if inverse_var:
            return 0.44  # honest >= 1/2
            #return 0.5 # ironic results > 0
            #return 1
            #return 0.744 # honest > 0
            # return 0.78 # ironic results > 1/2
            #return 0.8544
        else:
            return 0.56  # honest >= 1/2
            #return 0.5
            #return 0.22 # ironic results > 1/2
            #return 0.256 # honest > 0
            #return 0
            #return 0.1456


def f_web_frequency(high_web_frequ, ironic):
    """
    Step 8 and 9: Is the web-frequency >= 10? -> non-ironic
    """
    if ironic:
        if high_web_frequ:
            #return 0.453
            return 0.453
        else:
            return 0.547
            #return 0.547
    else:
        if high_web_frequ:
            return 0.6
            #return 0.6
        else:
            return 0.4
            #return 0.4


