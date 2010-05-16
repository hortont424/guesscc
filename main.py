#!/usr/bin/env python

from generateSymbolTable import generate_default_symbol_table
from scanner import scan_source_file

filename = "symbolScanner.c"
filename = "/Users/hortont/src/particles/Libraries/libcomputer/COBuffer.c"

symbolTable = generate_default_symbol_table()
neededLibs = set()

for symbol in scan_source_file(filename):
    if symbol.startswith("__builtin"):
        continue

    libsContaining = symbolTable["_" + symbol]

    if len(libsContaining) == 0:
        print "Can't find symbol '{0}'.".format(symbol)

    neededLibs |= libsContaining

print neededLibs