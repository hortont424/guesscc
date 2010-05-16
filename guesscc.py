#!/usr/bin/env python

import os
from symbolTable import Library, Framework
from chooseLibraries import choose_libraries

#filenames = ["symbolScanner.c"]
#filenames = glob("/Users/hortont/Desktop/particles/*.c")
filenames = ["/Users/hortont/Desktop/abgr.c"]

(neededLibs, missingSymbols) = choose_libraries(filenames)

compilercmd = "gcc "
compilercmd += " ".join([lib.generate_args() for lib in neededLibs]) + " "
compilercmd += " ".join(filenames)

os.system(compilercmd)