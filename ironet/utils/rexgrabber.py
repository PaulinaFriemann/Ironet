import requests
from bs4 import BeautifulSoup
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
    """
    Grabs the 7 attributes with the highest weight
    :param result: Request result
    :return: list with attributes
    """
    soup = BeautifulSoup(result.text, "lxml-xml")
    modifiers = soup.find_all('Modifier')

    weights = dict()
    for modifier in modifiers:
        attribute = modifier.string.strip().encode("utf-8")
        weight = int(modifier.get('weight'))
        weights[attribute] = weight

    most_common = Counter(weights).most_common(7)
    attributes = [attribute[0] for attribute in most_common]

    return attributes
