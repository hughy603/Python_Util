from __future__ import (
    print_function,
    division,
    unicode_literals,
    absolute_import,
)
from builtins import bytes
from future.utils import viewitems
from six import iteritems


def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str

    return value


def validate_dict_of_lists(data):
    """ Returns nothing if data is a dictionary of lists
    throws an exception if it is not

    >>> validate_dict_of_lists({'abc':[1,2,3]}) is None
    True
    """
    if not (isinstance(data, dict)):
        raise ValueError("Input is not a dictionary")

    for key, value in viewitems(data):
        if not (isinstance(key, str) or isinstance(key, bytes)):
            raise ValueError("Got a key of type " +
                             type(key) + "Only strings are supported")
        if not (isinstance(value, list) or isinstance(value, tuple)):
            raise ValueError("All values must be iterable")


def dict_to_flat_csv(data):
    validate_dict_of_lists(data)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
