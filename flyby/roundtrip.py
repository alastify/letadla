
from .output import log
from .airports import Airports
from .timemachine import less_then_year

from datetime import datetime
from threading import Thread


MAX_LEVEL = 10


class Hiker(Thread):
    """
    Worker class for some concurrency
    """
    def __init__(self, source_port, trip, roundtrips):
        """
        Constructor

        :type source_port: Port
        :param source_port: Port object

        :type trip: list
        :param trip: Stores trip information during recursion

        :type roundtrips: list
        :param roundtrips: Stores information of all valid trips
        """
        super().__init__(group=None, target=None, name=None, daemon=None)
        self.source_port = source_port
        self.trip = trip
        self.roundtrips = roundtrips

    def run(self):
        """
        Thread run method - this is where the stuff is happening
        """
        hiker(
            source_port=self.source_port,
            trip=self.trip,
            roundtrips=self.roundtrips
        )


def find_duplicate(trip):
    """
    Returns True if duplicate airport is found within the trip

    :type trip: tuple
    :param trip: (port, departure_at, arrival_at)
    """
    codes = []
    countries = []
    for port_tuple in trip:
        if port_tuple is not None:
            if port_tuple[0].code in codes:
                return True
            else:
                codes.append(port_tuple[0].code)
            if port_tuple[0].country in countries:
                return True
            else:
                countries.append(port_tuple[0].country)

    return False


def hiker(source_port, trip, roundtrips, level=0, departure_at=None, arrival_at=None):
    """
    Recursive function to find path within specified parameters
    (max hops, max time)

    :type source_port: Port
    :param source_port: Port object

    :type trip: tuple
    :param trip: Stores trip information during recursion

    :type roundtrips: list
    :param roundtrips: Stores information of all valid trips

    :type level: integer
    :param level: Depth of recurions

    :type departure_at: datetime
    :param departure_at: Time of departure

    :type arrival_at: datetime
    :param arrival_at: Time of arrival

    """
    trip[level] = (source_port, departure_at, arrival_at)

    # max time check
    if level > 0 and not less_then_year(trip[0][1], trip[level][2]):
        trip[level] = None
        return

    # max level check
    if level == MAX_LEVEL:
        if source_port.code == trip[0][0].code:
            roundtrips.append(trip.copy())
        return
    else:
        if find_duplicate(trip):
            trip[level] = None
            return

    # schedule traverse
    for dst in source_port.schedule:
        if level > 0:

            # throw away those, when arrival time is higher than departure time
            if arrival_at > dst.departure_at:
                continue

        trip[level] = (source_port, dst.departure_at, dst.arrival_at)

        hiker(
            source_port=dst.destination_port,
            trip=trip,
            level=level+1,
            roundtrips=roundtrips,
            departure_at=dst.departure_at,
            arrival_at=dst.arrival_at
        )

    return


def finder(grid, max_level=10, max_threads=1, least_trips=None):
    """
    Performe recursive search

    :type grid: Airports
    :param grid: Airpots data object

    :type max_level: integer
    :param max_level: Maximum depth of recursive search

    :type max_threads: integer
    :param max_threads: Maximum concurrent threads

    :type least_trips: integer
    :param least_trips: The least trips to find
    """
    global MAX_LEVEL
    MAX_LEVEL = max_level

    log("executing finder ({} threads)".format(max_threads))
    timer_in = datetime.now()

    roundtrips = []
    blank_trip = []
    for t in range(MAX_LEVEL+1):
        blank_trip.append(None)

    if max_threads == 1:
        for port in grid.data:
            hiker(source_port=port, trip=blank_trip.copy(), roundtrips=roundtrips)
            if least_trips is not None:
                if len(roundtrips) >= least_trips:
                    break
    else:
        # TODO: useless, remove
        pool = []
        for port in grid.data:
            while len(pool) == max_threads:
                for i in range(len(pool)):
                    pool[i].join(0.1)
                    if not pool[i].isAlive():
                        pool.pop(i)
                        break

            t = Hiker(source_port=port, trip=blank_trip.copy(), roundtrips=roundtrips)
            t.setDaemon(True)
            t.start()
            pool.append(t)

            if least_trips is not None:
                if len(roundtrips) >= least_trips:
                    break

        # clean up
        for t in pool:
            t.join()

    log("found: {}".format(len(roundtrips)))
    log("time elapse: {}".format(datetime.now() - timer_in))

    return roundtrips
