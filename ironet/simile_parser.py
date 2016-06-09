#from nltk.corpus import wordnet as wn
import sys
#from xgoogle.search import GoogleSearch, SearchError
#from IPython import embed
import time
import utils.utils as utils
import random


class SimileProperties:

    def __init__(self):
        self.frequency = 0
        self.about_frequency = 0

    def set_frequencies(self, frequency, with_frequency):
        self.frequency = frequency
        self.about_frequency = with_frequency


class Simile:

    def __init__(self, ground, vehicle, irony):
        self.ground = ground
        self.vehicle = vehicle
        self.properties = SimileProperties()

        if self.vehicle.__contains__("_"):
            self.vehicle = self.vehicle.replace("_", " ")

        self.ironic = (irony == 'i')

        self.an = (self.vehicle[0] in ['a', 'e', 'i', 'o', 'u'])

        self.synonyms = [self.ground]
        #self.get_synonyms()

    @classmethod
    def from_phrase(cls, phrase):
        words = phrase.split(" ")
        adjective, vehicle, irony = words[1], words[4], words[5].rstrip('\n')
        return cls(adjective, vehicle, irony)

    def morphological_similar(self):
        # TODO: iii) between the vehicle and an adjective that is a frequent conjoined
        # with the ground as a co-descriptor (e.g. as [cold and snowy] as snow)

        for word in self.synonyms:
            if self.vehicle in word:
                return True

        return False

    def high_web_frequ(self):
        return self.w_frequency >= 10

    def determine_such_as(self):
        self.such_as_vehicle = False

    def such_as_vehicle(self):
        return self.such_as_vehicle

    def determine_frequencies(self):
        #with open('../res/aboutfrequency.txt', 'a') as f:

        self.wo_frequency = utils.get_num_results(self.name())
        self.w_frequency = utils.get_num_results("about " + self.name())

        if self.w_frequency > self.wo_frequency:
            self.w_frequency = 0

        print str(self.wo_frequency) + " " + str(self.w_frequency)

        return str(self.wo_frequency) + " " + str(self.w_frequency) + "\n"

            #f.write(str(self.wo_frequency) + " " + str(self.w_frequency) + "\n")


    def about_predominant(self):
        return self.w_frequency > 0.5 * self.wo_frequency

    def print_simile(self):
        irony = " (ironic)" if self.ironic else " (honest)"
        print self.name() + irony

    def name(self):
        a = "an " if self.an else "a "
        return "as " + self.ground + " as " + a + self.vehicle

    def get_synonyms(self):

        # get direct synonyms
        for syns in wn.synsets(self.ground, wn.ADJ):
            for lemma in syns.lemmas():
                name = lemma.name().encode("utf-8")
                if name not in self.synonyms:
                    self.synonyms.append(name)

            # get similar words and their synonyms
            for lemma in syns.similar_tos():
                for name in lemma.lemma_names():
                    name = name.encode("utf-8")
                    if name not in self.synonyms:
                        self.synonyms.append(name)

    def set_frequencies(self, wo_frequ, w_frequ):
        self.wo_frequency = wo_frequ
        self.w_frequency = w_frequ


class SimileData:

    def __init__(self):
        self.similes = []
        self.number = 0
        self.num_ironics = 0

    def parse_similes(self):
        lines = []

        new = open('../res/nounderscores.txt', 'r')

        with open('../res/frequsunderscores.txt', 'r') as f:

            endreached = False

            for line in f:
                if not endreached:
                    asf = new.readline()
                if asf == '':

                    endreached = True
                    new.close()
                    new = open('../res/nounderscores.txt', 'a')

                if endreached:

                    simile = Simile.from_phrase(line)

                    if line.__contains__("_") or simile.an:

                        frequencies = simile.determine_frequencies()
                        bla = line.split(";")
                        line = bla[0].replace("\n", "")
                        lines.append(line + ";" + frequencies)
                        new.write(line + ";" + frequencies)

                    else:
                        new.write(line)

        new.close()



    def bs_parse(self):
        frequs = []
        with open('../res/SimilesNoDups.txt', 'r+') as f:

            with open('../res/aboutfrequency.txt', 'r+') as frequ_file:

                self.queried_similes = 0
                end_reached = False

                for line in f:
                    simile = Simile.from_phrase(line)
                    self.num_ironics += 1 if simile.ironic else 0

                    self.number += 1
                    self.similes.append(simile)

                    if not simile.vehicle.__contains__('_'):


                        if not end_reached:
                            frequencies = frequ_file.readline()
                        else:
                            frequencies = ''
                        if frequencies != '':
                            self.queried_similes += 1
                            frequencies = frequencies.replace("\n", "")
                            frequencies = frequencies.split(" ")
                            wo_frequ = int(frequencies[0])
                            w_frequ = int(frequencies[1])
                            simile.set_frequencies(wo_frequ, w_frequ)
                            frequs.append(str(wo_frequ) + " "+ str(w_frequ) + "\n")
                        else:
                            end_reached = True
                            frequs.append(simile.determine_frequencies())
                            self.queried_similes += 1

                    else:

                        simile.vehicle = simile.vehicle.replace("_", " ")
                        fr = frequs.append(simile.determine_frequencies())
                        print fr
                        self.queried_similes += 1


                        #time.sleep(random.randint(2,4))

                    #print self.queried_similes

                    if len(self.similes) == 3000:
                        break

        with open('../res/frequsunderscores.txt', 'w') as f:
            f.writelines(frequs)

    def print_all(self):
        for simile in self.similes:
            simile.print_simile()

        print str(self.number) + " ironics: " + str(self.num_ironics)
