
import os
import sys


def log(text):
    """
    Print debug messages to stderr
    """
    print(">> " + text, file=sys.stderr, flush=True)


def csv_export(filename, paths):
    """
    Export founded paths as CSV

    <trip_id>;<country_code>;<source>;<destination>;<local_departure_time>;<local_arrival_time>

    :type filename: string
    :param filename: Just file name, output will be saved in output/filename

    :type paths: tuple
    :param paths: tuple data returned by finder()
    """
    fn = os.path.join("output", filename)
    log("saving paths into: {}".format(fn))
    with open(fn, mode='w') as fp:
        trip_id = 1
        for trip in paths:
            for i in range(len(trip)):
                portA, tdepA, tarrA = trip[i]
                if i + 1 < len(trip):
                    portB, tdepB, tarrB = trip[i+1]
                    fp.write("{0};{1};{2};{3};{4};{5}\n".format(
                        trip_id,
                        portA.country,
                        portA.code,
                        portB.code ,
                        tdepA.strftime("%Y-%m-%dT%H:%M"),
                        tarrA.strftime("%Y-%m-%dT%H:%M")
                    ))

            trip_id+= 1


def validate(input_filename, paths):
    log("validating output")
    with open(input_filename, mode='r') as fp:
        for trip in paths:
            for i in range(len(trip)):
                portA, tdepA, tarrA = trip[i]
                if i + 1 < len(trip):
                    portB, tdepB, tarrB = trip[i+1]
                    result = "{0};{1};{2};{3}".format(
                        portA.code,
                        portB.code ,
                        tdepA.strftime("%Y-%m-%d %H:%M:%S"),
                        tarrA.strftime("%Y-%m-%d %H:%M:%S")
                    )
                    found = False
                    fp.seek(0)
                    for row in fp:
                        if row.strip() == result:
                            found = True
                            break
                    if not found:
                        log("NOT FOUND: {}".format(result))
