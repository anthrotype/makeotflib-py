from __future__ import (
    print_function, division, absolute_import, unicode_literals)
import sys
from . import _makeotflib as lib
from .py23 import tobytes, basestring


def main(args=None):
    if args is None:
        # if no arguments, read argument list from console
        args = sys.argv[1:]
    else:
        if isinstance(args, basestring):
            # if string, split into separate arguments
            import shlex
            args = shlex.split(args)
    # convert arguments to bytes
    args = [tobytes(a) for a in args]
    return lib.main(args)
