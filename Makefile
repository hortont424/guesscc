.PHONY: clean

LDFLAGS = -lclang

all: symbolScanner

clean:
	rm *.pyc
	rm symbolScanner