#!/usr/bin/env python

from symbolTable import Library, Framework
from chooseLibraries import choose_libraries

#filenames = ["symbolScanner.c"]
#filenames = glob("/Users/hortont/Desktop/particles/*.c")
filenames = ["/Users/hortont/Desktop/abgr.c"]

(neededLibs, missingSymbols) = choose_libraries(filenames, debug=True)


for symbol in missingSymbols:
    print "Can't find symbol '{0}'.".format(symbol)

print " ".join([lib.generate_args() for lib in neededLibs])