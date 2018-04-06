import sys

# Takes the form $chunkify <filename> <lines-per-chunk>


def __main():
    if len(sys.argv) < 3:
        print('INVALID! Ussage: %s <filename> <lines-per-chunk> [output-path]' % sys.argv[0])
    filename = sys.argv[1]
    chunkLen = int(sys.argv[2])
    chunkFile(filename, chunkLen)

def chunkFile(filename, chunkLen):
    nameGenerator = __nameGenerator(filename)
    with open(filename, 'r') as source:
        lineCount = 0
        cFile = open(next(nameGenerator), 'w')
        for line in source:
            if (lineCount >= chunkLen):
                lineCount = 0;
                cFile.close()
                cFile = open(next(nameGenerator), 'w')
            cFile.write(line)
            lineCount += 1
        cFile.close()

def __nameGenerator(baseName):
    count = 0
    while(True):
        yield '%s-%d' % (baseName, count)
        count += 1


if __name__ == '__main__':
    __main()
