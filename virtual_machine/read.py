import json
from re import I
from parser.variable_address import VariablesAddress

from parser.variable_semantics import FunctionTable
from virtual_machine.memory import Memory


class ReadObjFile(object):
    '''
    Class to read object file and create function and constant tables.
    '''

    def __init__(self, fileName='obj.json') -> None:
        self.table = FunctionTable()
        self.fileName = fileName
        self.quads = {}
        self.variableAddress = VariablesAddress()
        self.memory = Memory()
        self.instructionsStack = []
        self.currentFunctionCall = ""

    def readObjFile(self) -> None:
        '''
        Function to parse object file and generate 
        function and constant variables and to store the quads.
        '''
        with open(self.fileName) as json_file:
            data = json.load(json_file)
            self.loadData(data)

        iP = 1
        instruction = ""

        while(iP <= len(self.quads)):
            instruction = self.quads[iP - 1][0]
            iPChanged = False

            if instruction == '1':
                data1 = self.memory.getMemoryValue(
                    self.quads[iP - 1][1])
                data2 = self.memory.getMemoryValue(
                    self.quads[iP - 1][2])
                aux = data1 + data2
                address = self.quads[iP - 1][3]
                self.memory.setMemoryValue(address, aux)
            elif instruction == '2':
                data1 = self.memory.getMemoryValue(
                    self.quads[iP - 1][1])
                data2 = self.memory.getMemoryValue(
                    self.quads[iP - 1][2])
                aux = data1 - data2
                address = self.quads[iP - 1][3]
                self.memory.setMemoryValue(address, aux)
            elif instruction == '3':
                data1 = self.memory.getMemoryValue(
                    self.quads[iP - 1][1])
                data2 = self.memory.getMemoryValue(
                    self.quads[iP - 1][2])
                aux = data1 * data2
                address = self.quads[iP - 1][3]
                self.memory.setMemoryValue(address, aux)
            elif instruction == '4':
                data1 = self.memory.getMemoryValue(
                    self.quads[iP - 1][1])
                data2 = self.memory.getMemoryValue(
                    self.quads[iP - 1][2])
                aux = data1 / data2
                address = self.quads[iP - 1][3]
                self.memory.setMemoryValue(address, aux)
            elif instruction == '5':
                data1 = self.memory.getMemoryValue(
                    self.quads[iP - 1][1])
                data2 = self.memory.getMemoryValue(
                    self.quads[iP - 1][2])
                aux = data1 < data2
                address = self.quads[iP - 1][3]
                self.memory.setMemoryValue(address, aux)
            elif instruction == '6':
                data1 = self.memory.getMemoryValue(
                    self.quads[iP - 1][1])
                data2 = self.memory.getMemoryValue(
                    self.quads[iP - 1][2])
                aux = data1 > data2
                address = self.quads[iP - 1][3]
                self.memory.setMemoryValue(address, aux)
            elif instruction == '7':
                data1 = self.memory.getMemoryValue(
                    self.quads[iP - 1][1])
                data2 = self.memory.getMemoryValue(
                    self.quads[iP - 1][2])
                aux = data1 <= data2
                address = self.quads[iP - 1][3]
                self.memory.setMemoryValue(address, aux)
            elif instruction == '8':
                data1 = self.memory.getMemoryValue(
                    self.quads[iP - 1][1])
                data2 = self.memory.getMemoryValue(
                    self.quads[iP - 1][2])
                aux = data1 >= data2
                address = self.quads[iP - 1][3]
                self.memory.setMemoryValue(address, aux)
            elif instruction == '9':
                data1 = self.memory.getMemoryValue(
                    self.quads[iP - 1][1])
                data2 = self.memory.getMemoryValue(
                    self.quads[iP - 1][2])
                aux = data1 == data2
                address = self.quads[iP - 1][3]
                self.memory.setMemoryValue(address, aux)
            elif instruction == '10':
                data1 = self.memory.getMemoryValue(
                    self.quads[iP - 1][1])
                data2 = self.memory.getMemoryValue(
                    self.quads[iP - 1][2])
                aux = data1 != data2
                address = self.quads[iP - 1][3]
                self.memory.setMemoryValue(address, aux)
            elif instruction == '11':
                iP = self.quads[iP - 1][3]
                iPChanged = True
            elif instruction == '12':
                data1 = self.memory.getMemoryValue(self.quads[iP - 1][2])
                if not data1:
                    iP = self.quads[iP - 1][3]
                    iPChanged = True
            elif instruction == '13':
                data1 = self.memory.getMemoryValue(self.quads[iP - 1][2])
                if data1:
                    iP = self.quads[iP - 1][3]
                    iPChanged = True
            elif instruction == '14':
                data1 = self.memory.getMemoryValue(self.quads[iP - 1][3])
                print(data1)
            elif instruction == '15':
                pass
            elif instruction == '16':
                self.memory.deleteLocalMemory()
                self.memory.deleteCurrentMemory()
                iP = self.instructionsStack.pop()
                iPChanged = True
            elif instruction == '17':
                functionName = self.quads[iP - 1][3]
                self.memory.addLocalMemory(
                    self.table.getFunction(functionName))
                self.currentFunctionCall = functionName
            elif instruction == '18':
                address = self.quads[iP - 1][2]
                pNum = self.quads[iP - 1][3] - 1
                paramType = self.table.getParameter(
                    self.currentFunctionCall, pNum)
                self.memory.addLocalParameters(address, pNum, paramType)
            elif instruction == '19':
                function = self.quads[iP - 1][3]

                iP += 1
                self.instructionsStack.append(iP)
                self.memory.setCurrentMemory()
                iP = self.table.getFunctionStartingAddress(function)
                iPChanged = True
            elif instruction == '20':
                data1 = self.memory.getMemoryValue(self.quads[iP - 1][1])
                address = self.quads[iP - 1][3]
                self.memory.setMemoryValue(address, data1)
            else:
                pass

            if not iPChanged:
                iP += 1

    def loadData(self, data: map) -> None:
        self.table.setFunctionMap(data['functionTable'])
        self.table.setConstantTable(data['constantTable'])
        self.quads = data['quads']
        self.memory.loadConstantsInMemory(self.table.getConstants())
        self.memory.loadGlobalsInMemory(
            self.table.getFunction(data['programName']))
        self.memory.addLocalMemory(self.table.getFunction('main'))
        self.memory.setCurrentMemory()
        self.memory.printMemory()
