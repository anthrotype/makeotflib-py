from makeotflib import makeotfexe
import sys


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    return makeotfexe(args)


if __name__ == "__main__":
    main()
