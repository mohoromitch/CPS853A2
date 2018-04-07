#! /usr/bin/env python3
import sys
import argparse
from os import path

class ChunkWriter:
    def __init__(self, baseFilename, chunkLength):
        self.baseFilename = baseFilename
        self.chunkLength = chunkLength
        self.__nameGen = self.__nameGenerator(baseFilename)
        self.__currentFile = None
        self.__currentCount = 0

    def write(self, line):
        if self.__currentFile == None:
            self.__currentFile = open(next(self.__nameGen), 'w')
        self.__currentFile.write(line)
        self.__currentCount += 1
        if self.__currentCount >= self.chunkLength:
            self.__currentFile.close()
            self.__currentFile = open(next(self.__nameGen), 'w')
            self.__currentCount = 0

    def purge(self):
        if self.__currentFile:
            self.__currentFile.close()
            self.__currentFile = None
        self.__currentCount = 0

    def __enter__(self):
        return lambda l: self.write(l)

    def __exit__(self, type, value, traceback):
        self.purge()

    def __nameGenerator(self, baseName):
        count = 0
        while(True):
            yield '%s-%d' % (baseName, count)
            count += 1


def __main():
    parser = argparse.ArgumentParser(usage='%(prog)s <source> <size> [options...]', epilog="Like month old milk ;)", description='Text file chunker.')
    parser.add_argument('sourceFile', help='File to chunk')
    parser.add_argument('chunkSize', type=int, help='Number of lines per chunk')
    parser.add_argument('-d', default='./', help='Where to dump output files')
    parsed = parser.parse_args(sys.argv[1:])
    if not path.exists(parsed.d):
        exit('Error! %s is not a valid dir.' % parsed.d)
    chunkFile(parsed.sourceFile, parsed.chunkSize, outPath=parsed.d)

def chunkFile(filename, chunkLen, outPath='./'):
    baseName = path.join(path.abspath(outPath), path.basename(filename))
    with ChunkWriter(baseName, chunkLen) as write:
        with open(filename, 'r') as source:
            for line in source:
                write(line)

if __name__ == '__main__':
    __main()
