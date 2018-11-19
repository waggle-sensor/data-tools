ifeq ($(uname), Linux)
	CC=gcc
	FC=gfortran
	PYC=python
else ifeq ($(uname), Darwin)
	CC=gcc-7
	FC=gfortran-7
	PYC=python
endif

ifeq (, $(shell which $(CC)))
	$(error "No $(CC) compiler found, set CC compiler variable properly")
endif

uname := $(shell uname -s)

CFLAGS = -fPIC -O3 -Wall -I.

exe = readFile.exe

ifeq ($(uname), Linux)
	shlib = libreadFile.so
else ifeq ($(uname), Darwin)
	shlib = libreadFile.dylib
endif

src = readFile.c

objects = $(src:.c=.o)

all: default libs

default: $(exe)

libs: $(shlib)

$(exe): $(objects)
	$(CC) $^ -o $@

$(shlib): $(objects)
	$(CC) -shared $^ -o $@

readFile.o: readFile.c

%.o: %.c
	$(CC) $(CFLAGS) -c $<

clean:
	rm -f $(objects)
	rm -f $(exe)
	rm -f $(shlib)

distclean: clean
