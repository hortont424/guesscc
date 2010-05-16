#!/usr/bin/env python

from ctypes import *

clang = CDLL("libclang.dylib") # TODO: generalize extension

VISITFUNC = CFUNCTYPE(c_uint, c_void_p, c_void_p, c_void_p)

# define argument and return types for the few clang functions we need
clang.clang_createIndex.restype = c_void_p
clang.clang_createIndex.argtypes = [c_int, c_int]

clang.clang_createTranslationUnitFromSourceFile.restype = c_void_p
clang.clang_createTranslationUnitFromSourceFile.argtypes = [c_void_p, c_char_p, c_int, c_void_p, c_int, c_void_p]

clang.clang_getTranslationUnitCursor.restype = c_void_p
clang.clang_getTranslationUnitCursor.argtypes = [c_void_p]

clang.clang_visitChildren.restype = c_uint
clang.clang_visitChildren.argtypes = [c_void_p, VISITFUNC, c_void_p]

def found_child(cursor, parent, client_data):
    print "hi"

c_found_child = VISITFUNC(found_child)

filename = c_char_p("symbolScanner.c")
idx = clang.clang_createIndex(1, 0)
tu = clang.clang_createTranslationUnitFromSourceFile(idx, filename, 0, None, 0, None)
cur = clang.clang_getTranslationUnitCursor(tu)
clang.clang_visitChildren(cur, c_found_child, None)