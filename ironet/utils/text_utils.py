import pickle
import os
#from ironet.words import *
from nltk.corpus import wordnet as wn
from words import *

bytes_processed = 0
gb_processed = 0


def peek_line(f, k=10):
    """
    gives the next line / k words and sets the pointer back
    """
    pos = f.tell()
    line = get_k_words(f, k)
    f.seek(pos)
    return line


def get_k_words(f, k=10):
    global bytes_processed
    global gb_processed

    num_space = 0
    words = ' '

    while num_space < k:
        char = f.read(1)
        bytes_processed += 1
        words += char
        if char == ' ':
            num_space += 1

    if bytes_processed >= 1073741824:
        bytes_processed = 0
        gb_processed += 1
        print gb_processed

    if words == " ":
        return ""

    return " ".join(words.split())


def add_string(words, to_add=' '):
    return [str(word) + to_add for word in words]


def get_all_synonyms():
    """
    gets all synonyms for ALL grounds and vehicles
    :return: arrays with grounds and vehicles including synonyms
    """

    from ironet.simile import Simile

    grounds = []
    vehicles = []
    with open('../../res/SimilesNoDups.txt', 'r') as similes:
        for line in similes:
            simile = Simile.from_phrase(line)
            simile.find_synonyms()

            for ground in simile.ground_synonyms:
                if ground not in grounds:
                    grounds.append(ground)
            for vehicle in simile.vehicle_synonyms:
                if vehicle not in vehicles:
                    vehicles.append(vehicle)

    p_grounds = open('../../res/pdata/grounds.txt')
    p_vehicles = open('../../res/pdata/vehicles.txt')

    pickle.dump(grounds, p_grounds)
    pickle.dump(vehicles, p_vehicles)

    p_grounds.close()
    p_vehicles.close()

    return grounds, vehicles


def next_word(f):
    global bytes_processed
    global gb_processed

    word = ''
    next_char = 'dummy'

    while next_char != ' ' and next_char != '':
        next_char = f.read(1)
        bytes_processed += 1
        word += next_char

    if bytes_processed >= 1073741824:
        bytes_processed = 0
        gb_processed += 1
        print gb_processed

    return word


def get_codescriptors():
    import sys
    sys.path.insert(1, '../')

    import ironet.words

    data = ironet.words.WordDatabase()

    with open('../res/wiki/alland.txt', 'r') as f:
        for line in f:
            words = line.split(" ")
            for ground in data.grounds.keys():
                other = ""
                if words[1] == ground:
                    other = words[3]

                elif words[3] == ground:
                    other = words[1]

                if wn.synsets(other, wn.ADJ):
                    print "adj " + other
                    g = data.get_ground(ground)
                    g.add_codescriptor(other)
                elif other != "":
                    print "no adj " + other
    data.save()


def get_ground_and():

    with open('../res/wiki/alland.txt', 'w') as f:
        with open('E:/Documents/Workspace/wikitext.txt', 'r') as wikitext:

            word = ' '
            last_word = ''
            while word != '':
                word = next_word(wikitext)
                # print word
                if word == "as ":
                    next_w = next_word(wikitext)
                    nextnext_w = next_word(wikitext)
                    if nextnext_w == "and ":

                        nextnextnext_w = next_word(wikitext)

                        if next_word(wikitext) == "as ":
                            #print word + next_w + nextnext_w + nextnextnext_w + "as "
                            f.write(word + next_w + nextnext_w + nextnextnext_w + "as\n")


def get_all_such():

    def last_chars(f, pos):
        try:
            f.seek(pos - 35)
        except IOError, e:
            print pos
            print "IOERROR" + " " + str(e)
            f.seek(0)
        chars = ""
        while f.tell() != pos:
            chars += f.read(1)
        return chars

    def next_chars(f):
        words = " "
        for i in range(6):
            words += next_word(f)
        return words

    with open('../res/wiki/allsuchas.txt', 'w') as f:
        with open('E:/Documents/Workspace/wikitext.txt', 'r') as wikitext:

            word = ' '

            while word != '':
                word = next_word(wikitext)
                #print word
                if word == "such ":
                    next_w = next_word(wikitext)
                    if next_w == "as ":
                        #print "sSZCHG ASSS!!!"

                        chars = last_chars(wikitext, wikitext.tell()) + next_chars(wikitext)

                        f.write(chars + "\n")


def all_such_as():
    """
    looks for ALL such - as formations in Wikipedia
    and writes them to a file
    """

    with open('../../res/wiki/allsuchas.txt', 'w') as f:

        with open('E:/Documents/Workspace/wikitext.txt', 'r') as wikitext:

            lastline = []
            line = 'dummy'

            while line != '':

                line = get_k_words(wikitext)

                if line.__contains__(" such as "):
                    words = line.split(" ")
                    idx = words.index("such")
                    # if there is another "such" in the line
                    while words[idx + 1] != "as":

                        idx = words.index("such", idx+1)

                    words_w_space = add_string(words)

                    if 3 <= idx < len(words) - 3:

                        to_write = words_w_space[idx - 3:idx + 5] + ["\n"]

                        f.writelines(to_write)

                    elif idx < 3:
                        missingwords = 3 - idx
                        try:
                            words_last_line = lastline[-missingwords:]
                        except IndexError:
                            continue
                        else:
                            words_last_line = add_string(words_last_line)

                            to_write = words_last_line + words_w_space[:idx + 5] + ["\n"]

                            f.writelines(to_write)

                    elif idx >= len(words) - 3:

                        missingwords = idx - (len(words) - 4)

                        nextline = peek_line(wikitext).split(" ")

                        words_next_line = nextline[:missingwords+1]

                        with_space_next = add_string(words_next_line)

                        to_write = words_w_space[idx - 3:] + with_space_next + ["\n"]

                        f.writelines(to_write)

                lastline = line.split(" ")[:-1]


def get_attributes():
    wd = WordDatabase()

    for vehicle in wd.vehicles.keys():
        if not wn.synsets(vehicle, wn.NOUN):
            del wd.vehicles[vehicle]

    for ground in wd.grounds.keys():
        if not wn.synsets(ground, wn.ADJ):
            del wd.grounds[ground]

    with open('../res/wiki/allsuchas.txt', 'r') as f:

        for line in f:
            split_line = line.split(" such as ")
            left_side = split_line[0]
            right_side = split_line[1]

            for ground in wd.grounds.keys():
                ground_temp = " " + ground + " "
                if ground_temp.replace("_", " ") in left_side:
                    for vehicle in wd.vehicles.keys():
                        vehicle_temp = " " + vehicle + " "
                        if vehicle_temp.replace("_", " ") in right_side:

                            wd.get_vehicle(vehicle).add_attribute(wd.get_ground(ground))
                            print str(vehicle) + " " + str(ground) + "  ... " + line


    wd.save()


def ground_such_as_vehicle():
    """
    checks if something like "GROUND * such as * VEHICLE" is in wikipedia and writes lines to file
    for ALL grounds and vehicles and synonyms
    """
    grounds, vehicles = get_all_synonyms()

    with open('../../res/wiki/groundsavehicleALL.txt', 'w') as to_write:

        with open('../../res/wiki/allsuchas.txt', 'r') as f:
            for line in f:
                split_line = line.split(" ")
                leftside = split_line[:4]
                rightside = split_line[4:]
                if any(ground in leftside for ground in grounds) and any(vehicle in rightside for vehicle in vehicles):
                    to_write.write(line)


def get_all_co_descriptors():
    # TODO ground as a co-descriptor (e.g. as [cold and snowy] as snow)
    pass


def such_as(simile):

    grounds = simile.ground_synonyms
    vehicles = simile.vehicle_synonyms
    try:
        for vehicle in vehicles:
            if vehicle.__contains__("_"):
                vehicle = " ".join(vehicle.split("_"))
    except TypeError:
        print simile.name
        raise

    with open('../res/wiki/groundsavehicleALL.txt', 'r') as f:

        for line in f:
            words = line.split(" ")
            leftside, rightside = words[:3], words[4:]

            if any(ground in leftside for ground in grounds) and any(vehicle in rightside for vehicle in vehicles):
                return True
    return False


def pickle_inverses(data):
    inverses = []
    for simile in data.similes:
        if simile.inverse not in inverses:
            inverses.append(simile.inverse)

    f = open('C:/Users/Paulina/PycharmProjects/Ironet2.0/res/pdata/inverses.txt', 'wb')
    pickle.dump(inverses, f)
    f.close()


def dump(inverses, path):
    f = open(path, 'wb')
    pickle.dump(inverses, f)
    f.close()


def open_thing(path):
    f = open(path, 'rb')
    array = pickle.load(f)
    f.close()
    return array



