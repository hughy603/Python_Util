from __future__ import (
    print_function,
    # division,
    unicode_literals,
    absolute_import,
)
from builtins import bytes
from future.utils import viewitems
from itertools import zip_longest
import re


def to_str(bytes_or_str):
    """ Convert bytes or a string into a string

    >>> to_str('abc') == 'abc'
    True
    >>> to_str(b'abc') == 'abc'
    True
    """
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str

    return value


def validate_dol(dol):
    """ Returns nothing if data is a dictionary of lists
    throws an exception if it is not

    >>> validate_dol({'abc':[1,2,3]}) is None
    True
    >>> validate_dol({'abc':(1,2,3)}) is None
    True
    >>> validate_dol({12:(1,2,3)}) is None
    True
    >>> validate_dol({'abc':12}) is None
    Traceback (most recent call last):
    ValueError: All values must be a tuple or list
    >>> validate_dol({'abc':{1:None}}) is None
    Traceback (most recent call last):
    ValueError: All values must be a tuple or list
    """
    if not (isinstance(dol, dict)):
        raise ValueError("Input is not a dictionary")

    for key, value in viewitems(dol):
        if not (isinstance(value, list) or isinstance(value, tuple)):
            raise ValueError("All values must be a tuple or list")


def dol_to_2d(dol, fillvalue=None):
    """ Converts a dictionary of lists into a 2D array.
    This is useful for writing a dictionary to a CSV. The
    keys are the first row and there values follow.  If
    one key has more values than another, N
x
    >>> from collections import OrderedDict
    >>> d = {'abc':[1,2,3],'d':[4], 'e':[5,6]}
    >>> x = dol_to_2d(OrderedDict(sorted(d.items(), key=lambda t: t[0])))
    >>> [x[0]] + list(x[1])
    [('abc', 'd', 'e'), (1, 4, 5), (2, None, 6), (3, None, None)]
    >>> dol_to_2d({'abc':12}) is None
    Traceback (most recent call last):
    ValueError: All values must be a tuple or list
    """
    validate_dol(dol)
    table = [tuple(dol.keys())]
    table.append(zip_longest(*dol.values(),
                             fillvalue=fillvalue))
    return table


def clean_2d_csv(csv_data):
    """ Removes all , \n and \r characters from data being
    loaded to a csv

    TODO TODO TODO ValueError: line 8 of the docstring for __main__.clean_2d_csv has inconsistent leading whitespace: "1']])"

    >>> clean_2d_csv([['1','2','3']])
    [['1', '2', '3']]
    >>> clean_2d_csv([['1','2','3\n1']])
    [['1', '2', '31']]
    >>> clean_2d_csv([1,2,3])
    [[1,2,3]]
    """
    cleaner = re.compile(r'(,|\n|\r)')
    for sublist in csv_data:
        for el in sublist:
            el = cleaner.sub('', el)
    return csv_data


def dol_to_csv(dol, output_file):
    csv_data = dol_to_2d(dol)
    print(csv_data)
    cleaned_csv_data = clean_2d_csv(csv_data)
    print(cleaned_csv_data)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
