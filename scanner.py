#!/usr/bin/env python

from subprocess import Popen, PIPE

def scan_source_file(filename):
    args = ["./symbolScanner", filename]
    scan = Popen(args, stdout=PIPE, stderr=PIPE).communicate()[0].splitlines()

    wantSymbols = set()
    haveSymbols = set()

    for sym in scan:
        if sym[1:].startswith("__builtin") or sym[1:].startswith("__inline"):
            continue
        elif sym[0] == "+":
            haveSymbols.add(sym[1:])
        elif sym[0] == "-":
            wantSymbols.add(sym[1:])

    return (wantSymbols, haveSymbols)

def scan_source_files(filenames):
    wantSymbols = set()
    haveSymbols = set()

    for filename in filenames:
        (want, have) = scan_source_file(filename)
        wantSymbols |= want
        haveSymbols |= have

    return (wantSymbols, haveSymbols)