from ._makeotflib_cffi import ffi, lib
import sys
from fontTools.misc.py23 import tobytes, basestring


def makeotfexe(args=None):
    if args is None:
        args = sys.argv[1:]
    else:
        if isinstance(args, basestring):
            import shlex
            args = shlex.split(args)
    progname = ffi.new("char[]", b"makeotflib")
    argv = [progname]
    for arg in args:
        argv.append(ffi.new("char[]", tobytes(arg)))
    argc = len(argv)
    return lib.main(argc, argv)
