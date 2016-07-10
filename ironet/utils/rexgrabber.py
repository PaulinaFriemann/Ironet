import requests
from bs4 import BeautifulSoup
from IPython import embed
from collections import Counter


def do_request(vehicle):
    result = requests.get('http://ngrams.ucd.ie/therex2/common-nouns/member.action',
                          params={'member': vehicle,
                                  "kw": vehicle,
                                  'needDisamb': 'true',
                                  'xml': 'true'}
                          )

    return result


def find_attributes(result):
    soup = BeautifulSoup(result.text, "lxml-xml")
    modifiers = soup.find_all('Modifier')

    too_low = []

    weights = dict()
    for modifier in modifiers:
        attribute = modifier.string.strip().encode("utf-8")
        weight = int(modifier.get('weight'))
        weights[attribute] = weight
        # if  < 100:
        #     too_low.append(attribute)
    most_common = Counter(weights).most_common(5)
    attributes = [attribute[0] for attribute in most_common]

    #attributes = [modifier.string.strip().encode("utf-8") for modifier in modifiers]

    #attributes = list(set(attributes) - set(too_low))

    return attributes


def has_attribute(ground, vehicle):

    if type(ground) == 'instance':
        ground = ground.name
    if type(vehicle) == 'instance':
        vehicle = vehicle.name

    result = do_request(vehicle)
    attributes = find_attributes(result)

    return ground in attributes
