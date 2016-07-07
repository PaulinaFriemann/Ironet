def parse_all():

    global database
    similes = []
    ironic = dict()

    similes = []
    num = 0
    with open('../res/SimilesNoDups.txt', 'r') as f:
        for line in f:
            num += 1
            print num
            words = line.split(" ")
            ground, vehicle, irony = words[1], words[4], words[5].strip()

            simile = Simile(ground, vehicle)
            simile.initialise()
            similes.append(simile)
            ironic[simile.key] = irony == 'i'
    return similes, ironic
    #database.save()




class SimileData:
    def __init__(self):
        self.similes = []
        self.number = 0
        self.num_ironics = 0
        self.simile_frequencies = dict()
        self.ironic = dict()

    def parse_old(self):

        with open('../res/similes.txt', 'r') as f:
            for line in f:
                simile = Simile.from_line(line)
                simile.initialise()

                self.similes.append(simile)

                line = line.split(";")
                words = line[0].split(" ")
                self.ironic[simile.ground.name + ";" + simile.vehicle.name] = words[5] == 'i'

    def load_data(self):
        # f = open('../res/pdata/similes/sims.p', 'rb')
        # self.similes = pickle.load(f)
        # f.close()
        self.parse_old()

        if os.stat('../res/pdata/similes/frequenticed.p').st_size == 0:
            for simile in self.similes:
                self.simile_frequencies[simile.ground.name + ";" + simile.vehicle.name] = [simile.frequency,
                                                                                           simile.about_frequency]
            self.number = len(self.similes)

        else:
            print "??"
            f = open('../res/pdata/similes/frequenticed.p', 'rb')
            self.simile_frequencies = pickle.load(f)
            f.close()
        self.save_data()

    def get_frequencies(self):
        print len(self.similes)

        num = 0
        for simile in self.similes:
            num += len(simile.inverses)
        print " wie viele? " + str(num)

        for i, simile in enumerate(self.similes):
            for inverse in simile.inverses:
                key = inverse.ground.name + ";" + inverse.vehicle.name
                if not self.simile_frequencies.get(key):
                    inverse.determine_frequencies()
                    self.simile_frequencies[key] = [inverse.frequency, inverse.about_frequency]
                    self.save_data()
                else:
                    print str(self.simile_frequencies.get(key)) + " " + key
            print i

    def get_frequency(self, key):
        return self.simile_frequencies.get(key)

    def save_data(self):
        #print "save data thou"
        f = open('../res/pdata/similes/frequenticed.p', 'wb')
        pickle.dump(self.simile_frequencies, f)
        f.close()

        f = open('../res/pdata/similes/sims.p', 'wb')
        pickle.dump(self.similes, f)
        f.close()


###############################
#  Simile initializers        #
###############################

@classmethod
def from_phrase(cls, phrase):
    words = phrase.split(" ")
    adjective, vehicle, irony = words[1], words[4], words[5].rstrip('\n')
    return cls(adjective, vehicle, irony)


@classmethod
def from_line(cls, line):
    line = line.split(";")
    words = line[0].split(" ")
    adjective, vehicle = words[1], words[4]
    frequencies = line[1].split(" ")
    return cls(adjective, vehicle, frequencies[0], frequencies[1].rstrip("\n"))


@classmethod
def from_line_no_irony(cls, line):
    line = line.split(";")
    words = line[0].split(" ")
    adjective, vehicle = words[1], words[4]
    frequencies = line[1].split(" ")
    return cls(adjective, vehicle, irony=False, frequency=frequencies[0], about_frequency=frequencies[1].rstrip("\n"))