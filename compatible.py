""" This file contains python 2 and 3 compatible code
examples.

Execute with "python compatible.py -v"
"""
from __future__ import (
    print_function,
    division,
    unicode_literals,
    absolute_import,
)


def doc_test_example(n):
    """ Sample doctest comment

    >>> doc_test_example('abc')
    'abc'
    """
    return n


def print_example():
    """ Print text to the screen

    >>> print_example()
    Hello World
    """
    print('Hello', 'World')


def exception_example():
    """ Throw a basic exception

    >>> exception_example()
    Traceback (most recent call last):
    ValueError: exceptional
    """
    raise ValueError('exceptional')


def exception_traceback_example():
    """ Throw an exception with traceback

    >>> exception_traceback_example()
    Traceback (most recent call last):
    ValueError: exceptional
    """
    from future.utils import raise_with_traceback
    raise_with_traceback(ValueError('exceptional'))


def exception_chain_example():
    """ Chain exceptions together

    >>> exception_chain_example() #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: chained
    """
    from future.utils import raise_from
    try:
        raise ValueError('cause')
    except ValueError as e:
        raise_from(ValueError('chained'), e)


def division_example(numerator, denominator):
    """ Floating point division

    >>> division_example(3,2)
    1.5
    >>> division_example(3,0)
    Traceback (most recent call last):
    ZeroDivisionError: division by zero
    """
    return numerator / denominator


def byte_loop_example():
    """ Loop through array of bytes

    >>> byte_loop_example() is None
    True
    """
    from builtins import bytes, chr
    for myint in bytes(b'byte-string with high-bit chars like \xf9'):
        char = chr(myint)    # returns a unicode string
        bytechar = char.encode('latin-1')


def test_if_int_example(x):
    """ Tests if a value is an integer, int was converted
    to long in Python 3

    >>> test_if_int_example(1)
    True
    >>> test_if_int_example(9223372036854775808)
    True
    """
    from builtins import int

    return isinstance(x, int)

def dict_loop_example(d):
    from future.utils import viewitems
    for (key, value) in viewitems(d):
      print(key,value)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
