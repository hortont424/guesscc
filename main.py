#!/usr/bin/env python

from generateSymbolTable import generate_default_symbol_table, Library, Framework
from scanner import scan_source_files
from glob import glob

filenames = ["symbolScanner.c"]
filenames = glob("/Users/hortont/Desktop/particles/*.c")

symbolTable = generate_default_symbol_table()
(wantSymbols, haveSymbols) = scan_source_files(filenames)
neededLibs = set()

for symbol in wantSymbols:
    if symbol in haveSymbols:
        continue

    libsContaining = symbolTable["_" + symbol]

    if len(libsContaining) == 0:
        print "Can't find symbol '{0}'.".format(symbol)

    if len(libsContaining) > 1:
        print "Conflict for symbol '{0}':".format(symbol), libsContaining
        libnames = [lib.name for lib in libsContaining]
        #TODO: prefer Frameworks over libraries
        if "System" in libnames:
            libsContaining = set([Library("System")])
        else:
            libsContaining = set([libsContaining.pop()])
        print "Choosing:", libsContaining

    neededLibs |= libsContaining

print " ".join([lib.generate_args() for lib in neededLibs])