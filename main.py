import sys
from parser.parser import parseFile
from virtual_machine.read import ReadObjFile

if __name__ == '__main__':
    if len(sys.argv) == 2:
        file = open(str(sys.argv[1]), "r")
        user_input = file.read()
        parseFile(user_input)
        read = ReadObjFile()
        read.readObjFile()
    else:
        sys.exit("ERROR: Should be provided with only one file name as argument")
