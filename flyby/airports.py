
import os
from csv import reader
from .output import log
from .timemachine import parse_time
import math


class Schedule:
    """
    Direct trip information
    """
    def __init__(self, departure_at, arrival_at, destination_port):
        """
        Constructor

        :type departure_at: datetime
        :param departure_at: Time of departure

        :type arrival_at: datetime
        :param arrival_at: Time of arrival

        :type destination_port: Port
        :param destination_port: Port object
        """
        self.departure_at = departure_at
        self.arrival_at = arrival_at
        self.destination_port = destination_port


class Port:
    """
    Airport basic information and destination schedule
    """
    def __init__(self):
        """
        Constructor
        """
        self.name = ""
        self.code = ""
        self.country = ""
        self.schedule = []

    def __str__(self):
        return self.code

    def add_schedule(self, schedule):
        """
        Attach new destination from this airport to another airport

        :type schedule: Schedule
        :param schedule: Schedule object which contains trip information
        """
        self.schedule.append(schedule)


class Airports:
    """
    Wrapper for data about all the airports and its schedule

    """

    def __init__(self, geo_a, total_estimation):
        """
        Constructor

        :type geo_a: GeoBase
        :param geo_a: Information about airports

        :type total_estimation: integer
        :param total_estimation: Estimation of total airports
        """
        self.data = []
        self.total_estimation = total_estimation
        self.geo_a = geo_a

    def get_port_by_code(self, code, return_default=True):
        """
        Returns Port object if already exists,
          or create new if return_default is True
          or return None

          :type code: string
          :param code: IATA code of Airport

          :type return_default: boolean
          :param return_default: If set, returns new Port object
        """
        for port in self.data:
            if port.code == code:
                return port

        if return_default:
            ainfo = "XXX"
            if self.geo_a is not None:
                ainfo = self.geo_a.get(code, 'name', default="EMPTY")

            if ainfo == "EMPTY":
                log("  NOTICE airport {} has not been found!".format(code))
                return None
            else:
                port = Port()
                port.name = ainfo
                port.code = code
                if self.geo_a is not None:
                    port.country = self.geo_a.get(code, 'country_code')
                self.data.append(port)
                return port

        return None

    def add_from_csv(self, source, destination, departure_at, arrival_at):
        """
        Append airport data from CSV

        :type source: string
        :param source: Airport iata code

        :type destination: string
        :param destination: Airport iata code

        :type departure_at: string
        :param departure_at: Time of departure as a string

        :type arrival_at: string
        :param arrival_at: Time of arrival as a string
        """
        source_port = self.get_port_by_code(source)
        destination_port = self.get_port_by_code(destination)

        if source_port and destination_port:
            source_port.add_schedule(
                Schedule(
                    departure_at=parse_time(departure_at),
                    arrival_at=parse_time(arrival_at),
                    destination_port=destination_port
                )
            )


def import_csv(filename, geo_a):
    """
    Import given CSV file

    :type filename: string
    :param filename: File name

    :type geo_a: GeoBase
    :param geo_a: GeoBase object
    """
    if os.path.exists(filename) and os.path.isfile(filename):
        log("enumerating")
        num_lines = sum(1 for line in open(filename))
        log("total: {}".format(num_lines))
        ap = Airports(geo_a=geo_a, total_estimation=num_lines)
        with open(filename, mode='r') as fp:
            csv = reader(fp, delimiter=';')
            log("parsing")
            i = 1
            step = 5

            for line in csv:
                if len(line) == 4:
                    if line[0] == "source":
                        continue
                    percent = int((i/num_lines)*100)
                    if percent > step:
                        log("  {}%".format(percent))
                        step+= 5
                    ap.add_from_csv(source=line[0], destination=line[1], departure_at=line[2], arrival_at=line[3])
                else:
                    log("Ignoring line: {}, bad format!".format(i))
                i+= 1
            log("done")
        return ap
    else:
        raise RuntimeError(filename + " not found!")

    return None
