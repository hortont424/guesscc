#!/usr/bin/env python

import os
import sys
from symbolTable import Library, Framework
from chooseLibraries import choose_libraries

filenames = sys.argv[1:]

(neededLibs, missingSymbols) = choose_libraries(filenames)

for symbol in missingSymbols:
    print "Can't find symbol '{0}'.".format(symbol)

compilercmd = "gcc "
compilercmd += " ".join([lib.generate_args() for lib in neededLibs]) + " "
compilercmd += " ".join(filenames)

print compilercmd
os.system(compilercmd)