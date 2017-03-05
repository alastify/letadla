
from time import mktime, strptime
from datetime import datetime
from datetime import timedelta


def parse_time(time_str):
    """
    Parse given time
    and return datetime object

    :type time_str: string
    :param time_str: Given string has to be like: %Y-%m-%d %H:%M:%S
    """
    struc = strptime(time_str, "%Y-%m-%d %H:%M:%S")

    return datetime.fromtimestamp(mktime(struc))


def less_then_year(a, b):
    """
    Returns True if b-a is less then a year

    :type a: datetime
    :param a: initial date
    :type b: datetime
    :param b: final date
    """
    year = timedelta(days=365)
    delta = b - a
    
    return year >= delta
