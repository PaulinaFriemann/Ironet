import pickle

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


def get_not_done(data):

    alle = open_thing('C:/Users/Paulina/PycharmProjects/Ironet2.0/res/pdata/inverses.txt')

    done = open_thing('C:/Users/Paulina/PycharmProjects/Ironet2.0/res/pdata/invwfrequ.txt')

    not_done = []
    #not_done = open_thing(not_done, 'C:/Users/Paulina/PycharmProjects/Ironet2.0/res/pdata/invnotdone.txt')
    howmany = 0
    for simile in alle:
        if simile not in done:
            howmany += 1
            not_done.append(simile)
    print howmany
    dump(not_done, 'C:/Users/Paulina/PycharmProjects/Ironet2.0/res/pdata/invnotdone.txt')


def get_frequencies():
    inverses = open_thing('C:/Users/Paulina/PycharmProjects/Ironet2.0/res/pdata/invnotdone.txt')

    done_inverses = open_thing('C:/Users/Paulina/PycharmProjects/Ironet2.0/res/pdata/invwfrequ.txt')

    print len(inverses)
    print len(done_inverses)

    #done_inverses_names = [simile.name for simile in done_inverses]

    for inverse in inverses:
        inverse.initialise()
        done_inverses.append(inverse)
        inverses.remove(inverse)
        #inverse.initialise()
        dump(done_inverses, 'C:/Users/Paulina/PycharmProjects/Ironet2.0/res/pdata/invwfrequ.txt')
        dump(inverses, 'C:/Users/Paulina/PycharmProjects/Ironet2.0/res/pdata/invnotdone.txt')

    #dump(inverses, 'C:/Users/Paulina/PycharmProjects/Ironet2.0/res/pdata/invnotdone.txt')
    #dump(done_inverses, 'C:/Users/Paulina/PycharmProjects/Ironet2.0/res/pdata/invwfrequ.txt')


def dump(inverses, path):
    f = open(path, 'wb')
    pickle.dump(inverses, f)
    f.close()


def open_thing(path):
    f = open(path, 'rb')
    array = pickle.load(f)
    f.close()
    return array


def parse():
    from ironet.simile import Simile
    similes = []
    with open('C:/Users/Paulina/PycharmProjects/Ironet2.0/res/inversefrequsINWORK.txt', 'r') as f:
        for line in f:
            print line
            if line != "\n":
                simile = Simile.from_line_no_irony(line)
                similes.append(simile)

    dump(similes, 'C:/Users/Paulina/PycharmProjects/Ironet2.0/res/pdata/invwfrequ.txt')


