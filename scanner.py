#!/usr/bin/env python

from subprocess import Popen, PIPE

def scan_source_file(filename):
    args = ["./symbolScanner", filename]
    symbols = Popen(args, stdout=PIPE, stderr=PIPE).communicate()[0].splitlines()
    return set(symbols)