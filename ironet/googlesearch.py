from proxycepion import Connection
from simile_parser import *


def main():
    #c = Connection()

    data = SimileData()
    data.parse_similes()

    #result = c.make_request("http://www.google.com", {'as_epq': "hallo"})
    #print result.content

if __name__ == '__main__':
    main()