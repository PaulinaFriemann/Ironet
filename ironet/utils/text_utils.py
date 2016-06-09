from tqdm import tqdm

bytes_processed = 0
gb_processed = 0

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


def clear_false_resultstats(file):
    lines = []
    with open(file, 'r+') as f:
        for line in f:
            frequencies = line.replace("\n", "")
            frequencies = line.split(" ")
            wo_frequ = int(frequencies[0])
            w_frequ = int(frequencies[1])

            if w_frequ > wo_frequ:
                lines.append(str(wo_frequ) + " 0\n")
            else:
                lines.append(str(wo_frequ) + " " + str(w_frequ) + "\n")

    with open(file, 'w') as f:
        f.writelines(lines)


def do_append_shit(file, file2):
    lines = []
    frequencies = open(file2, 'r')

    with open(file, 'r') as f:

        num = 0

        for line in f:
            frequ = frequencies.readline()
            line = line.replace("\n", "")
            print frequ
            print line
            num+=1

            lines.append(line + ";" + frequ)

            if num == 3000:
                break


    with open('../../res/frequsunderscores.txt', 'w') as f:
        f.writelines(lines)


def add_spaces(words):
    return [word + " " for word in words]


def peek_line(f):
    pos = f.tell()
    line = get_k_words(f)
    f.seek(pos)
    return line


def get_k_words(f):

    global bytes_processed
    global gb_processed

    num_space = 0
    words = ' '

    while num_space < 10:
        char = f.read(1)
        bytes_processed += 1
        words += char
        if char == ' ':
            num_space += 1

    if bytes_processed >= 1073741824:
        bytes_processed = 0
        gb_processed += 1
        print gb_processed

    return " ".join(words.split())


def such_as():

    f = open('../../res/suchas.txt', 'w')


    with open('E:/Documents/Workspace/wikitext.txt', 'r') as wikitext:

        lastline = []
        line = 'bla'

        while line != '':

            line = get_k_words(wikitext)
            #print "process line"
            #print line

            if line.__contains__(" such as "):
                words = line.split(" ")
                idx = words.index("such")
                #if there is another "such" in the line
                while words[idx + 1] != "as":

                    idx = words.index("such", idx+1)

                words_w_space = add_spaces(words)

                if 3 <= idx < len(words) - 3:

                    to_write = words_w_space[idx - 3:idx + 4] + ["\n"]

                    #print "passt " + str(to_write)

                    f.writelines(to_write)

                elif idx < 3:
                    missingwords = 3 - idx
                    try:
                        words_last_line = lastline[-missingwords:]
                    except IndexError:
                        continue
                    else:
                        #print "we are in else!!!"
                        words_last_line = add_spaces(words_last_line)

                        to_write = words_last_line + words_w_space[:idx + 4] + ["\n"]

                        #print "idx zu klein " + str(to_write)

                        f.writelines(to_write)

                elif idx >= len(words) - 3:

                    missingwords = idx - (len(words) - 4)

                    nextline = peek_line(wikitext).split(" ")
                    #print "netxt line " + str(nextline)

                    words_next_line = nextline[:missingwords]

                    #print "miising words " + str(missingwords)
                    #print words_next_line

                    with_space_next = add_spaces(words_next_line)

                    to_write = words_w_space[idx - 3:] + with_space_next + ["\n"]

                    #print "idx zu gross " + str(to_write)

                    f.writelines(to_write)

            lastline = line.split(" ")[:-1]
            #print lastline
    f.close()



def main():
    #do_append_shit('../../res/backupsimiles.txt', '../../res/aboutfrequency.txt')
    such_as()


if __name__ == '__main__':
    main()
