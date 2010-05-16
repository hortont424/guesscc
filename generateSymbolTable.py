#!/usr/bin/env python

# nm -g -U -j -f -A -m /usr/lib/libssl.dylib

from subprocess import Popen, PIPE
from collections import defaultdict

def list_library_symbols(libraryName):
    args = ["/usr/bin/nm", "-g", "-U", "-j", "-f", "-A", "-m", libraryName]
    symbols = Popen(args, stdout=PIPE).communicate()[0].splitlines()
    symbols = [sym.split(" ") for sym in symbols]
    symbols = [sym[4] for sym in symbols if sym[3] == "external"]
    return symbols

print list_library_symbols("/usr/lib/libssl.dylib")