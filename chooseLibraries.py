#!/usr/bin/env python

from symbolTable import load_symbol_table, Library, Framework
from scanner import scan_source_files
from glob import glob

def choose_libraries(filenames, debug=False):
    symbolTable = load_symbol_table()
    (wantSymbols, haveSymbols) = scan_source_files(filenames)
    neededLibs = set()
    missingSymbols = set()

    for symbol in wantSymbols:
        if symbol in haveSymbols:
            continue

        libsContaining = symbolTable["_" + symbol]

        if len(libsContaining) == 0:
            missingSymbols.add(symbol)

        if len(libsContaining) > 1:
            for lib in libsContaining:
                if lib.name == "System" or isinstance(lib, Framework):
                    libsContaining = set([lib])
                    break

            if len(libsContaining) > 1:
                libsContaining = set([libsContaining.pop()])

            if debug:
                print "Conflict for symbol '{0}':".format(symbol), libsContaining
                print "Choosing:", libsContaining

        if debug:
            print symbol, neededLibs

        neededLibs |= libsContaining

    return (neededLibs, missingSymbols)