#!/usr/bin/env python

import os
import magic
from subprocess import Popen, PIPE
from collections import defaultdict
from glob import glob

ms = magic.open(magic.MAGIC_NONE)
ms.load()

class SymbolSource(object):
    def __init__(self, name):
        super(SymbolSource, self).__init__()
        self.name = name

    def __hash__(self):
        return self.name.__hash__()

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return  "{0}({1})".format(type(self).__name__, self.name)

class Library(SymbolSource):
    def __init__(self, name):
        super(Library, self).__init__(name)

class Framework(SymbolSource):
    def __init__(self, name):
        super(Framework, self).__init__(name)

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

def generate_symbol_table(libpaths, frameworkpaths):
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
                    symbolTable[symbol].add(Library(libname))

    for frameworkpath in frameworkpaths:
        for filename in glob(os.path.join(frameworkpath, "*.framework")):
            (frameworkname, extension) = os.path.splitext(os.path.basename(filename))
            libfilename = os.path.join(filename, "Versions", "Current", frameworkname)

            if not file_is_library(libfilename):
                continue

            symbols = list_library_symbols(libfilename)

            for symbol in symbols:
                symbolTable[symbol].add(Framework(frameworkname))

    return symbolTable

def generate_default_symbol_table():
    libpaths = ["/usr/lib", "/usr/local/lib"]
    frameworkpaths = ["/System/Library/Frameworks", "/Library/Frameworks",
        os.path.expanduser("~/Library/Frameworks")]

    return generate_symbol_table(libpaths, frameworkpaths)

if __name__ == "__main__":
    print generate_default_symbol_table()
