
.PHONY: all

all: libmeanshift.so Meanshift.dll

CXX=/usr/bin/g++
MINGW_CXX=/usr/bin/x86_64-w64-mingw32-g++
SRC=histogram.cpp histogram.h

libmeanshift.so: ${SRC}
	${CXX} -o $@ -fPIC --shared $<

Meanshift.dll: ${SRC}
	${MINGW_CXX} -o $@ -fPIC --shared $<

