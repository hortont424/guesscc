#!/usr/bin/env python

import os
import magic
from subprocess import Popen, PIPE
from collections import defaultdict

ms = magic.open(magic.MAGIC_NONE)
ms.load()

def list_library_symbols(filename):
    args = ["/usr/bin/nm", "-g", "-U", "-j", "-f", "-A", "-m", filename]
    symbols = Popen(args, stdout=PIPE, stderr=PIPE).communicate()[0].splitlines()
    symbols = [sym.split(" ") for sym in symbols]
    symbols = [sym[4] for sym in symbols if sym[3] == "external"]

    return symbols

def libname_from_filename(filename):
    libname = os.path.basename(filename).split("-")[0].split(".")[0]

    if libname.startswith("lib"):
        libname = libname[3:]

    return libname

def file_is_library(filename):
    # TODO: adjust to accept elf, etc.
    if ms.file(filename).find("Mach-O") >= 0:
        return True

    return False

def generate_symbol_table(libpaths):
    symbolTable = defaultdict(set)

    for libpath in libpaths:
        for (root, subdirs, files) in os.walk(libpath):
            for file in files:
                filename = os.path.join(root, file)

                if os.path.islink(filename):
                    continue

                if not file_is_library(filename):
                    continue

                libname = libname_from_filename(filename)
                symbols = list_library_symbols(filename)

                for symbol in symbols:
                    symbolTable[symbol].add(libname)

    return symbolTable

if __name__ == "__main__":
    print generate_symbol_table(["/usr/lib", "/usr/local/lib"])
