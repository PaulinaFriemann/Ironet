from nltk.corpus import wordnet as wn
import requests
from bs4 import BeautifulSoup
from xgoogle.search import GoogleSearch, SearchError
from IPython import embed


def get_num_results(query):
    text = search_query(query)
    if text[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        number = text.split(" ")[0]
    else:
        number = text.split(" ")[1]
    return int(number.replace(".", ""))


def search_query(query):
    while True:

        r = requests.get('http://www.google.com/search',
                         params={'as_epq': query,
                                 "tbs": "qdr:a"}
                     )
        if str(r.url).startswith("http://ipv4.google.com/sorry/IndexRedirect?"):
            print "wtf " + r.url
            raw_input("Tell me when it is over...")
        else:
            soup = BeautifulSoup(r.text, "html.parser")
            # gets the number of search results
            return soup.find('div', {'id': 'resultStats'}).text

    # try:
    #     gs = GoogleSearch("as dumb as a brick")
    #     print gs.num_results
    #     embed()
    # except SearchError, e:
    #     print "Search failed: %s" % e


class Simile:

    def __init__(self, ground, vehicle, irony):
        self.ground = ground
        self.vehicle = vehicle
        self.w_frequency = 0
        self.wo_frequency = 0

        if irony == 'i':
            self.ironic = True
        else:
            self.ironic = False

        self.synonyms = [self.ground]
        #self.get_synonyms()

    def morphological_similar(self):
        # TODO: iii) between the vehicle and an adjective that is a frequent conjoined
        # with the ground as a co-descriptor (e.g. as [cold and snowy] as snow)

        for word in self.synonyms:
            if self.vehicle in word:
                return True

        return False

    def determine_frequencies(self):
        with open('../res/aboutfrequency.txt', 'r+') as f:

            self.wo_frequency = get_num_results(self.name())
            self.w_frequency = get_num_results("about " + self.name())

            f.writelines(str(self.wo_frequency) + " " + str(self.w_frequency))

        f.close()

    def about_predominant(self):
        return self.w_frequency > 0.5 * self.wo_frequency

    def print_simile(self):
        irony = " (ironic)" if self.ironic else " (honest)"
        print self.name() + irony

    def name(self):

        return "as " + self.ground + " as ~a " + self.vehicle

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
        with open('../res/SimilesNoDups.txt', 'r+') as f:

            with open('../res/aboutfrequency.txt', 'r+') as frequ_file:

                for line in f:
                    words = line.split(" ")
                    adjective, vehicle, irony = words[1], words[4], words[5].rstrip('\n')
                    self.num_ironics += 1 if irony == 'i' else 0
                    simile = Simile(adjective, vehicle, irony)

                    self.number += 1
                    self.similes.append(simile)

                    frequencies = frequ_file.readline()
                    if frequencies != '':
                        frequencies = frequencies.split(" ")
                        wo_frequ = int(frequencies[0])
                        w_frequ = int(frequencies[1])
                        simile.set_frequencies(wo_frequ, w_frequ)
                        print simile.name() + " " + str(wo_frequ) + " " + str(w_frequ)
                    else:
                        simile.determine_frequencies()

        frequ_file.close()
        f.close()

    def create_no_dubs(self):
        with open('../res/Similes.txt', 'r+') as f:
            with open('../res/SimilesNoDups.txt', 'r+') as f_no_dups:

                f_no_dups.truncate()

                seen = set()

                for line in f:
                    if line not in seen:

                        seen.add(line)
                        f_no_dups.write(line)

        f.close()

        f_no_dups.close()

    def print_all(self):
        for simile in self.similes:
            simile.print_simile()

        print str(self.number) + " ironics: " + str(self.num_ironics)
