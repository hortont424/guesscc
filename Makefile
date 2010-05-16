.PHONY: clean

LDFLAGS = -lclang

all: symbolScanner symbolTable.dat

clean:
	rm -f *.pyc
	rm -f symbolScanner

symbolTable.dat: symbolTable.py
	./symbolTable.py