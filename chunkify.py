#! /usr/bin/env python3
import sys

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
    if len(sys.argv) < 3:
        print('INVALID! Ussage: %s <filename> <lines-per-chunk> [output-path]' % sys.argv[0])
    filename = sys.argv[1]
    chunkLen = int(sys.argv[2])
    chunkFile(filename, chunkLen)

def chunkFile(filename, chunkLen):
    with ChunkWriter(filename, chunkLen) as write:
        with open(filename, 'r') as source:
            for line in source:
                write(line)

if __name__ == '__main__':
    __main()
