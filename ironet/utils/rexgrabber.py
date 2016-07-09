import requests
from bs4 import BeautifulSoup
from IPython import embed


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
    for modifier in modifiers:
        attribute = unicode(modifier.string).strip()

        if int(modifier.get('weight')) < 100:
            too_low.append(attribute)

    attributes = [modifier.string.strip().encode("utf-8") for modifier in modifiers]

    attributes = list(set(attributes) - set(too_low))

    return attributes


def has_attribute(ground, vehicle):

    if type(ground) == 'instance':
        ground = ground.name
    if type(vehicle) == 'instance':
        vehicle = vehicle.name

    result = do_request(vehicle)
    attributes = find_attributes(result)

    return ground in attributes
