import sys, getopt
import os
from flyby.airports import import_csv
from flyby.output import csv_export, log, validate
from flyby.roundtrip import finder
from GeoBases import GeoBase


def main(argv):
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    INPUT_FILENAME = os.path.join(BASE_PATH, "input-data.csv")
    LEAST_TRIPS = 100
    MAX_LEVEL = 10
    OUTPUT_FILENAME = os.path.join(BASE_PATH, "output", "output.csv")

    hint = "letadla.py -i <inputfile> -t <least trips to find> -l <max recursion>"
    try:
        opts, args = getopt.getopt(argv, "hi:t:l:",)
    except getopt.GetoptError:
        print(hint)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(hint)
            sys.exit()
        elif opt == "-i":
            INPUT_FILENAME = arg
        elif opt == "-t":
            LEAST_TRIPS = int(arg)
        elif opt == "-l":
            MAX_LEVEL = int(arg)

    log("geobase init")
    # TODO: more actual data https://github.com/opentraveldata/opentraveldata/find/master
    geo_a = GeoBase(data='ori_por', verbose=False)
    grid = import_csv(filename=INPUT_FILENAME, geo_a=geo_a)
    paths = finder(grid, least_trips=LEAST_TRIPS, max_level=MAX_LEVEL)
    validate(INPUT_FILENAME, paths)
    csv_export(filename=OUTPUT_FILENAME, paths=paths)


if  __name__ == '__main__':
    main(sys.argv[1:])
