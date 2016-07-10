"""
Miscellaneous utils to work with text
Functions to search Wikipedia Text
"""
from data import Data
from nltk.corpus import wordnet as wn

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
    """
    reads the next k words from a file
    :param f: file to read from (opened)
    :param k: number of words to read
    :return: next k words, un a string joint with white spaces
    """

    words = ' '

    for i in range(k):
        words += next_word(f) + " "

    if words == " ":
        return ""

    return words


def add_string(words, to_add=' '):
    """
    adds a string to the beginning of every string in a list
    :param words: list of strings
    :param to_add: string to add to the strings in the list
    :return: list with to_add added to all elements
    """
    return [str(word) + to_add for word in words]


def next_word(f):
    """
    reads the next word from a file
    :param f: file to read from (opened)
    :return: next word
    """
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
    """
    looks for all codescriptors of grounds (as COLD and SNOWY as)
    """
    import sys
    sys.path.insert(1, '../')

    data = Data()

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
    """
    Gets all "as * and * as " forms from Wikipedia
    """

    with open('../res/wiki/alland.txt', 'w') as f:
        with open('E:/Documents/Workspace/wikitext.txt', 'r') as wikitext:

            word = ' '
            while word != '':
                word = next_word(wikitext)
                if word == "as ":
                    next_w = next_word(wikitext)
                    nextnext_w = next_word(wikitext)
                    if nextnext_w == "and ":

                        nextnextnext_w = next_word(wikitext)

                        if next_word(wikitext) == "as ":
                            f.write(word + next_w + nextnext_w + nextnextnext_w + "as\n")


def get_all_such():
    """
    Finds all "such as" forms in Wikipedia
    :return:
    """

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
                if word == "such ":
                    next_w = next_word(wikitext)
                    if next_w == "as ":

                        chars = last_chars(wikitext, wikitext.tell()) + next_chars(wikitext)

                        f.write(chars + "\n")


def get_attributes():
    """
    Gets all attributes for all vehicles ("GROUND * such as VEHICLE")
    """
    wd = Data()

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
                        vehicle_temp = " a " + vehicle.replace("_", " ") + " "
                        vehicle_plural = " " + vehicle.replace("_", " ") + "s "
                        vehicle_temp = vehicle_temp.replace("_", " ")
                        if vehicle_temp in right_side or vehicle_plural in right_side:

                            wd.get_vehicle(vehicle).add_attribute(wd.get_ground(ground))
                            print str(vehicle) + " " + str(ground) + "  ... " + line

    wd.save()
