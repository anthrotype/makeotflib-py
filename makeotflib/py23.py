from __future__ import (
    print_function, division, absolute_import, unicode_literals)


try:
    basestring = basestring
except NameError:
    basestring = str


def tobytes(s, encoding='ascii', errors='strict'):
    if not isinstance(s, bytes):
        return s.encode(encoding, errors)
    else:
        return s
